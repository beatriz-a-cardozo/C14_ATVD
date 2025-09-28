from Gasto import gasto
from datetime import date

class gasto_do_mes(gasto):
    def __init__(self, descricao: str, data: date, categoria: str, metodo: str, valor: float):
        super().__init__(descricao, data, categoria, metodo, valor)

    def __str__(self):
        return f"Gasto do mês: {self.descricao} - R${self.valor:.2f} - {self.data} - {self.categoria} - {self.metodo}"

    def get_mes_ano(self):
        #Retorna o mês e ano do gasto no formato 'MM/YYYY'
        return self.data.strftime("%m/%Y")

    def is_gasto_do_mes_corrente(self):
        #Verifica se o gasto é do mês atual
        hoje = date.today()
        return self.data.month == hoje.month and self.data.year == hoje.year