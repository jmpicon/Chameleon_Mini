# ChameleonLib: Suite Avanzada de Auditoría RFID y Emulación de Hardware
### Por José Picón - Especialista en Ciberseguridad y Auditoría Física

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Chameleon Mini](https://img.shields.io/badge/Hardware-Chameleon%20Mini-orange)

## 1. Visión del Proyecto

Como profesional y docente en el ámbito de la seguridad ofensiva, he observado que existe un abismo crítico entre la teoría de la radiofrecuencia (RF) y su aplicación táctica en el terreno. Este repositorio no es solo un conjunto de scripts; es el resultado de mi experiencia auditando sistemas de control de acceso y mi deseo de proporcionar una base de ingeniería sólida para el **Red Teaming**.

**ChameleonLib** es un wrapper de Python diseñado para elevar al Chameleon Mini (RevE/RevG) de ser un simple emulador de tarjetas a una plataforma de automatización programable. El objetivo es que tú, como auditor, dejes de depender de herramientas gráficas limitadas y empieces a desarrollar tus propias capacidades de interceptación, manipulación y clonación de activos RFID.

---

## 2. El Paradigma de la Emulación de Hardware

En mis auditorías, el tiempo es el recurso más escaso. El Chameleon Mini es excelente porque abstrae los desafíos físicos de la capa PHY (modulación, codificación), permitiéndonos concentrarnos en la capa de aplicación. Sin embargo, su interfaz ASCII, aunque didáctica, requiere una gestión precisa de tiempos y estados para ser efectiva en entornos automatizados.

### ¿Por qué esta arquitectura?
He diseñado esta suite dividiéndola en tres capas fundamentales:
1.  **Capa de Conectividad (`connection.py`)**: Gestión inteligente de puertos CDC en entornos multiplataforma (Evitando el "infierno de los puertos serie").
2.  **Capa de Interfaz (`interface.py`)**: Un motor de parsing robusto que interpreta los códigos de estado del firmware (1xx, 2xx) y maneja los buffers para evitar colisiones de datos.
3.  **Capa de Aplicación (Labs/Examples)**: Implementaciones tácticas para escenarios reales: desde diagnóstico veloz hasta sniffing en tiempo real.

---

## 3. Instalación y Configuración del Entorno

### Requisitos Previos
Necesitarás Python 3.8 o superior. Recomiendo encarecidamente trabajar en un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Linux/macOS
pip install -r requirements.txt
```

### Configuración Específica de OS (Mi recomendación profesional)

#### En Linux (Ubuntu/Kali)
No luches con los permisos. Crea una regla UDEV para que el Chameleon siempre sea `/dev/chameleon`:

```bash
echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2044", MODE="0666", SYMLINK+="chameleon"' | sudo tee /etc/udev/rules.d/99-chameleon.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
```

#### En macOS
Usa siempre los dispositivos `/dev/cu.usbmodem*`. He configurado la detección automática para priorizar estos puertos, evitando bloqueos por control de flujo de módem heredado.

---

## 4. Estructura del Repositorio

-   `src/`: El "motor" del proyecto. `ChameleonInterface` gestiona toda la comunicación.
-   `src/web_dashboard.py`: **¡NUEVO!** Panel de control web visual y moderno.
-   `src/cli.py`: Herramienta de línea de comandos para uso rápido.
-   `examples/`: Scripts terminados y listos para usar en auditorías reales.
-   `student_material/`: Una versión simplificada y comentada para alumnos.

---

## 5. Uso con Docker y Panel Web

Hemos preparado un entorno contenerizado que incluye tanto las herramientas de terminal como el **Dashboard Web**.

### Construir y Ejecutar
```bash
docker-compose up -d --build
```

### Acceso a las Herramientas
1.  **Dashboard Web**: Abre tu navegador en `http://localhost:8501`.
    *   Interfaz gráfica para controlar slots, cambiar UIDs y ver el tráfico en tiempo real traducido.
2.  **Terminal**: Si prefieres la consola:
    ```bash
    docker exec -it chameleon_pro_lab /bin/bash
    ```

### Ejecución Local del Dashboard (Sin Docker)
Si prefieres correrlo directamente en tu máquina (requiere Python 3.8+):
```bash
pip install -r requirements.txt
streamlit run src/web_dashboard.py
```

### Notas sobre Hardware en Docker
Estad atentos a mapear correctamente el dispositivo USB (`/dev/ttyACM0`) en el archivo `docker-compose.yml`. Si no tenéis el dispositivo, podéis usar el **Modo Simulador** en el Dashboard.

---

## 6. Futuras Mejoras (Roadmap)

Como docente y auditor, mi visión para este proyecto incluye:

1.  **Dashboard de Monitoreo**: Una interfaz web (Streamlit/Flask) para visualizar el sniffing en tiempo real con gráficos de ocupación de banda.
2.  **Analizador de Protocolos Avanzado**: Traducción automática de tramas RAW a comandos legibles (ej: "Lector enviando SELECT", "Tarjeta respondiendo ATS").
3.  **Simulador Integrado**: Un sistema de mocks para que los alumnos puedan programar y testear sus scripts sin necesidad de tener el hardware físico conectado.
4.  **Soporte DESFire/Ultralight C**: Ampliación de la biblioteca para manejar protocolos con cifrado avanzado.

---

## 7. El Camino del Estudiante: Del Bit al Acceso

Este proyecto está estructurado pedagógicamente. Si eres docente o estás usando este material para formación:
1.  **Fundamentos**: Entender el protocolo de comandos ASCII.
2.  **Mutabilidad**: Aprender que el UID no es una constante inmutable, sino un parámetro de software.
3.  **Persistencia**: Configurar el dispositivo para operaciones "Headless" (Sin PC).
4.  **Invisibilidad**: Dominar el sniffing pasivo para recolectar vectores de ataque sin ser detectado.

---

## 6. Consideraciones Éticas

Como autor, enfatizo que el uso de estas herramientas debe limitarse estrictamente a entornos controlados, laboratorios académicos o auditorías de seguridad debidamente autorizadas. La potencia para clonar un UID es real, pero la responsabilidad del auditor es documentar la vulnerabilidad para fortalecer la infraestructura, no para explotarla con fines maliciosos.

---

## 7. Contacto y Contribuciones

Este proyecto está en constante evolución. Si encuentras un bug o quieres proponer una mejora en la gestión de protocolos (como ampliar a ISO15693), siéntete libre de abrir un Pull Request.

**José Picón**
*Consultor de Seguridad Ofensiva | Especialista en Hardware Hacking*
