from Gasto import Gasto
from datetime import date

class GastoDoMes(Gasto):
    def __init__(self, gasto: str, data: date, categoria: str, metodo: str, valor: float, periodo: int):
        super().__init__(gasto, data, categoria, metodo, valor)
        self.periodo = periodo

    def para_dicionario(self):
        return {
            "gasto": self.gasto,
            "data": self.data.isoformat(),
            "categoria": self.categoria,
            "metodo": self.metodo,
            "valor": self.valor,
            "periodo": self.periodo
        }

    @classmethod
    def de_dicionario(cls, data):
        return cls(
            data["gasto"],
            date.fromisoformat(data["data"]),
            data["categoria"],
            data["metodo"],
            data["valor"],
            data["periodo"]
        )