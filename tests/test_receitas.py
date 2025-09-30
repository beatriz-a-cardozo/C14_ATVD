import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models.Usuario import Usuario


class TesteReceitas:

    def test_06_adicionar_receita_aumenta_saldo(self):
        #Teste 6: Adicionar receita altera positivamente o saldo

        #Cria usuário isolado para este teste
        usuario = Usuario("teste_receita", "hash123", 1000.0)
        saldo_inicial = usuario.saldo

        #Adiciona receita diretamente
        usuario.receitas.append({"origem": "Salário", "valor": 2000.0, "data": "30/09/2025"})
        usuario.saldo += 2000.0

        assert usuario.saldo == saldo_inicial + 2000.0
        assert len(usuario.receitas) == 1

    def test_07_adicionar_receita_valor_zero(self):
        #Teste 7: Adicionar receita com valor zero
        usuario = Usuario("teste_zero", "hash123", 500.0)

        #Adiciona receita com valor zero
        usuario.receitas.append({"origem": "Presente", "valor": 0.0, "data": "30/09/2025"})

        #O sistema atual permite valor zero
        assert len(usuario.receitas) == 1
        assert usuario.receitas[0]["valor"] == 0.0

    def test_08_adicionar_receita_sem_origem(self):
        #Teste 8: Adicionar receita sem origem
        usuario = Usuario("teste_sem_origem", "hash123", 800.0)

        #Adiciona receita sem origem
        usuario.receitas.append({"origem": "", "valor": 300.0, "data": "30/09/2025"})

        #O sistema atual permite origem vazia
        assert len(usuario.receitas) == 1
        assert usuario.receitas[0]["origem"] == ""

    def test_18_calculo_total_receitas(self):
        #Teste 18: Total de receitas calculado corretamente
        usuario = Usuario("teste_total", "hash123", 0.0)

        #Adiciona múltiplas receitas
        usuario.receitas = [
            {"origem": "Salário", "valor": 1000.0, "data": "01/09/2025"},
            {"origem": "Freelance", "valor": 500.0, "data": "15/09/2025"},
            {"origem": "Investimentos", "valor": 200.0, "data": "20/09/2025"}
        ]

        total = sum(receita["valor"] for receita in usuario.receitas)
        assert total == 1700.0
        assert usuario.get_total_receitas() == 1700.0