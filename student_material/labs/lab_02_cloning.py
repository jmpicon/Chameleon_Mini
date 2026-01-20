"""
LAB 02: CLONACIÓN DE IDENTIDAD (UID)
Objetivo: Configurar el Chameleon para que se comporte como una tarjeta específica.
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from library.connection import seleccionar_puerto
from library.interface import ChameleonInterface

def lab02():
    puerto = seleccionar_puerto()
    dev = ChameleonInterface(puerto)

    print("--- EMPEZANDO PROCESO DE CLONACIÓN ---")

    # 1. Seleccionar el Slot 1
    dev.enviar_comando("SETTING=1")

    # 2. Configurar como Mifare Classic 1K
    # TODO: Usa el comando "CONFIG=MF_CLASSIC_1K"
    dev.enviar_comando("CONFIG=MF_CLASSIC_1K")

    # 3. Cambiar el UID
    uid_nuevo = "CA FE BA BE"
    print(f"Cambiando UID a: {uid_nuevo}")
    # TODO: Usa el comando "UID=..." con la variable uid_nuevo
    dev.enviar_comando(f"UID={uid_nuevo}")

    # 4. Verificar el cambio
    check = dev.enviar_comando("UID?")
    print(f"UID configurado en el hardware: {check['data']}")

    # 5. Persistencia
    # TODO: Envía el comando "STORE" para que no se borre al desconectar
    dev.enviar_comando("STORE")
    print("Datos guardados en memoria Flash.")

    dev.close()

if __name__ == "__main__":
    lab02()
