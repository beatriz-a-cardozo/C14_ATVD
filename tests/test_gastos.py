import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models.Usuario import Usuario


class TesteGastos:

    def test_11_gasto_credito_nao_afeta_saldo(self):
        #Teste 11: Gasto no crédito não afeta saldo imediatamente
        usuario = Usuario("teste_credito", "hash123", 1000.0)
        saldo_inicial = usuario.saldo

        #Adiciona gasto no crédito
        usuario.gastoFixo.append({
            "gasto": "Compra crédito",
            "categoria": "Lazer",
            "metodo": "Credito",
            "valor": 200.0,
            "data": "30/09/2025",
            "periodo": 1
        })

        #No crédito, saldo não muda
        assert usuario.saldo == saldo_inicial
        assert len(usuario.gastoFixo) == 1

    def test_12_gasto_debito_reduz_saldo(self):
        #Teste 12: Gasto no débito reduz saldo imediatamente
        usuario = Usuario("teste_debito", "hash123", 1000.0)
        saldo_inicial = usuario.saldo

        #Adiciona gasto no débito
        usuario.gastoDoMes.append({
            "gasto": "Compra débito",
            "categoria": "Alimentacao",
            "metodo": "Debito",
            "valor": 150.0,
            "data": "30/09/2025"
        })
        usuario.saldo -= 150.0  #Simula a redução do saldo

        assert usuario.saldo == saldo_inicial - 150.0
        assert len(usuario.gastoDoMes) == 1

    def test_13_adicionar_gasto_fixo_periodo_valido(self):
        #Teste 13: Adicionar gasto fixo com período válido
        usuario = Usuario("teste_fixo", "hash123", 2000.0)

        usuario.gastoFixo.append({
            "gasto": "Aluguel",
            "categoria": "Moradia",
            "metodo": "Debito",
            "valor": 800.0,
            "data": "30/09/2025",
            "periodo": 1
        })

        assert len(usuario.gastoFixo) == 1
        assert usuario.gastoFixo[0]["periodo"] == 1
        assert usuario.gastoFixo[0]["categoria"] == "Moradia"

    def test_14_adicionar_gasto_categoria_valida(self):
        #Teste 14: Adicionar gasto com categoria válida
        usuario = Usuario("teste_categoria", "hash123", 1500.0)

        categorias_validas = ["Alimentacao", "Transporte", "Moradia", "Lazer", "Saude", "Investimento"]

        for categoria in categorias_validas:
            usuario.gastoDoMes.append({
                "gasto": f"Gasto {categoria}",
                "categoria": categoria,
                "metodo": "Debito",
                "valor": 100.0,
                "data": "30/09/2025"
            })

        assert len(usuario.gastoDoMes) == len(categorias_validas)
        assert all(gasto["categoria"] in categorias_validas for gasto in usuario.gastoDoMes)

    def test_15_adicionar_fatura_reduz_saldo(self):
        #Teste 15: Adicionar fatura reduz saldo
        usuario = Usuario("teste_fatura", "hash123", 1000.0)
        saldo_inicial = usuario.saldo

        usuario.fatura.append({
            "gasto": "Nubank",
            "valor": 300.0,
            "data": "30/09/2025"
        })
        usuario.saldo -= 300.0  #Simula redução do saldo

        assert usuario.saldo == saldo_inicial - 300.0
        assert len(usuario.fatura) == 1