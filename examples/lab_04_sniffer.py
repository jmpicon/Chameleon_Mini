#!/usr/bin/env python3
"""
Lab 04: Interceptación Avanzada (Live Sniffing)
Autor: José Picón
Escenario: Capturar en tiempo real la comunicación entre un lector y una tarjeta.
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
    print(f"{Fore.CYAN}{Style.BRIGHT}=== CHAMELEON MINI: SNIFFER ISO14443A (LIVE) ===")
    
    puerto = seleccionar_puerto()
    if not puerto: sys.exit(1)

    try:
        dev = ChameleonInterface(puerto)

        print(f"\n{Fore.YELLOW}[*] Preparando hardware para interceptación...")
        # Desactivamos logs previos y configuramos modo Live
        dev.enviar_comando("LOGMODE=OFF")
        dev.enviar_comando("CLEAR")
        dev.enviar_comando("LOGMODE=LIVE")

        print(f"{Fore.GREEN}[LIVE] Escuchando tráfico RF. Interacción detectada:")
        print(f"{Fore.WHITE}(Presione Ctrl+C para finalizar y guardar log)")
        
        log_captured = []
        
        try:
            while True:
                if dev.serial.in_waiting > 0:
                    raw_line = dev.serial.readline().decode('ascii', errors='ignore').strip()
                    if raw_line and not raw_line.isdigit():
                        # Diferenciar entre datos del lector y de la tarjeta
                        # En Chameleon, < es entrada (lector) y > es salida (tarjeta emulada)
                        prefix = f"{Fore.RED}[Lector] " if "<" in raw_line else f"{Fore.BLUE}[Tarjeta] "
                        print(f"{prefix}{Fore.WHITE}{raw_line}")
                        log_captured.append(raw_line)
                time.sleep(0.01)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Deteniendo captura...")
        
        # Guardar en archivo para análisis forense
        if log_captured:
            filename = f"capture_{int(time.time())}.log"
            with open(filename, "w") as f:
                f.write("\n".join(log_captured))
            print(f"{Fore.GREEN}[OK] Log guardado en: {filename}")
        
        # Limpieza
        dev.enviar_comando("LOGMODE=OFF")
        dev.close()

    except Exception as e:
        print(f"{Fore.RED}[!] Error en sniffer: {e}")

if __name__ == "__main__":
    main()
