"""
LAB 03: OPERACIONES DE CAMPO (BOTONES)
Objetivo: Preparar el Chameleon para una auditoría física sin cables.
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from library.connection import seleccionar_puerto
from library.interface import ChameleonInterface

def lab03():
    puerto = seleccionar_puerto()
    dev = ChameleonInterface(puerto)

    print("--- PROGRAMACIÓN DE BOTONES FÍSICOS ---")

    # Misión:
    # Queremos que al pulsar el botón L (Izquierdo) se genere un UID aleatorio.
    # Y que al pulsar el botón R (Derecho) se cambie al siguiente Slot.

    # 1. Configurar LBUTTON
    # TODO: Usa el comando "LBUTTON=UID_RANDOM"
    dev.enviar_comando("LBUTTON=UID_RANDOM")

    # 2. Configurar RBUTTON
    # TODO: Usa el comando "RBUTTON=SETTING_INC"
    dev.enviar_comando("RBUTTON=SETTING_INC")

    # 3. Guardar configuración
    dev.enviar_comando("STORE")

    print("Configuración autónoma completada.")
    print("Prueba: Desconecta el USB y pulsa los botones. ¿Ves cambiar los LEDs?")

    dev.close()

if __name__ == "__main__":
    lab03()
