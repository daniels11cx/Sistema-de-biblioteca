from util import carregar_livros, salvar_livros, mostrar_livros

def filtrar_por_titulo():
    livros = carregar_livros()
    if not livros:
        print("Nenhum livro cadastrado.")
        return
    titulo = input("Digite o titulo do livro que deseja filtrar: ").lower()
    resultados = [livro for livro in livros if titulo in livro["titulo"].lower()]
    if resultados:
        print("Livros encontrados:")
        mostrar_livros(resultados)
    else:
        print("Nenhum livro encontrado com esse titulo.")

def filtrar_por_autor():
    livros = carregar_livros()
    if not livros:
        print("Nemnhum livro encontrado.")
        return
    autor = input("Digite o autor do livro que deseja filtrar: ").lower()
    resultados = [livro for livro in livros if autor in livro["autor"].lower()]
    if resultados:
        print("Livros encontrados:")
        mostrar_livros(resultados)
    else:
        print("Nenhum livro encontrado com esse autor.")

def filtrar_por_ano():
    livros = carregar_livros()
    if not livros:
        print("Nenhum livro cadastrado.")
        return
    try:
        ano = int(input("Digite o ano de publicação do livro que deseja filtrar: "))
        resultados = [livro for livro in livros if livro["ano"] == ano]
        if resultados:
            print("Livros encontrados:")
            mostrar_livros(resultados)
        else:
            print("Nenhum livro encontrado com esse ano de publicação.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")

def filtrar_por_disponibilidade():
    livros = carregar_livros()
    if not livros:
        print("Nenhum livro cadastrado.")
        return
    resultados = [livro for livro in livros if not livro["emprestado"]]
    if resultados:
        print("Livros disponíveis:")
        mostrar_livros(resultados)
    else:
        print("Nenhum livro disponível no momento.")

def menu_filtrar():
    while True:
        try:
            print("=== Filtrar Livros ===")
            print("1- Filtrar por título\n2- Filtrar por autor\n3- Filtrar por ano de publicação\n4- Livros disponíveis\n5- Voltar ao menu principal")
            opcao = int(input("Escolha uma opção: "))
            if opcao == 1:
                filtrar_por_titulo()
            elif opcao == 2:
                filtrar_por_autor()
            elif opcao == 3:
                filtrar_por_ano()
            elif opcao == 4:
                filtrar_por_disponibilidade()
            elif opcao == 5:
                break
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")
        