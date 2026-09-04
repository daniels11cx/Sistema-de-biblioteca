import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

CADASTROS_FILE = os.path.join(DATA_DIR, "cadastros.json")
LIVROS_FILE = os.path.join(DATA_DIR, "livros.json")
HISTORICO_FILE = os.path.join(DATA_DIR, "historico.json")
HISTORICO_USUARIO_FILE = os.path.join(DATA_DIR, "historico_usuario.json")