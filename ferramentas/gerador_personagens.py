"""Gera os sprites (pixel art) dos personagens originais da party: Lume e Grão.

Os desenhos são feitos com formas simples numa tela pequena (resolução "nativa" do
pixel art) e ganham contorno automático. O jogo amplia com escala inteira (x3), então
cada pixel daqui vira um bloco 3x3 na tela.

Rodar `python -m ferramentas.gerador_personagens` (da raiz) salva os frames em
assets/sprites/lume/ e assets/sprites/grao/.
Para mudar cores, é só mexer nas paletas abaixo e rodar de novo.
"""
import os
import pygame
from jogo import recursos

CONTORNO = (28, 20, 36)


def contornar(s, cor=CONTORNO):
    """Adiciona contorno de 1px em volta de tudo que não é transparente."""
    w, h = s.get_size()
    saida = s.copy()
    for y in range(h):
        for x in range(w):
            if s.get_at((x, y)).a:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and s.get_at((nx, ny)).a:
                    saida.set_at((x, y), cor)
                    break
    return saida


def px(s, cor, *pontos):
    for p in pontos:
        s.set_at(p, cor)


# ---------------------------------------------------------------------- LUME
# Mariposa pequena com capa e lanterna. Equilibrada (ex-slot do Kris).
PALETA_LUME = {
    "asa": (230, 200, 140), "asa_sombra": (190, 156, 100), "mancha": (236, 132, 52),
    "pelo": (250, 246, 232), "pelo_sombra": (214, 204, 186),
    "olho": (24, 20, 34), "brilho_olho": (255, 255, 255),
    "capa": (44, 118, 128), "capa_sombra": (28, 82, 92), "botas": (60, 44, 40),
    "lanterna": (120, 84, 46), "luz": (255, 214, 84), "luz_forte": (255, 246, 176),
    "antena": (226, 204, 160), "borda": (120, 96, 70),
}


def desenhar_lume(frame=0):
    c = PALETA_LUME
    s = pygame.Surface((30, 31), pygame.SRCALPHA)
    ox, oy = 3, 1  # margem para o contorno e para as asas abertas
    asa_y = -1 if frame == 1 else 0  # asas batem levemente

    # Asas inferiores (atrás)
    pygame.draw.ellipse(s, c["asa_sombra"], (ox - 2, oy + 15 + asa_y, 8, 8))
    pygame.draw.ellipse(s, c["asa_sombra"], (ox + 16, oy + 15 + asa_y, 8, 8))
    # Asas superiores, abertas para os lados
    pygame.draw.ellipse(s, c["asa"], (ox - 3, oy + 4 + asa_y, 11, 14))
    pygame.draw.ellipse(s, c["asa"], (ox + 14, oy + 4 + asa_y, 11, 14))
    pygame.draw.ellipse(s, c["asa_sombra"], (ox - 3, oy + 12 + asa_y, 9, 6))
    pygame.draw.ellipse(s, c["asa_sombra"], (ox + 16, oy + 12 + asa_y, 9, 6))
    # Manchas "olho" nas asas
    pygame.draw.ellipse(s, c["mancha"], (ox - 2, oy + 7 + asa_y, 4, 4))
    pygame.draw.ellipse(s, c["mancha"], (ox + 20, oy + 7 + asa_y, 4, 4))
    px(s, c["olho"], (ox - 1, oy + 8 + asa_y), (ox + 21, oy + 8 + asa_y))

    # Capa (corpo)
    pygame.draw.polygon(s, c["capa"], [(ox + 7, oy + 15), (ox + 14, oy + 15), (ox + 16, oy + 26), (ox + 5, oy + 26)])
    pygame.draw.polygon(s, c["capa_sombra"], [(ox + 11, oy + 16), (ox + 14, oy + 15), (ox + 16, oy + 26), (ox + 12, oy + 26)])
    # Botas
    pygame.draw.rect(s, c["botas"], (ox + 6, oy + 26, 4, 2))
    pygame.draw.rect(s, c["botas"], (ox + 12, oy + 26, 4, 2))

    # Gola fofa
    pygame.draw.ellipse(s, c["pelo_sombra"], (ox + 5, oy + 13, 12, 5))
    pygame.draw.ellipse(s, c["pelo"], (ox + 5, oy + 12, 12, 4))

    # Cabeça (com borda fina para não se misturar com as asas)
    pygame.draw.ellipse(s, c["borda"], (ox + 4, oy + 3, 14, 12))
    pygame.draw.ellipse(s, c["pelo"], (ox + 5, oy + 4, 12, 10))
    pygame.draw.ellipse(s, c["pelo_sombra"], (ox + 11, oy + 9, 6, 5))
    pygame.draw.ellipse(s, c["pelo"], (ox + 5, oy + 4, 10, 9))

    # Olhos grandes
    pygame.draw.ellipse(s, c["olho"], (ox + 6, oy + 7, 4, 5))
    pygame.draw.ellipse(s, c["olho"], (ox + 12, oy + 7, 4, 5))
    px(s, c["brilho_olho"], (ox + 7, oy + 8), (ox + 13, oy + 8))

    # Antenas plumosas
    for base, ponta, lado in (((ox + 8, oy + 4), (ox + 5, oy + 0), -1), ((ox + 13, oy + 4), (ox + 16, oy + 0), 1)):
        pygame.draw.line(s, c["antena"], base, ponta)
        px(s, c["antena"], (ponta[0] + lado, ponta[1] + 1), (ponta[0] + 2 * lado, ponta[1] + 1),
           (base[0] - lado * 1, base[1] - 2))

    # Braço + lanterna (lado direito)
    pygame.draw.line(s, c["capa_sombra"], (ox + 15, oy + 18), (ox + 19, oy + 19))
    pygame.draw.line(s, c["lanterna"], (ox + 20, oy + 17), (ox + 20, oy + 19))
    pygame.draw.rect(s, c["lanterna"], (ox + 18, oy + 19, 5, 7))
    luz = c["luz_forte"] if frame == 1 else c["luz"]
    pygame.draw.rect(s, luz, (ox + 19, oy + 20, 3, 5))
    px(s, c["luz_forte"], (ox + 20, oy + 22))

    return contornar(s)


# ---------------------------------------------------------------------- GRÃO
# Golem de pedra com musgo e marreta. Tanque (ex-slot da Susie).
PALETA_GRAO = {
    "pedra": (138, 136, 150), "pedra_luz": (178, 176, 190), "pedra_sombra": (96, 94, 112),
    "rachadura": (64, 62, 78), "musgo": (96, 168, 76), "musgo_sombra": (62, 116, 54),
    "flor": (246, 140, 170), "olho": (110, 220, 255), "olho_forte": (190, 246, 255),
    "cabo": (140, 92, 52), "marreta": (104, 70, 42), "marreta_luz": (156, 110, 66),
}


def desenhar_grao(frame=0):
    c = PALETA_GRAO
    s = pygame.Surface((33, 27), pygame.SRCALPHA)
    ox, oy = 1, 1

    # Marreta apoiada (atrás do braço direito)
    pygame.draw.line(s, c["cabo"], (ox + 27, oy + 19), (ox + 28, oy + 5), 2)
    pygame.draw.rect(s, c["marreta"], (ox + 24, oy + 0, 8, 5))
    pygame.draw.rect(s, c["marreta_luz"], (ox + 24, oy + 0, 8, 2))

    # Pernas
    pygame.draw.rect(s, c["pedra_sombra"], (ox + 7, oy + 20, 6, 5))
    pygame.draw.rect(s, c["pedra_sombra"], (ox + 16, oy + 20, 6, 5))

    # Corpo (rochedo)
    pygame.draw.ellipse(s, c["pedra_sombra"], (ox + 3, oy + 5, 23, 18))
    pygame.draw.ellipse(s, c["pedra"], (ox + 3, oy + 4, 22, 16))
    pygame.draw.ellipse(s, c["pedra_luz"], (ox + 6, oy + 6, 9, 5))

    # Braços
    pygame.draw.ellipse(s, c["pedra"], (ox + 0, oy + 10, 6, 10))
    pygame.draw.ellipse(s, c["pedra_sombra"], (ox + 0, oy + 15, 6, 5))
    pygame.draw.ellipse(s, c["pedra"], (ox + 23, oy + 10, 6, 10))
    pygame.draw.ellipse(s, c["pedra_sombra"], (ox + 23, oy + 15, 6, 5))

    # Rachaduras
    pygame.draw.lines(s, c["rachadura"], False, [(ox + 18, oy + 15), (ox + 20, oy + 17), (ox + 19, oy + 19)])
    pygame.draw.lines(s, c["rachadura"], False, [(ox + 7, oy + 15), (ox + 9, oy + 16)])

    # Musgo no topo
    pygame.draw.ellipse(s, c["musgo_sombra"], (ox + 5, oy + 2, 18, 7))
    pygame.draw.ellipse(s, c["musgo"], (ox + 5, oy + 1, 18, 6))
    for x, comp in ((7, 2), (11, 3), (16, 2), (20, 2)):  # "gotas" de musgo escorrendo
        pygame.draw.line(s, c["musgo_sombra"], (ox + x, oy + 6), (ox + x, oy + 6 + comp))
    px(s, c["flor"], (ox + 16, oy + 2), (ox + 17, oy + 1), (ox + 18, oy + 2), (ox + 17, oy + 3))
    px(s, (255, 230, 120), (ox + 17, oy + 2))

    # Olhos brilhando (frame 2 = brilho mais forte, frame 3 = piscando)
    if frame == 2:
        pygame.draw.line(s, c["rachadura"], (ox + 10, oy + 11), (ox + 12, oy + 11))
        pygame.draw.line(s, c["rachadura"], (ox + 16, oy + 11), (ox + 18, oy + 11))
    else:
        cor = c["olho_forte"] if frame == 1 else c["olho"]
        pygame.draw.rect(s, cor, (ox + 10, oy + 10, 3, 2))
        pygame.draw.rect(s, cor, (ox + 16, oy + 10, 3, 2))

    return contornar(s)


# Sequência de frames de cada personagem (índices passados para a função de desenho)
SEQUENCIAS = {
    "lume": (desenhar_lume, [0, 1]),
    "grao": (desenhar_grao, [0, 1, 0, 1, 0, 2]),
}


def salvar_todos(pasta="sprites"):
    for nome, (funcao, frames) in SEQUENCIAS.items():
        destino = os.path.join(recursos.ASSETS, pasta, nome)
        os.makedirs(destino, exist_ok=True)
        for antigo in os.listdir(destino):
            if antigo.endswith(".png"):
                os.remove(os.path.join(destino, antigo))
        for i, frame in enumerate(frames):
            pygame.image.save(funcao(frame), os.path.join(destino, f"{i:02d}.png"))
    print(f"Sprites salvos em {os.path.join(recursos.ASSETS, pasta)}")


if __name__ == "__main__":
    pygame.init()
    salvar_todos()
