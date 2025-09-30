import pytest
import tempfile
from pathlib import Path
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.service.AutenticacaoService import criar_conta, login, checar_usarios
from src.models.Usuario import Usuario


class TesteIntegracao:

    def test_10_usuario_criado_aparece_na_lista(self):
        #Teste 10: Usuário criado aparece na lista de usuários

        #Configura ambiente isolado
        temp_dir = tempfile.TemporaryDirectory()
        test_data_path = Path(temp_dir.name) / "usuarios.json"

        import src.service.AutenticacaoService as auth_service
        original_path = auth_service.arquivo
        auth_service.arquivo = test_data_path

        try:
            #Cria arquivo vazio
            with open(test_data_path, 'w') as f:
                json.dump({}, f)

            #Cria usuário
            criar_conta("usuario_lista", "senha123")

            #Verifica se aparece na lista
            usuarios = checar_usarios()
            assert "usuario_lista" in usuarios

            #Verifica se pode fazer login
            resultado_login = login("usuario_lista", "senha123")
            assert resultado_login == True

        finally:
            #Limpeza
            auth_service.arquivo = original_path
            temp_dir.cleanup()