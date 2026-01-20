import sys
import glob
import logging
import serial.tools.list_ports

# Configuración de logging profesional
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("ChameleonConn")

def listar_puertos_candidatos():
    """
    Busca puertos serie que coincidan con firmas conocidas del Chameleon Mini.
    Retorna una lista de dispositivos.
    """
    candidatos = []
    
    # IDs conocidos:
    # 0x03EB: Atmel Corp / 0x2044: LUFA CDC Demo Application (Default)
    # 0x16C0: Van Ooijen / 0x0483: STM32 (Clones/Custom)
    ids_conocidos = [
        (0x03EB, 0x2044),
        (0x16C0, 0x0483),
        (0x16C0, 0x05DC) # Algunos modelos RevE
    ]
    
    try:
        puertos = serial.tools.list_ports.comports()
        for p in puertos:
            logger.debug(f"Escaneando: {p.device} | VID:{p.vid:04x} PID:{p.pid:04x} | HWID: {p.hwid}")
            if (p.vid, p.pid) in ids_conocidos:
                candidatos.append(p.device)
    except Exception as e:
        logger.error(f"Error al listar puertos via serial.tools: {e}")
            
    # Fallback heurístico si no hay coincidencias por ID (útil en algunos drivers de Windows/Linux)
    if not candidatos:
        if sys.platform.startswith('darwin'):
            candidatos = glob.glob('/dev/cu.usbmodem*')
        elif sys.platform.startswith('linux'):
            candidatos = glob.glob('/dev/chameleon') + glob.glob('/dev/ttyACM*')
        elif sys.platform.startswith('win'):
            # En Windows es difícil sin VID/PID, pero serial.tools suele funcionar.
            pass
            
    return list(set(candidatos)) # Evitar duplicados

def seleccionar_puerto():
    """
    Intenta auto-detectar el puerto. Si hay múltiples, retorna el primero.
    """
    puertos = listar_puertos_candidatos()
    if not puertos:
        logger.error("No se detectó ningún Chameleon Mini. Compruebe la conexión o los permisos UDEV.")
        return None
    
    if len(puertos) > 1:
        logger.warning(f"Múltiples dispositivos detectados: {puertos}. Usando {puertos[0]}")
    else:
        logger.info(f"Dispositivo detectado en: {puertos[0]}")
        
    return puertos[0]
