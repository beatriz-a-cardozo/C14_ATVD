from src.service.AutenticacaoService import get_usuario_atual
from datetime import date
from pathlib import Path
import json

class Receita:
    def __init__(self, origem: str, valor: float, data: str):
        self.origem = origem
        self.valor = valor
        self.data = data

    @staticmethod
    def adicionar_receita(self,origem: str, valor: float, data: str):
        # Adiciona uma nova receita para o usuário atual
        usuario_atual = get_usuario_atual()
        arquivo_usuarios = Path("src/data/usuarios.json")

        if usuario_atual is None:
            return False

        # Carrega todos os usuários
        with open(arquivo_usuarios, "r") as f:
            usuarios_info = json.load(f)

        # Adiciona a receita ao usuário atual
        nova_receita = {
            "origem": origem,
            "valor": valor,
            "data": data
        }

        usuarios_info[usuario_atual.nome_de_usuario]["receitas"].append(nova_receita)
        usuarios_info[usuario_atual.nome_de_usuario]["saldo"] += valor

        # Atualiza o usuário atual
        usuario_atual.receitas.append(nova_receita)
        usuario_atual.saldo += valor

        # Salva no arquivo
        with open(arquivo_usuarios, "w") as f:
            json.dump(usuarios_info, f, indent=4)

        return True

    @staticmethod
    def get_receitas_usuario(self):
        # Retorna todas as receitas do usuário atual
        usuario_atual = get_usuario_atual()

        if usuario_atual is None:
            return []

        return usuario_atual.receitas

    @staticmethod
    def get_total_receitas(self):
        # Retorna o total de receitas do usuário atual
        receitas = self.get_receitas_usuario()
        return sum(receita["valor"] for receita in receitas)