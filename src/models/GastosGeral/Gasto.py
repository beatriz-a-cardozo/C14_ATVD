from datetime import date
from pathlib import Path
import json
from src.service.AutenticacaoService import get_usuario_atual

class gasto:
    def __init__(self, gasto: str, data: date, categoria: str, metodo: str, valor: float):
        self.gasto = gasto
        self.data = data
        self.categoria = categoria
        self.metodo = metodo
        self.valor = valor

    def __str__(self):
        return f"Gasto: {self.descricao} - R${self.valor:.2f} - {self.data} - {self.categoria} - {self.metodo}"

    #Métodos para manipulação de receitas
    @staticmethod
    def adicionar_receita(origem: str, valor: float, data: str):
        #Adiciona uma nova receita para o usuário atual
        usuario_atual = get_usuario_atual()
        arquivo_usuarios = Path("src/data/usuarios.json")

        if usuario_atual is None:
            return False

        #Carrega todos os usuários
        with open(arquivo_usuarios, "r") as f:
            usuarios_data = json.load(f)

        #Adiciona a receita ao usuário atual
        nova_receita = {
            "origem": origem,
            "valor": valor,
            "data": data
        }

        usuarios_data[usuario_atual.nome_de_usuario]["receitas"].append(nova_receita)
        usuarios_data[usuario_atual.nome_de_usuario]["saldo"] += valor

        #Atualiza o usuário atual
        usuario_atual.receitas.append(nova_receita)
        usuario_atual.saldo += valor

        #Salva no arquivo
        with open(arquivo_usuarios, "w") as f:
            json.dump(usuarios_data, f, indent = 4)

        return True

    @staticmethod
    def get_receitas_usuario():
        #Retorna todas as receitas do usuário atual
        from src.service.AutenticacaoService import get_usuario_atual

        usuario_atual = get_usuario_atual()

        if usuario_atual is None:
            return []

        return usuario_atual.receitas

    @staticmethod
    def get_total_receitas():
        #Retorna o total de receitas do usuário atual
        receitas = gasto.get_receitas_usuario()
        return sum(receita["valor"] for receita in receitas)


    ### Fluxo de funcionamento ###
    # gasto.adicionar_receita("Gasto exemplo", 500.00, "2023-10-20")
    #          ↓
    # Busca usuário logado
    #          ↓
    # Carrega arquivo JSON
    #          ↓
    # Adiciona receita nos dados
    #          ↓
    # Atualiza saldo
    #          ↓
    # Salva no arquivo JSON
    #          ↓
    # Retorna True / False