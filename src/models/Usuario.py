class Usuario:

    def __init__(self, nomeDeUsuario: str, senhaHash: str):
        self.nomeDeUsuario = nomeDeUsuario
        self.senhaHash = senhaHash
        self.saldo = 0
        self.gastos = []
        self.receitas = []

    def para_diciionario(self) -> dict:
        return {
            "nome_de_usuario": self.nomeDeUsuario,
            "senha_hash": self.senhaHash,
            "saldo": self.saldo,
            "gastos": self.gastos,
            "receitas": self.receitas
        }

    @staticmethod
    def de_dicionario(data: dict):
        usuario = Usuario(data["nome_de_usuario"],data["senha_hash"])

        usuario.saldo = data["saldo"]
        usuario.receitas = data.get("receitas",[])
        usuario.gastos = data.get("gastos",[])

        return usuario