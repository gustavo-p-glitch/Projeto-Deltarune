"""Gera os sprites dos botões de batalha (estilo Undertale: moldura laranja, ícone + texto).

Rodar `python -m jogo.visao.gerador_botoes` (da raiz) salva os PNGs em assets/botoes/.
Se os PNGs não existirem,
a VisaoBatalha chama criar_botao() direto, então o jogo funciona de qualquer jeito.
Para personalizar: edite os PNGs à mão ou mude os ícones/cores abaixo e gere de novo.
"""
import os
import pygame
from jogo import recursos

TAMANHO_BOTAO = (170, 44)
COR_NORMAL = (255, 128, 0)
COR_SELECIONADO = (255, 255, 0)
ESCALA_ICONE = 2
POS_ICONE = (12, 9)  # canto do ícone dentro do botão (o coração fica aqui quando selecionado)

ICONES = {
    "lutar": [
        "...........##",
        "..........###",
        ".........###.",
        "........###..",
        ".......###...",
        "......###....",
        "..#..###.....",
        "...####......",
        "....##.......",
        "...####......",
        "..##..#......",
        ".##..........",
        "##...........",
    ],
    "agir": [
        ".............",
        ".###########.",
        "#...........#",
        "#.##.###.##.#",
        "#...........#",
        "#.####.####.#",
        "#...........#",
        ".####.######.",
        ".....#.#.....",
        "......##.....",
        ".......#.....",
        ".............",
        ".............",
    ],
    "item": [
        "....#####....",
        ".....#.#.....",
        "....##.##....",
        "...#.....#...",
        "..#.......#..",
        ".#.........#.",
        ".#....#....#.",
        ".#...###...#.",
        ".#....#....#.",
        ".#.........#.",
        ".#.........#.",
        "..#########..",
        ".............",
    ],
    "poupar": [
        "##...........",
        "######.......",
        "#.....####...",
        "#.........##.",
        "#..........#.",
        "#.........#..",
        "#.....###....",
        "######.......",
        "#............",
        "#............",
        "#............",
        "#............",
        "###..........",
    ],
}

TEXTOS = {"lutar": "LUTAR", "agir": "AGIR", "item": "ITEM", "poupar": "POUPAR"}

# Nome da opção no modelo -> nome do botão
MAPA_OPCOES = {"Ataque": "lutar", "Agir": "agir", "Item": "item", "Poupar": "poupar"}


def _fonte(tamanho):
    try:
        return pygame.font.Font(recursos.fonte(), tamanho)
    except (pygame.error, FileNotFoundError):
        return pygame.font.Font(None, tamanho)


def desenhar_icone(nome, cor):
    grade = ICONES[nome]
    largura, altura = len(grade[0]), len(grade)
    s = pygame.Surface((largura * ESCALA_ICONE, altura * ESCALA_ICONE), pygame.SRCALPHA)
    for y, linha in enumerate(grade):
        for x, c in enumerate(linha):
            if c == "#":
                s.fill(cor, (x * ESCALA_ICONE, y * ESCALA_ICONE, ESCALA_ICONE, ESCALA_ICONE))
    return s


def criar_botao(nome, selecionado=False):
    """Selecionado: amarelo e SEM ícone (o jogo desenha o coração da alma no lugar)."""
    cor = COR_SELECIONADO if selecionado else COR_NORMAL
    s = pygame.Surface(TAMANHO_BOTAO, pygame.SRCALPHA)
    s.fill((0, 0, 0))
    pygame.draw.rect(s, cor, s.get_rect(), 3)

    if not selecionado:
        s.blit(desenhar_icone(nome, cor), POS_ICONE)

    texto = _fonte(28).render(TEXTOS[nome], False, cor)
    inicio_texto = POS_ICONE[0] + 13 * ESCALA_ICONE + 6
    area = pygame.Rect(inicio_texto, 0, TAMANHO_BOTAO[0] - inicio_texto - 6, TAMANHO_BOTAO[1])
    s.blit(texto, texto.get_rect(center=area.center))
    return s


def salvar_todos(pasta="botoes"):
    destino = os.path.join(recursos.ASSETS, pasta)
    os.makedirs(destino, exist_ok=True)
    for nome in ICONES:
        pygame.image.save(criar_botao(nome, False), os.path.join(destino, f"{nome}.png"))
        pygame.image.save(criar_botao(nome, True), os.path.join(destino, f"{nome}_sel.png"))
    print(f"Botões salvos em {destino}")


if __name__ == "__main__":
    pygame.init()
    salvar_todos()
