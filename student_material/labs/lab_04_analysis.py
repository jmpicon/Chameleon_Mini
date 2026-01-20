"""
LAB 04: ANÁLISIS DE TRÁFICO (SNIFFER)
Objetivo: Capturar datos reales y entender el flujo Lector <-> Tarjeta.
"""
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from library.connection import seleccionar_puerto
from library.interface import ChameleonInterface

def lab04():
    puerto = seleccionar_puerto()
    dev = ChameleonInterface(puerto)

    print("--- MODO SNIFFER ACTIVO ---")
    
    # 1. Limpiar logs previos
    dev.enviar_comando("LOGMODE=OFF")
    dev.enviar_comando("CLEAR")

    # 2. TODO: Activa el modo de log en tiempo real usando "LOGMODE=LIVE"
    dev.enviar_comando("LOGMODE=LIVE")

    print("Escuchando... Acerque el Chameleon a un lector de tarjetas.")
    print("Presione Ctrl+C para parar.")

    try:
        while True:
            # Leemos directamente del puerto serie
            if dev.serial.in_waiting > 0:
                linea = dev.serial.readline().decode('ascii', errors='ignore').strip()
                if linea:
                    # RETO PRO: Descomenta las siguientes líneas para usar el traductor automático
                    # from library.translator import ISO14443ATranslator
                    # print(ISO14443ATranslator.translate_line(linea))

                    # TODO: Identifica si la línea empieza por < (Lector) o > (Tarjeta)
                    if "<" in linea:
                        print(f"[LECTOR] -> {linea}")
                    elif ">" in linea:
                        print(f"[TARJETA] -> {linea}")
                    else:
                        print(f"Info: {linea}")
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nCaptura finalizada.")

    dev.enviar_comando("LOGMODE=OFF")
    dev.close()

if __name__ == "__main__":
    lab04()
