import json
from datetime import datetime
from config import HISTORICO_FILE

def carregar_historico():
    try:
        with open(HISTORICO_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def salvar_historico(dados):
    with open(HISTORICO_FILE, "w") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def registrar_acao(usuario, livro, acao):
    historico = carregar_historico()

    evento = {
        "usuario": usuario,
        "livro": livro,
        "acao": acao,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    historico.append(evento)
    salvar_historico(historico)