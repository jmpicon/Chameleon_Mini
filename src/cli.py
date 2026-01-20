import argparse
import sys
from .connection import seleccionar_puerto
from .interface import ChameleonInterface
from colorama import Fore, Style, init

init(autoreset=True)

def main():
    parser = argparse.ArgumentParser(description="ChameleonLib CLI - Suite de Auditoría RFID por José Picón")
    parser.add_argument("--port", help="Puerto serie del Chameleon")
    
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")
    
    # Comando Info
    subparsers.add_parser("info", help="Muestra información del dispositivo")
    
    # Comando Get UID
    subparsers.add_parser("get-uid", help="Obtiene el UID actual")
    
    # Comando Set UID
    set_uid = subparsers.add_parser("set-uid", help="Cambia el UID del slot actual")
    set_uid.add_argument("uid", help="Nuevo UID (ej: 'DE AD BE EF')")
    
    # Comando Config
    config = subparsers.add_parser("config", help="Cambia la configuración del slot")
    config.add_argument("mode", help="Modo de emulación (ej: MF_CLASSIC_1K)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return

    puerto = args.port or seleccionar_puerto()
    if not puerto:
        print(f"{Fore.RED}Error: Dispositivo no detectado.")
        sys.exit(1)
        
    dev = ChameleonInterface(puerto)
    
    try:
        if args.command == "info":
            print(f"{Fore.CYAN}Firmware:{Fore.WHITE} {dev.version_get()}")
            print(f"{Fore.CYAN}Config:{Fore.WHITE}   {dev.config_get()}")
            print(f"{Fore.CYAN}UID:{Fore.WHITE}      {dev.get_uid()}")
            
        elif args.command == "get-uid":
            print(dev.get_uid())
            
        elif args.command == "set-uid":
            resp = dev.enviar_comando(f"UID={args.uid}")
            if resp['success']:
                print(f"{Fore.GREEN}UID actualizado a {args.uid}")
            else:
                print(f"{Fore.RED}Error al actualizar UID")
                
        elif args.command == "config":
            resp = dev.enviar_comando(f"CONFIG={args.mode}")
            if resp['success']:
                print(f"{Fore.GREEN}Modo cambiado a {args.mode}")
            else:
                print(f"{Fore.RED}Error al cambiar configuración")
                
    finally:
        dev.close()

if __name__ == "__main__":
    main()
