from datetime import date
from pathlib import Path
import json
#from src.service.AutenticacaoService import get_usuario_atual

class Gasto:
    def __init__(self, gasto: str, data: date, categoria: str, metodo: str, valor: float):
        self.gasto = gasto
        self.data = data
        self.categoria = categoria
        self.metodo = metodo
        self.valor = valor
        self.usuario_atual = get_usuario_atual()