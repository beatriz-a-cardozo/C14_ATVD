import pytest
import tempfile
import json
from pathlib import Path


@pytest.fixture
def temp_json_file():
    #Fixture para criar arquivo JSON temporário
    with tempfile.NamedTemporaryFile(mode = 'w', suffix = '.json', delete = False) as f:
        json.dump({}, f)
        temp_path = f.name

    yield Path(temp_path)

    #Limpeza
    Path(temp_path).unlink()

@pytest.fixture
def sample_usuario_data():
    #Fixture com dados de exemplo de usuário
    return {
        "nome_de_usuario": "testuser",
        "senha_hash": "testhash",
        "saldo": 1000.0,
        "gasto_fixo": [],
        "gasto_do_mes": [],
        "fatura": [],
        "receitas": []
    }