import serial
import time
import logging
import sys

class ChameleonInterface:
    """
    Clase maestra para la comunicación con Chameleon Mini.
    Implementa el protocolo ASCII y gestión de estados del firmware.
    """
    
    def __init__(self, port=None, timeout=2, mock_device=None):
        self.logger = logging.getLogger("ChameleonAPI")
        self.port = port
        self.mock_mode = mock_device is not None
        
        if self.mock_mode:
            self.serial = mock_device
            self.logger.info("Iniciando en modo SIMULACIÓN (Mock Hardware)")
            return

        try:
            # Aunque sea CDC, definimos un baudrate estándar
            self.serial = serial.Serial(port, 115200, timeout=timeout)
            time.sleep(0.1) # Tiempo de estabilización tras apertura
            self.limpiar_buffers()
            self.logger.info(f"Conexión abierta en {port}")
        except serial.SerialException as e:
            self.logger.critical(f"Error fatal al abrir el puerto {port}: {e}")
            raise

    def limpiar_buffers(self):
        """Limpia la basura residual en los buffers de entrada/salida."""
        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()

    def enviar_comando(self, comando, esperar_respuesta=True):
        """
        Envía un comando ASCII y parsea la respuesta estructurada.
        """
        if self.mock_mode:
            raw_response = self.serial.handle_command(comando)
            # Simular comportamiento de líneas para el parser
            lineas = raw_response.split('\n')
            codigo = int(lineas[-1].split(':')[0]) if ':' in lineas[-1] else int(lineas[-1][:3])
            mensaje = lineas[-1].split(':', 1)[1].strip() if ':' in lineas[-1] else ""
            return self._parsear_respuesta(codigo, mensaje, lineas)

        if not self.serial.is_open:
            raise ConnectionError("La conexión serie se ha perdido.")

        # Limpiar antes de enviar para asegurar sincronización
        self.limpiar_buffers()
        
        cmd_str = comando.strip() + "\r\n"
        self.serial.write(cmd_str.encode('ascii'))
        
        if not esperar_respuesta:
            return None

        lineas = []
        timeout_limit = time.time() + self.serial.timeout
        
        while time.time() < timeout_limit:
            try:
                # Usamos errors='ignore' para evitar crashes con bytes no-ASCII del log
                linea = self.serial.readline().decode('ascii', errors='ignore').strip()
            except Exception as e:
                self.logger.error(f"Error de lectura: {e}")
                break

            if not linea:
                continue

            # Ignorar eco local si el firmware lo tiene activado
            if linea == comando.strip():
                continue

            lineas.append(linea)

            # El protocolo Chameleon termina con un código de estado tipo '101:OK WITH TEXT'
            if len(linea) >= 3 and linea[:3].isdigit() and (':' in linea or linea[3:].strip() == ""):
                try:
                    codigo = int(linea.split(':')[0]) if ':' in linea else int(linea[:3])
                    mensaje = linea.split(':', 1)[1].strip() if ':' in linea else ""
                    return self._parsear_respuesta(codigo, mensaje, lineas)
                except ValueError:
                    continue # No era un código de estado real
        
        raise TimeoutError(f"Timeout esperando respuesta al comando: {comando}")

    def _parsear_respuesta(self, codigo, mensaje, histórico):
        """Transforma la respuesta bruta en un objeto Python manejable."""
        dato = None
        
        # Lógica de extracción de carga útil (Payload)
        if codigo == 101: # OK WITH TEXT
            if len(histórico) > 1:
                # El dato suele estar en la línea previa al código de estado
                # Ejemplo: 
                # [Línea 0] MF_CLASSIC_1K
                # [Línea 1] 101:OK WITH TEXT
                dato = histórico[-2]
            else:
                dato = mensaje # A veces viene en la misma línea
        
        # Mapeo booleano
        elif codigo == 120: dato = False # FALSE
        elif codigo == 121: dato = True  # TRUE
        
        # Gestión de errores conocidos
        éxito = (100 <= codigo < 200)

        return {
            "success": éxito,
            "code": codigo,
            "msg": mensaje,
            "data": dato,
            "raw": histórico
        }

    def config_get(self):
        """Helper para obtener la configuración actual."""
        return self.enviar_comando("CONFIG?")["data"]

    def version_get(self):
        """Helper para obtener la versión del firmware."""
        return self.enviar_comando("VERSION?")["data"]

    def get_uid(self):
        """Obtiene el UID del slot actual."""
        return self.enviar_comando("UID?")["data"]

    def close(self):
        """Cierra el puerto de forma segura."""
        if hasattr(self, 'serial') and self.serial.is_open:
            self.serial.close()
            self.logger.info("Conexión cerrada.")
