from Gasto import gasto
from datetime import date

class gasto_fixo(gasto):

    def __init__(self, descricao: str, data: date, categoria: str, metodo: str, valor: float, periodo: int):
        super().__init__(descricao, data, categoria, metodo, valor)
        self.periodo = periodo  #Período em dias do gato fixo

    def __str__(self):
        return f"Gasto fixo: {self.descricao} - R${self.valor:.2f} - {self.data} - Recorrência: {self.periodo} dias"