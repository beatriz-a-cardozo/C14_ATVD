import pytest
import tempfile
from pathlib import Path
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.service.AutenticacaoService import criar_conta, login, checar_usarios


class TesteAutenticacao:

    def criar_ambiente_teste(self):
        #Cria ambiente isolado para cada teste
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_data_path = Path(self.temp_dir.name) / "usuarios.json"

        import src.service.AutenticacaoService as auth_service
        self.original_path = auth_service.arquivo
        auth_service.arquivo = self.test_data_path

        with open(self.test_data_path, 'w') as f:
            json.dump({}, f)

        return auth_service

    def limpar_ambiente_teste(self, auth_service):
        #Limpa ambiente após cada teste
        auth_service.arquivo = self.original_path
        self.temp_dir.cleanup()

    def test_01_criar_usuario_sucesso(self):
        #Teste 1: Criar usuário retorna sucesso
        auth_service = self.criar_ambiente_teste()
        try:
            resultado = criar_conta("novousuario", "senha123")
            assert resultado == True

            usuarios = checar_usarios()
            assert "novousuario" in usuarios
        finally:
            self.limpar_ambiente_teste(auth_service)

    def test_02_criar_usuario_existente(self):
        #Teste 2: Criar usuário que já existe retorna erro
        auth_service = self.criar_ambiente_teste()
        try:
            criar_conta("usuario_existente", "senha123")
            resultado = criar_conta("usuario_existente", "outrasenha")
            assert resultado == False
        finally:
            self.limpar_ambiente_teste(auth_service)

    def test_03_login_sucesso(self):
        #Teste 3: Login com usuário criado retorna sucesso
        auth_service = self.criar_ambiente_teste()
        try:
            criar_conta("usuariologin", "senha123")
            resultado = login("usuariologin", "senha123")
            assert resultado == True
        finally:
            self.limpar_ambiente_teste(auth_service)

    def test_04_login_usuario_inexistente(self):
        #Teste 4: Login com usuário que não existe retorna erro
        auth_service = self.criar_ambiente_teste()
        try:
            resultado = login("naoexiste", "senha123")
            assert resultado == False
        finally:
            self.limpar_ambiente_teste(auth_service)

    def test_05_login_senha_incorreta(self):
        #Teste 5: Login com senha incorreta retorna erro
        auth_service = self.criar_ambiente_teste()
        try:
            criar_conta("usuariosenha", "senha123")
            resultado = login("usuariosenha", "senhaerrada")
            assert resultado == False
        finally:
            self.limpar_ambiente_teste(auth_service)