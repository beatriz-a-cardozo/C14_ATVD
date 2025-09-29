from Gasto import Gasto
from datetime import date

class GastoFixo(Gasto):
    def __init__(self, gasto: str, data: date, categoria: str, metodo: str, valor: float, periodo: int):
        super().__init__(gasto, data, categoria, metodo, valor)
        self.periodo = periodo

    def __str__(self):
        return f"Gasto Fixo: {self.gasto} - R${self.valor:.2f} - Recorrência: {self.periodo} dias"