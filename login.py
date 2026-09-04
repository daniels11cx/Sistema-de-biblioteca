import json
from config import CADASTROS_FILE

def carregar_usuarios():
    try:
        with open(CADASTROS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def salvar_usuarios(dados):
    with open(CADASTROS_FILE, "w") as f:
        json.dump(dados, f, indent=4)

def criar_cadastro():
    usuarios = carregar_usuarios()

    username = input("Usuário: ")
    senha = input("Senha: ")

    for u in usuarios:
        if u["username"] == username:
            print("Usuário já existe")
            return

    novo_usuario = {
        "username": username,
        "password": senha,
        "tipo": "comum"  # 🔥 TODO mundo nasce comum
    }

    usuarios.append(novo_usuario)
    salvar_usuarios(usuarios)

    print("Cadastro criado com sucesso!")

def login():
    usuarios = carregar_usuarios()

    username = input("Usuário: ")
    senha = input("Senha: ")

    for u in usuarios:
        if u["username"] == username and u["password"] == senha:
            return u  # 🔥 retorna o OBJETO COMPLETO

    return None

def menu_login():
    while True:
        print("=== Biblioteca ===")
        print("1 - Login")
        print("2 - Criar cadastro")
        print("3 - Sair")

        try:
            opcao = int(input("> "))

            if opcao == 1:
                usuario = login()

                if usuario:
                    print("Login bem-sucedido!")
                    return usuario  # 🔥 IMPORTANTE

            elif opcao == 2:
                criar_cadastro()

            elif opcao == 3:
                return None

            else:
                print("Opção inválida")

        except ValueError:
            print("Digite um número")