"""
LAB 00: LABORATORIO VIRTUAL (MODO SIMULACIÓN)
Autor: José Picón
Escenario: No tienes el hardware físico contigo, pero necesitas probar un script de 
clonación antes de ir a la oficina o al cliente.
"""
import sys
import os

# Importamos la librería desde la carpeta de materiales
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from library.interface import ChameleonInterface
from library.mock_hardware import ChameleonMock

def lab_virtual():
    print("--- INICIANDO ENTORNO VIRTUAL DE PRUEBAS ---")

    # 1. Creamos el hardware simulado
    # Este objeto imita el comportamiento de los comandos del Chameleon real.
    mock_hardware = ChameleonMock()

    # 2. Inicializamos la interfaz en MODO SIMULACIÓN
    # Observa que no pasamos un puerto, sino el objeto mock_hardware.
    dev = ChameleonInterface(mock_device=mock_hardware)

    print("\n[VIRTUAL] Consultando versión del hardware simulado...")
    print(f"Versión: {dev.version_get()}")

    # 3. Probando un comando de configuración
    print("\n[VIRTUAL] Cambiando configuración a MF_ULTRALIGHT...")
    dev.enviar_comando("CONFIG=MF_ULTRALIGHT")
    
    # 4. Verificando que el simulador ha guardado el estado
    config_actual = dev.config_get()
    print(f"Configuración actual: {config_actual}")

    if config_actual == "MF_ULTRALIGHT":
        print("\n[EXITO] El script funciona correctamente en el simulador.")
        print("Ahora puedes usarlo con el Chameleon real sin miedo a errores de sintaxis.")
    else:
        print("\n[ERROR] Algo falló en la lógica del script.")

    dev.close()
    print("\n--- FIN DEL LABORATORIO VIRTUAL ---")

if __name__ == "__main__":
    lab_virtual()
