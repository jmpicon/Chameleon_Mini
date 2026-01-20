# Guía del Estudiante: Auditoría de Sistemas de Acceso con Chameleon Mini
### Instructor: José Picón

## ¡Bienvenido al Laboratorio!
Este material ha sido diseñado para que pases de ser un usuario de herramientas a un desarrollador de tecnología de seguridad. A lo largo de estos laboratorios, aprenderás a interactuar con el hardware **Chameleon Mini** usando Python.

---

## 1. Estructura de Trabajo
En tu carpeta de trabajo encontrarás:
-   `library/`: Contiene el código base que gestiona la comunicación con el dispositivo. No necesitas modificarlo, pero te invito a leerlo para entender cómo manejamos los puertos serie.
-   `labs/`: Aquí están tus misiones. Algunos archivos tienen partes incompletas que deberás rellenar basándote en la teoría.

---

## 2. Antes de empezar
Asegúrate de tener instaladas las dependencias necesarias:
```bash
pip install pyserial colorama
```

Si estás en **Linux**, recuerda aplicar la regla UDEV que vimos en clase para evitar problemas de permisos con el puerto `/dev/ttyACM0`.

---

## 3. Tus Misiones

### Laboratorio 00: Laboratorio Virtual (¡Nuevo!)
**Objetivo:** Aprender a programar sin necesidad del hardware físico.
- Usarás el simulador `ChameleonMock`.
- Ideal para practicar en casa o en el bus antes de llegar al laboratorio real.

### Laboratorio 01: Contacto Inicial
**Objetivo:** Verificar que tu ordenador "habla" con el Chameleon.
-   Aprenderás a usar el comando `VERSION?` y `RSSI?`.
-   **Reto:** ¿Qué voltaje devuelve tu antena cuando estás conectado por USB?

### Laboratorio 02: El Camaleón
**Objetivo:** Clonar un UID y entender los Slots.
-   Configuraremos el Slot 1 como una tarjeta Mifare Classic.
-   Cambiaremos el UID a `DE AD BE EF`.
-   **Reto:** Comprueba si el cambio persiste después de desconectar y volver a conectar el dispositivo.

### Laboratorio 03: Operaciones Encubiertas
**Objetivo:** Programar el dispositivo para usarlo sin ordenador (Modo Autónomo).
-   Asignaremos funciones a los botones físicos.
-   **Reto:** Configura el botón derecho para que genere un UID aleatorio cada vez que lo pulses.

### Laboratorio 04: Cazador de Datos (Sniffer)
**Objetivo:** Interceptar una conversación entre un lector de pared y una tarjeta real.
-   Usaremos el modo `LOGMODE=LIVE`.
-   **Reto:** Identifica en el log qué parte es la pregunta del lector y qué parte es la respuesta de la tarjeta.

---

## 4. Consejos de José Picón
-   "El hardware no miente, pero los buffers sí". Si recibes datos extraños, limpia el buffer.
-   "Lee la respuesta del dispositivo". El Chameleon siempre te dirá si un comando falló con un código `2xx`.
-   **Seguridad Ética:** Lo que aprendas aquí es una herramienta potente. Úsala siempre con permiso y dentro del marco legal.

¡A por ello!
