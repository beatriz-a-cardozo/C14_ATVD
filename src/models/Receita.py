from datetime import date
from pathlib import Path
import json

class Receita:
    def __init__(self, origem: str, valor: float, data: str):
        self.origem = origem
        self.valor = valor
        self.data = data

    def para_dicionario(self):
        return {
            "origem": self.origem,
            "valor": self.valor,
            "data": self.data
        }

    @classmethod
    def de_dicionario(cls, data):
        return cls(data["origem"], data["valor"], data["data"])