from Gasto import gasto
from datetime import date

class fatura(gasto):

    def __init__(self, descricao: str, data: date, categoria: str, metodo: str, valor: float, banco: str):
        super().__init__(descricao, data, categoria, metodo, valor)
        self.banco = banco

    def __str__(self):
        return f"Fatura: {self.descricao} - R${self.valor:.2f} - {self.data} - Banco: {self.banco}"