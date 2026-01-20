from src.translator import ISO14443ATranslator

def test_reader_reqa():
    line = "< 26"
    result = ISO14443ATranslator.translate_line(line)
    assert "[LECTOR]" in result
    assert "REQA" in result

def test_card_atqa():
    line = "> 00 04"
    result = ISO14443ATranslator.translate_line(line)
    assert "[TARJETA]" in result
    assert "ATQA" in result

def test_unknown_command():
    line = "< FF FF"
    result = ISO14443ATranslator.translate_line(line)
    assert "[LECTOR]" in result
    assert "Comando Desconocido" in result

def test_mifare_auth():
    line = "< 60 10"
    result = ISO14443ATranslator.translate_line(line)
    assert "AUTH" in result
    assert "Key A" in result
    assert "Sector 10" in result
