import os

# Raiz do projeto (pasta acima de jogo/). Usar caminhos absolutos faz o jogo
# funcionar mesmo rodando de outra pasta (ex: python Projeto/main.py).
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(RAIZ, "assets")
DADOS = os.path.join(RAIZ, "dados")

FONTE_PADRAO = "8bitoperator.ttf"


def caminho(*partes: str) -> str:
    """Caminho a partir da raiz do projeto."""
    return os.path.join(RAIZ, *partes)


def fonte(nome: str = FONTE_PADRAO) -> str:
    return os.path.join(ASSETS, "fontes", nome)


def imagem(nome: str) -> str:
    """Imagens soltas: alma, projéteis (assets/imagens/)."""
    return os.path.join(ASSETS, "imagens", nome)


def sprite(nome: str) -> str:
    """Sprites de personagens/inimigos: um PNG ou uma pasta de frames (assets/sprites/)."""
    return os.path.join(ASSETS, "sprites", nome)


def botao(nome: str) -> str:
    return os.path.join(ASSETS, "botoes", nome)


def audio(nome: str) -> str:
    return os.path.join(ASSETS, "audio", nome)


def dado(nome: str) -> str:
    """Arquivos JSON de dados (dados/)."""
    return os.path.join(DADOS, nome)
