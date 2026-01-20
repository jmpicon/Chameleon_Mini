#!/usr/bin/env python3
"""
Lab 02: Gestión de Memoria Multicapa (Slots)
Autor: José Picón
Escenario: Configurar múltiples identidades en un solo dispositivo físico.
"""

import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.connection import seleccionar_puerto
from src.interface import ChameleonInterface
from colorama import Fore, Style, init

init(autoreset=True)

def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}=== CHAMELEON MINI: VIRTUALIZACIÓN DE TARJETAS ===")
    
    puerto = seleccionar_puerto()
    if not puerto: sys.exit(1)

    try:
        dev = ChameleonInterface(puerto)

        # --- SLOT 1: MIFARE CLASSIC (Auditoría Corporativa) ---
        print(f"\n{Fore.GREEN}[*] Configurando SLOT 1: Perfil Corporativo")
        dev.enviar_comando("SETTING=1")
        dev.enviar_comando("CONFIG=MF_CLASSIC_1K")
        dev.enviar_comando("UID=A1 B2 C3 D4")
        dev.enviar_comando("STORE") # Persistir en memoria no volátil
        print(f"    -> Slot 1 listo (UID: A1B2C3D4)")

        # --- SLOT 2: MIFARE ULTRALIGHT (Auditoría Transporte) ---
        print(f"\n{Fore.GREEN}[*] Configurando SLOT 2: Perfil Transporte")
        dev.enviar_comando("SETTING=2")
        dev.enviar_comando("CONFIG=MF_ULTRALIGHT")
        dev.enviar_comando("UID=04 E1 22 33 44 55 66")
        dev.enviar_comando("STORE")
        print(f"    -> Slot 2 listo (UID: 7-byte Ultralight)")

        # --- PRUEBA DE PERSISTENCIA ---
        print(f"\n{Fore.YELLOW}[?] Verificando cambio de contexto...")
        time.sleep(1)
        
        dev.enviar_comando("SETTING=1")
        check_1 = dev.get_uid()
        print(f"    -> Recuperado Slot 1: {Fore.WHITE}{check_1}")

        dev.enviar_comando("SETTING=2")
        check_2 = dev.get_uid()
        print(f"    -> Recuperado Slot 2: {Fore.WHITE}{check_2}")

        print(f"\n{Fore.CYAN}[+] Operación de slots completada.")
        dev.close()

    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}")

if __name__ == "__main__":
    main()
