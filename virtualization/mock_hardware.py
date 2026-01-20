class ChameleonMock:
    """
    Simulador del hardware Chameleon Mini para pruebas unitarias y entornos virtuales.
    Imita las respuestas del firmware oficial.
    """
    def __init__(self):
        self.slot = 1
        self.configs = {i: "MF_CLASSIC_1K" for i in range(1, 9)}
        self.uids = {i: "01 02 03 04" for i in range(1, 9)}
        self.log_mode = "OFF"
        self.is_open = True

    def handle_command(self, cmd):
        cmd = cmd.strip().upper()
        
        if cmd == "VERSION?":
            return "ChameleonMini RevG (Mock) by José Picón"
        
        if cmd == "CONFIG?":
            return f"{self.configs[self.slot]}\n101:OK WITH TEXT"
            
        if cmd == "UID?":
            return f"{self.uids[self.slot]}\n101:OK WITH TEXT"

        if cmd == "RSSI?":
            return "5000mV\n101:OK WITH TEXT"

        if cmd.startswith("SETTING="):
            try:
                s = int(cmd.split("=")[1])
                if 1 <= s <= 8:
                    self.slot = s
                    return "100:OK"
                return "201:INVALID PARAMETER"
            except: return "200:UNKNOWN COMMAND"

        if cmd.startswith("CONFIG="):
            self.configs[self.slot] = cmd.split("=")[1]
            return "100:OK"

        if cmd.startswith("UID="):
            self.uids[self.slot] = cmd.split("=")[1]
            return "100:OK"

        if cmd == "STORE":
            return "100:OK"
            
        return "200:UNKNOWN COMMAND"

    def readline(self):
        # Implementación mínima para satisfacer el buffer circular en tests
        return b""

    def write(self, data):
        pass

    def close(self):
        self.is_open = False
