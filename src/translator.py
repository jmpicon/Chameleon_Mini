"""
Módulo de Traducción de Protocolos RFID (ISO14443A)
Autor: José Picón
Este módulo actúa como una capa de inteligencia para interpretar tramas RAW 
capturadas por el Chameleon Mini.
"""

class ISO14443ATranslator:
    # Diccionario de comandos del Lector (PCD)
    PCD_COMMANDS = {
        "26": "REQA (Request Command, Type A)",
        "52": "WUPA (Wake-Up Command, Type A)",
        "9320": "ANTICOLLISION (Select Cascade Level 1)",
        "9370": "SELECT (Cascade Level 1)",
        "9520": "ANTICOLLISION (Select Cascade Level 2)",
        "9570": "SELECT (Cascade Level 2)",
        "E0": "RATS (Request for Answer to Select)",
        "5000": "HALT (Halt Command)",
    }

    # Diccionario de respuestas comunes de la Tarjeta (PICC)
    PICC_RESPONSES = {
        "0004": "ATQA (Mifare Classic / Ultralight)",
        "0044": "ATQA (Mifare Ultralight)",
        "08": "SAK (Mifare Classic 1K)",
        "88": "SAK (Cascade bit set - UID not complete)",
        "20": "SAK (ISO/IEC 14443-4 compatible)",
    }

    @classmethod
    def translate_line(cls, line):
        """
        Interpreta una línea de log del Chameleon.
        Ejemplo: '< 93 20' -> '[LECTOR] ANTICOLLISION'
        """
        line = line.strip()
        if not line:
            return ""

        # Identificar dirección del tráfico
        is_reader = line.startswith("<")
        is_tag = line.startswith(">")
        
        # Limpiar la trama (quitar prefijo y espacios)
        raw_hex = line[1:].replace(" ", "").upper()
        
        if is_reader:
            prefix = "[LECTOR] "
            meaning = cls.PCD_COMMANDS.get(raw_hex, "Comando Desconocido / Datos de Aplicación")
            # Caso especial: Autenticación Mifare (60xx o 61xx)
            if raw_hex.startswith("60") or raw_hex.startswith("61"):
                meaning = f"AUTH (Mifare Auth Key {'A' if raw_hex.startswith('60') else 'B'}) Sector {raw_hex[2:4]}"
        elif is_tag:
            prefix = "[TARJETA] "
            meaning = cls.PICC_RESPONSES.get(raw_hex, "Datos / UID / Response")
        else:
            return f"[INFO] {line}"

        return f"{prefix}{raw_hex.ljust(10)} | {meaning}"
