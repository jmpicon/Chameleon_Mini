#!/usr/bin/env python3
"""
Lab 03: Configuración Headless (Operaciones de Campo)
Autor: José Picón
Escenario: El auditor debe usar el dispositivo sin PC. Se programan los botones
para acciones rápidas en el bolsillo.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.connection import seleccionar_puerto
from src.interface import ChameleonInterface
from colorama import Fore, Style, init

init(autoreset=True)

def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}=== CHAMELEON MINI: PERFIL DE CAMPO (STEALTH) ===")
    
    puerto = seleccionar_puerto()
    if not puerto: sys.exit(1)

    try:
        dev = ChameleonInterface(puerto)

        print(f"\n{Fore.YELLOW}[+] Programando HMI (Interfaz Humana)...")

        # RBUTTON (Pulsación corta derecho): Cambiar de Slot
        dev.enviar_comando("RBUTTON=SETTING_INC")
        print(f"    - Botón Derecho: Rotar Slots (Ciclo de identidades)")

        # LBUTTON (Pulsación corta izquierdo): Clonar UID
        # (Funciona mejor en RevG con modo lector)
        dev.enviar_comando("LBUTTON=CLONE")
        print(f"    - Botón Izquierdo: Clonación rápida (Proximidad)")

        # LBUTTON_LONG (Derecho Largo): Identidad Aleatoria
        # Útil para evadir listas negras temporales
        dev.enviar_comando("LBUTTON_LONG=UID_RANDOM")
        print(f"    - Izquierdo Largo: Generar Identidad Aleatoria")

        # Guardar todo
        dev.enviar_comando("STORE")

        print(f"\n{Fore.GREEN}[OK] Perfil 'Red Team' cargado con éxito.")
        print(f"{Fore.WHITE}\nInstrucciones tácticas:")
        print("1. Desconecte el dispositivo.")
        print("2. Use el botón derecho para seleccionar la tarjeta objetivo.")
        print("3. Acerque el Chameleon a una tarjeta víctima y pulse el izquierdo.")
        print("4. Presente el Chameleon al lector para obtener acceso.")

        dev.close()

    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}")

if __name__ == "__main__":
    main()
