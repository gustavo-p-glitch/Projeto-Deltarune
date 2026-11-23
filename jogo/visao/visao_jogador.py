import math
import os
import pygame
from jogo import recursos


class VisaoJogador:
    """Sprite de um membro da party.

    Para trocar o visual, basta substituir o PNG (ex: kris.png) ou apontar para uma
    PASTA com vários PNGs (vira animação, em ordem alfabética). O espaço transparente
    em volta é recortado e o sprite é escalado por ESCALA, então o tamanho do canvas
    não importa — só a proporção entre os personagens.
    """

    ESCALA = 1.25
    VELOCIDADE_ANIMACAO = 150   # ms por frame
    DURACAO_FLASH_DANO = 450    # ms

    def __init__(self, imagem, escala=None, velocidade_animacao=None):
        # Pixel art feito em resolução pequena (ex: sprites/lume) fica melhor com escala inteira (3).
        self.escala = escala if escala is not None else self.ESCALA
        self.velocidade_animacao = velocidade_animacao or self.VELOCIDADE_ANIMACAO
        self.frames = self._carregar_frames(imagem)
        self.imagem = self.frames[0]
        self.indice_frame = 0
        self.tempo = 0
        self.temporizador_animacao = 0
        self.temporizador_dano = 0
        self.fase = hash(imagem) % 100 / 10  # cada personagem "respira" num ritmo diferente
        self._vida_anterior = None

    def _carregar_frames(self, imagem):
        alvo = recursos.sprite(imagem)
        arquivos = []
        if os.path.isdir(alvo):
            arquivos = [os.path.join(alvo, f) for f in sorted(os.listdir(alvo)) if f.lower().endswith(".png")]
        elif os.path.exists(alvo):
            arquivos = [alvo]

        frames = []
        for arq in arquivos:
            try:
                img = pygame.image.load(arq).convert_alpha()
            except pygame.error as e:
                print(f"[aviso] sprite '{arq}' ignorado: {e}")
                continue
            recorte = img.get_bounding_rect()
            if recorte.width and recorte.height:
                img = img.subsurface(recorte).copy()
            tamanho = (max(1, round(img.get_width() * self.escala)),
                       max(1, round(img.get_height() * self.escala)))
            frames.append(pygame.transform.scale(img, tamanho))  # scale (não smooth): mantém o pixel art

        if not frames:
            placeholder = pygame.Surface((60, 90), pygame.SRCALPHA)
            placeholder.fill((0, 0, 255))
            frames = [placeholder]
        return frames

    def atualizar(self, dt, vida_atual):
        self.tempo += dt
        if self._vida_anterior is not None and vida_atual < self._vida_anterior:
            self.temporizador_dano = self.DURACAO_FLASH_DANO
        self._vida_anterior = vida_atual
        self.temporizador_dano = max(0, self.temporizador_dano - dt)

        if len(self.frames) > 1:
            self.temporizador_animacao += dt
            if self.temporizador_animacao >= self.velocidade_animacao:
                self.temporizador_animacao = 0
                self.indice_frame = (self.indice_frame + 1) % len(self.frames)
                self.imagem = self.frames[self.indice_frame]

    def desenhar(self, modelo, rect, tela):
        img = self.imagem
        destino = img.get_rect(midbottom=rect.midbottom)

        if not modelo.estou_vivo():
            caido = img.copy()
            caido.set_alpha(70)
            tela.blit(caido, destino)
            return

        # "Respiração": sobe e desce 2px
        destino.y += round(math.sin(self.tempo / 350 + self.fase) * 2)

        if self.temporizador_dano > 0:
            destino.x += round(math.sin(self.tempo / 25) * 4)  # tremida
            if (self.temporizador_dano // 75) % 2 == 0:
                vermelho = img.copy()
                vermelho.fill((255, 60, 60, 255), special_flags=pygame.BLEND_RGBA_MULT)
                img = vermelho

        tela.blit(img, destino)
