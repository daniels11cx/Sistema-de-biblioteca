import json
from datetime import datetime, timedelta
from util import carregar_historico_usuario, carregar_livros, salvar_livros, mostrar_livros, mostrar_livros_numerados, salvar_historico_usuario, calcular_multa
from historico import registrar_acao

# 🔥 ID SEGURO (não duplica mais)
def gerar_id(livros):
    if not livros:
        return 1
    return max(l["id"] for l in livros) + 1


def buscar_livro_por_id(livros, id_livro):
    for livro in livros:
        if livro["id"] == id_livro:
            return livro
    return None


def cadastrar_livro():
    livros = carregar_livros()

    titulo = input("Digite o título do livro: ").lower()
    autor = input("Digite o autor do livro: ").lower()

    try:
        ano = int(input("Digite o ano de publicação do livro: "))
    except ValueError:
        print("Ano inválido.")
        return

    # evitar duplicado
    for l in livros:
        if l["titulo"] == titulo and l["autor"] == autor and l["ano"] == ano:
            print("Livro já cadastrado.")
            return

    livro = {
        "id": gerar_id(livros),
        "titulo": titulo,
        "autor": autor,
        "ano": ano,
        "emprestado": False,
        "emprestado_por": None,
        "data_emprestimo": None,
        "data_devolucao": None
    }

    livros.append(livro)
    salvar_livros(livros)
    print("Livro cadastrado com sucesso!")


def listar_livros():
    livros = carregar_livros()

    if not livros:
        print("Nenhum livro cadastrado.")
        return

    mostrar_livros(livros)

def emprestar_livro(usuario_logado):
    livros = carregar_livros()

    disponiveis = [l for l in livros if not l.get("emprestado")]

    if not disponiveis:
        print("Nenhum livro disponível.")
        return

    mostrar_livros_numerados(disponiveis)

    try:
        escolha = int(input("Escolha o livro: "))

        if not (1 <= escolha <= len(disponiveis)):
            print("Número inválido.")
            return

        livro_selecionado = disponiveis[escolha - 1]
        livro_real = buscar_livro_por_id(livros, livro_selecionado["id"])

        if not livro_real:
            print("Erro interno: livro não encontrado.")
            return

        # 🔥 atualiza estado do livro
        livro_real["emprestado"] = True
        livro_real["emprestado_por"] = usuario_logado["username"]
        livro_real["data_emprestimo"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        livro_real["data_devolucao"] = (
            datetime.now() + timedelta(days=14)
        ).strftime("%Y-%m-%d %H:%M:%S")

        # 🔥 salva estado atualizado
        salvar_livros(livros)

        # 🔥 registra histórico (sem quebrar sistema se falhar)
        try:
            registrar_acao(
                usuario_logado["username"],
                livro_real["titulo"],
                "emprestimo"
            )
        except Exception:
            pass

        print("Livro emprestado com sucesso!")

    except ValueError:
        print("Entrada inválida.")

def devolver_livro(usuario_logado):
    livros = carregar_livros()

    meus = [l for l in livros if l.get("emprestado_por") == usuario_logado["username"]]

    if not meus:
        print("Você não possui livros emprestados.")
        return

    mostrar_livros_numerados(meus)

    try:
        escolha = int(input("Escolha o livro: "))

        if 1 <= escolha <= len(meus):
            livro_selecionado = meus[escolha - 1]

            livro_real = buscar_livro_por_id(livros, livro_selecionado["id"])

            if not livro_real:
                print("Erro interno.")
                return
            historico_usuario = carregar_historico_usuario()
            dias_atraso, multa = calcular_multa(livro_real)
            registro = {
                "usuario": usuario_logado["username"],
                "livro": livro_real["titulo"],
                "data_emprestimo": livro_real.get("data_emprestimo"),
                "data_devolucao_real": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "dias_atraso": dias_atraso,
                "multa": multa
                }
            historico_usuario.append(registro)
            salvar_historico_usuario(historico_usuario)

            livro_real["emprestado"] = False
            livro_real["emprestado_por"] = None
            livro_real["data_emprestimo"] = None
            livro_real["data_devolucao"] = None

            salvar_livros(livros)

            if multa > 0:
                print(f"⚠️ Livro devolvido com {dias_atraso} dia(s) de atraso")
                print(f"💰 Multa gerada: R${multa:.2f}")
            print("Livro devolvido com sucesso!")
        else:
            print("Número inválido.")

    except ValueError:
        print("Entrada inválida.")


def remover_livro():
    livros = carregar_livros()

    if not livros:
        print("Nenhum livro cadastrado.")
        return

    mostrar_livros_numerados(livros)

    try:
        escolha = int(input("Escolha o livro: "))

        if 1 <= escolha <= len(livros):
            livro = livros[escolha - 1]
            livros.remove(livro)

            salvar_livros(livros)
            print("Livro removido com sucesso!")
        else:
            print("Número inválido.")

    except ValueError:
        print("Entrada inválida.")


def estatisticas():
    livros = carregar_livros()

    total = len(livros)
    emprestados = sum(1 for l in livros if l.get("emprestado"))
    disponiveis = total - emprestados

    print(f"Total: {total}")
    print(f"Emprestados: {emprestados}")
    print(f"Disponíveis: {disponiveis}")


def editar_livro():
    livros = carregar_livros()

    mostrar_livros_numerados(livros)

    try:
        escolha = int(input("Escolha o livro: "))

        if 1 <= escolha <= len(livros):
            livro = livros[escolha - 1]

            novo_titulo = input("Novo título: ").strip().lower()
            novo_autor = input("Novo autor: ").strip().lower()

            if novo_titulo:
                livro["titulo"] = novo_titulo
            if novo_autor:
                livro["autor"] = novo_autor

            salvar_livros(livros)
            print("Livro editado com sucesso!")
        else:
            print("Número inválido.")

    except ValueError:
        print("Entrada inválida.")


def meus_emprestimos(usuario_logado):
    livros = carregar_livros()

    meus = [l for l in livros if l.get("emprestado_por") == usuario_logado["username"]]

    if not meus:
        print("Você não possui livros emprestados.")
        return

    print("Meus empréstimos:")
    mostrar_livros(meus)

def mostrar_historico_usuario(usuario_logado):
    historico = carregar_historico_usuario()

    meus_registros = [
        h for h in historico
        if h["usuario"] == usuario_logado["username"]
    ]

    if not meus_registros:
        print("Você ainda não possui histórico.")
        return

    print("=== Meu histórico de empréstimos ===")

    for h in meus_registros:
        print(
            f"Livro: {h['livro']} | "
            f"Emprestado: {h['data_emprestimo']} | "
            f"Devolvido: {h['data_devolucao_real']} | "
            f"Atraso: {h.get('dias_atraso', 0)} dia(s) | "
            f"Multa: R${h.get('multa', 0):.2f}"
        )