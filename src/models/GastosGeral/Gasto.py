from datetime import date
from pathlib import Path
import json

class Gasto:
    def __init__(self, gasto: str, data: date, categoria: str, metodo: str, valor: float):
        self.gasto = gasto
        self.data = data
        self.categoria = categoria
        self.metodo = metodo
        self.valor = valor

    def para_dicionario(self):
        return {
            "gasto": self.gasto,
            "data": self.data.isoformat(),
            "categoria": self.categoria,
            "metodo": self.metodo,
            "valor": self.valor
        }

    @classmethod
    def de_dicionario(cls, data):
        return cls(
            data["gasto"],
            date.fromisoformat(data["data"]),
            data["categoria"],
            data["metodo"],
            data["valor"]
        )