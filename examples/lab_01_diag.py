#!/usr/bin/env python3
"""
Lab 01: Diagnóstico de Integridad y Reconocimiento de Hardware
Autor: José Picón
Escenario: El auditor recibe el dispositivo y debe verificar su estado operativo
antes de una intervención.
"""

import sys
import os

# Asegurar que podemos importar desde src (Ajustar si se instala como paquete)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.connection import seleccionar_puerto
from src.interface import ChameleonInterface
from colorama import Fore, Style, init

init(autoreset=True)

def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}=== CHAMELEON MINI: DIAGNÓSTICO PROFESIONAL ===")
    
    puerto = seleccionar_puerto()
    if not puerto:
        print(f"{Fore.RED}[!] ERROR: No se detectó ningún dispositivo.")
        sys.exit(1)

    try:
        dev = ChameleonInterface(puerto)
        
        # 1. Identificación de Identidad
        ver = dev.version_get()
        print(f"\n{Fore.YELLOW}[+] Firmware detectado:")
        print(f"    {ver}")
        
        # 2. Estado de Memoria y Slot
        config = dev.config_get()
        slot = dev.enviar_comando("SETTING?")["data"]
        print(f"\n{Fore.YELLOW}[+] Configuración activa:")
        print(f"    Slot: {slot} | Modo: {config}")
        
        # 3. Salud Eléctrica (RSSI / Battery)
        # Nota: En RevG, esto nos da una lectura de voltaje de antena/batería
        print(f"\n{Fore.YELLOW}[+] Test de Voltaje (RSSI):")
        try:
            rssi = dev.enviar_comando("RSSI?")["data"]
            voltaje = int(str(rssi).replace('mV', '').strip())
            color = Fore.GREEN if voltaje > 4000 else Fore.RED
            print(f"    Voltaje: {color}{voltaje} mV")
            
            if voltaje < 3000:
                print(f"{Fore.RED}    [ALERT] El voltaje es demasiado bajo. Verifique conexión.")
        except:
            print(f"    {Fore.WHITE}Lectura RSSI no disponible en esta revisión.")

        # 4. Verificación de UID Actual
        uid = dev.get_uid()
        print(f"\n{Fore.YELLOW}[+] Identidad RF Actual (UID):")
        print(f"    {Fore.WHITE}{uid}")

        print(f"\n{Fore.CYAN}=== Diagnóstico finalizado con éxito ===")
        dev.close()

    except Exception as e:
        print(f"\n{Fore.RED}[!] Error crítico durante el diagnóstico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
