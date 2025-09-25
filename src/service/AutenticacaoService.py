import hashlib
import json
from pathlib import Path
from src.models.Usuario import Usuario

arquivo = Path("src/data/usuarios.json")

# ==================================================== CRIAR CONTA ====================================================
def criar_conta(nomeDeUsuario: str, senha: str) -> bool:

    usuarios = checar_usarios()

    if nomeDeUsuario in usuarios:
        return False

    novoUsuario = Usuario(nomeDeUsuario, hashlib.sha256(senha.encode()).hexdigest())

    usuarios[nomeDeUsuario] = novoUsuario
    salvar_usuario(usuarios)

    return True

# ======================================================= LOGIN =======================================================
def login(nomeDeUsuario: str, senha: str) -> bool:

    usuarios = checar_usarios()

    if nomeDeUsuario in usuarios:
        return False

    return hashlib.sha256(senha.encode()).hexdigest() == usuarios[nomeDeUsuario].senhaHash

# ================================================ MÉTODOS AUXILIARES =================================================
def checar_usarios(): # retorna um dicionario com todos os usuarios

    if arquivo.exists():
        with open(arquivo,"r") as arq:
            raw = json.load(arq)

        return {
            user: Usuario.de_dicionario(data) for user,data in raw.items()
        }

    return {}

def salvar_usuario(usuarios: dict[str,Usuario]): # salca o usuario criado no dicionario e transforma em json

    serial = {
        user: u.para_diciionario() for user,u in usuarios.items()
    } # serialização

    with open(arquivo,"w") as arq:
        json.dump(serial,arq,indent=4)

