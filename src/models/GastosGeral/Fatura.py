from Gasto import Gasto
from datetime import date

class Fatura(Gasto):
    def __init__(self, gasto: str, data: date, categoria: str, metodo: str, valor: float, banco: str):
        super().__init__(gasto, data, categoria, metodo, valor)
        self.banco = banco

    def __str__(self):
        return f"Fatura: {self.gasto} - R${self.valor:.2f} - Banco: {self.banco}"