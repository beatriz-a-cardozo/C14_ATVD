import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models.Usuario import Usuario


class TesteValidacoes:

    def test_09_persistencia_usuario_isolado(self):
        #Teste 9: Dados persistem em usuário isolado

        #Cria usuário do zero
        usuario = Usuario("usuario_persistente", "hash123", 1500.0)

        #Adiciona alguns dados
        usuario.receitas.append({"origem": "Salário", "valor": 1500.0, "data": "01/10/2025"})
        usuario.gastoFixo.append({
            "gasto": "Aluguel", "categoria": "Moradia", "metodo": "Débito",
            "valor": 800.0, "data": "05/10/2025", "periodo": 1
        })

        #Converte para dicionário (simulando salvamento)
        usuario_dict = usuario.para_diciionario()

        #Recria usuário a partir do dicionário (simulando carregamento)
        usuario_recriado = Usuario.de_dicionario(usuario_dict)

        #Verifica se os dados persistiram
        assert usuario_recriado.nomeDeUsuario == "usuario_persistente"
        assert usuario_recriado.saldo == 1500.0
        assert len(usuario_recriado.receitas) == 1
        assert len(usuario_recriado.gastoFixo) == 1

    def test_20_valida_campos_obrigatorios(self):
        #Teste 20: Validação de campos obrigatórios

        #Testa criação de usuário com dados mínimos
        usuario = Usuario("usuario_minimo", "hash123")

        # Verifica se campos obrigatórios existem
        assert hasattr(usuario, 'nomeDeUsuario')
        assert hasattr(usuario, 'senhaHash')
        assert hasattr(usuario, 'saldo')
        assert hasattr(usuario, 'receitas')
        assert hasattr(usuario, 'gastoFixo')
        assert hasattr(usuario, 'gastoDoMes')
        assert hasattr(usuario, 'fatura')

        #Verifica valores padrão
        assert usuario.nomeDeUsuario == "usuario_minimo"
        assert usuario.senhaHash == "hash123"
        assert usuario.saldo == 0.0
        assert usuario.receitas == []
        assert usuario.gastoFixo == []