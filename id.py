import json

ARQUIVO = "livros.json"

with open(ARQUIVO, "r") as f:
    livros = json.load(f)

for i, livro in enumerate(livros, start=1):
    livro["id"] = i

with open(ARQUIVO, "w") as f:
    json.dump(livros, f, indent=4)

print("Migração concluída!")