from livros import (
    cadastrar_livro, listar_livros, emprestar_livro,
    devolver_livro, remover_livro, editar_livro,
    estatisticas, meus_emprestimos, mostrar_historico_usuario
)
from filtros import menu_filtrar
from login import menu_login


def menu(usuario_logado):

    if not usuario_logado:
        print("Erro: usuário não logado")
        return

    while True:
        print("\n=== BIBLIOTECA ===")
        print(f"Logado como: {usuario_logado['username']} ({usuario_logado['tipo']})")
        print("\n--- MENU ---")

        print("2 - Listar livros")
        print("4 - Emprestar livro")
        print("5 - Devolver livro")
        print("6 - Buscar livro")
        print("10 - Meus empréstimos")
        print("11 - Historico")
        print("0 - Sair")

        if usuario_logado["tipo"] == "admin":
            print("\n--- ADMIN ---")
            print("1 - Cadastrar livro")
            print("7 - Remover livro")
            print("8 - Estatísticas")
            print("9 - Editar livro")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "0":
            print("Saindo...")
            break

        elif opcao == "2":
            listar_livros()

        elif opcao == "4":
            emprestar_livro(usuario_logado)

        elif opcao == "5":
            devolver_livro(usuario_logado)

        elif opcao == "6":
            menu_filtrar()

        elif opcao == "10":
            meus_emprestimos(usuario_logado)

        elif opcao == "11":
            mostrar_historico_usuario(usuario_logado)

        elif opcao == "1":
            if usuario_logado["tipo"] == "admin":
                cadastrar_livro()
            else:
                print("❌ Apenas admin")

        elif opcao == "7":
            if usuario_logado["tipo"] == "admin":
                remover_livro()
            else:
                print("❌ Apenas admin")

        elif opcao == "8":
            if usuario_logado["tipo"] == "admin":
                estatisticas()
            else:
                print("❌ Apenas admin")

        elif opcao == "9":
            if usuario_logado["tipo"] == "admin":
                editar_livro()
            else:
                print("❌ Apenas admin")

        else:
            print("❌ Opção inválida")


if __name__ == "__main__":
    usuario_logado = menu_login()

    if usuario_logado is None:
        print("Login cancelado ou inválido")
    else:
        menu(usuario_logado)