"""
LAB 01: SETUP Y VERIFICACIÓN
Instrucciones: Completa las líneas marcadas con 'TODO'.
"""
import sys
import os

# Importamos la librería desde la carpeta superior
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from library.connection import seleccionar_puerto
from library.interface import ChameleonInterface

def lab01():
    print("--- INICIANDO PROTOCOLO DE CONEXIÓN ---")
    
    # 1. Detectar el puerto
    puerto = seleccionar_puerto()
    if not puerto:
        print("Error: No se encuentra el Chameleon. ¿Está conectado?")
        return

    # 2. Abrir la interfaz
    dev = ChameleonInterface(puerto)

    # 3. TODO: Obtén la versión del dispositivo usando el comando "VERSION?"
    # Pista: usa dev.enviar_comando("...")
    respuesta_version = dev.enviar_comando("VERSION?")
    print(f"Versión detectada: {respuesta_version['data']}")

    # 4. TODO: Consulta el estado de la antena con el comando "RSSI?"
    # Imprime el valor resultante.
    respuesta_rssi = dev.enviar_comando("RSSI?")
    print(f"Estado de Antena/Voltaje: {respuesta_rssi['data']}")

    dev.close()
    print("--- FIN DEL LAB 01 ---")

if __name__ == "__main__":
    lab01()
