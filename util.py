import json
from datetime import datetime
from config import LIVROS_FILE, HISTORICO_USUARIO_FILE

def carregar_historico_usuario():
    try:
        with open(HISTORICO_USUARIO_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
def salvar_historico_usuario(dados):
    with open(HISTORICO_USUARIO_FILE, "w") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_livros():
    try:
        with open(LIVROS_FILE, "r") as arquivo_json:
            livros = json.load(arquivo_json)

            for livro in livros:
                livro.setdefault("emprestado_por", None)
                livro.setdefault("data_emprestimo", None)
                livro.setdefault("data_devolucao", None)

            return livros

    except FileNotFoundError:
        return []
    
def salvar_livros(livros):
    with open(LIVROS_FILE, "w") as arquivo_json:
        json.dump(livros, arquivo_json, indent=4, ensure_ascii=False)

def mostrar_livro(livro):
    status = "Emprestado" if livro["emprestado"] else "Disponível"

    texto = (
        f"{livro['titulo']} - {livro['autor']} "
        f"({livro['ano']}) - {status}"
    )

    if livro.get("emprestado_por"):
        texto += f" - Emprestado por: {livro['emprestado_por']}"

    if livro.get("data_emprestimo"):
        texto += f" - Data de empréstimo: {livro['data_emprestimo']}"

    if livro.get("data_devolucao"):
        texto += f" - Data de devolução: {livro['data_devolucao']}"

    dias_atraso, multa = calcular_multa(livro)

    if dias_atraso > 0:
        texto += (
            f" - ⚠️ ATRASADO {dias_atraso} dia(s)"
            f" - 💰 Multa: R${multa:.2f}"
        )

    print(texto)

def mostrar_livros(livros):
    for livro in livros:
        mostrar_livro(livro)

def mostrar_livros_numerados(livros):
    for i, livro in enumerate(livros, start=1):
        status = "Emprestado" if livro["emprestado"] else "Disponível"

        texto = (
            f"{i}. {livro['titulo']} - {livro['autor']} "
            f"({livro['ano']}) - {status}"
        )

        if livro.get("emprestado_por"):
            texto += f" - Emprestado por: {livro['emprestado_por']}"

        if livro.get("data_emprestimo"):
            texto += f" - Empréstimo: {livro['data_emprestimo']}"

        if livro.get("data_devolucao"):
            texto += f" - Devolver até: {livro['data_devolucao']}"

        print(texto)

def calcular_multa(livro):
    if not livro.get("data_devolucao"):
        return 0, 0

    data_devolucao = datetime.strptime(
        livro["data_devolucao"],
        "%Y-%m-%d %H:%M:%S"
    )

    if datetime.now() <= data_devolucao:
        return 0, 0

    dias_atraso = (datetime.now() - data_devolucao).days
    multa = dias_atraso * 1

    return dias_atraso, multa