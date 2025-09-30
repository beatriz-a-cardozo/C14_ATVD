import pytest
from datetime import datetime
from unittest.mock import patch
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models.Usuario import Usuario


class TesteCalculos:

    def test_16_calculo_valor_restante_dia_setembro(self):
        #Teste 16: Cálculo de valor restante por dia em setembro
        usuario = Usuario("teste_setembro", "hash123", 300.0)

        #Mock para dia 15 de setembro
        with patch('src.models.Usuario.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 9, 15)

            valor_dia = usuario.valor_restante_por_dia()

            #Setembro tem 30 dias
            assert valor_dia == 20

    def test_17_saldo_negativo_alerta(self):
        #Teste 17: Saldo negativo mostra alerta
        usuario = Usuario("teste_negativo", "hash123", -100.0)

        #Mock da data para evitar problemas com divisão por zero
        with patch('src.models.Usuario.datetime') as mock_datetime:
            #Define uma data segura (dia 15 de setembro - não é o último dia do mês)
            mock_datetime.now.return_value = datetime(2025, 9, 15)
            mock_datetime.year = 2025
            mock_datetime.month = 9

            #Verifica se o saldo é negativo
            assert usuario.saldo < 0

            #Testa o cálculo de valor por dia com saldo negativo
            valor_dia = usuario.valor_restante_por_dia()

            #Com saldo negativo
            assert valor_dia == -6
            assert valor_dia < 0  # Confirmando que é negativo

    def test_19_valida_formato_data(self):
        #Teste 19: Validação de formato de data
        usuario = Usuario("teste_data", "hash123", 500.0)

        #Adiciona receita com data no formato certo
        data_valida = "30/09/2025"
        usuario.receitas.append({"origem": "Teste", "valor": 100.0, "data": data_valida})

        #Verifica se a data foi armazenada corretamente
        assert usuario.receitas[0]["data"] == data_valida
        assert len(usuario.receitas[0]["data"]) == 10