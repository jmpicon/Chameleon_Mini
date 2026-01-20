import pytest
from src.interface import ChameleonInterface
from virtualization.mock_hardware import ChameleonMock

@pytest.fixture
def mock_dev():
    mock = ChameleonMock()
    return ChameleonInterface(mock_device=mock)

def test_version_command(mock_dev):
    version = mock_dev.version_get()
    assert "Mock" in version
    assert "José Picón" in version

def test_uid_persistence_simulation(mock_dev):
    # Probar que en el modo simulado podemos cambiar UIDs
    target_uid = "DE AD BE EF"
    resp = mock_dev.enviar_comando(f"UID={target_uid}")
    assert resp['success'] is True
    
    # Verificar que se lee correctamente
    current_uid = mock_dev.get_uid()
    assert current_uid == target_uid

def test_invalid_command(mock_dev):
    resp = mock_dev.enviar_comando("BLOOP")
    assert resp['success'] is False
    assert resp['code'] == 200

def test_slot_switching(mock_dev):
    mock_dev.enviar_comando("SETTING=2")
    # En el mock, el slot 2 tiene un UID por defecto
    assert mock_dev.enviar_comando("SETTING?")['data'] == "2"
