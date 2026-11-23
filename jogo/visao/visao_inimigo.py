import math
import pygame
import os
from jogo import recursos

class VisaoInimigo:
    def __init__(self, imagens:str):
        self.frames = []
        self.indice_frame = 0
        self.temporizador_animacao = 0
        self.velocidade_animacao = 120

        self.carregar_animacao(imagens)

        # Efeitos de dano: tremida + números subindo + fade ao morrer
        self.temporizador_tremida = 0
        self.numeros_dano = []  # [valor, tempo_restante]
        self.DURACAO_NUMERO = 900
        self.temporizador_morte = 0
        self.DURACAO_MORTE = 700
        try:
            self.fonte_dano = pygame.font.Font(recursos.fonte(), 34)
        except (pygame.error, FileNotFoundError):
            self.fonte_dano = pygame.font.Font(None, 40)

        if self.frames:
            self.imagem = self.frames[0]
        else:
            self.imagem = pygame.Surface((100, 100), pygame.SRCALPHA)
            self.imagem.fill((255, 0, 0))

    def carregar_animacao(self, pasta):
        pasta = recursos.sprite(pasta)
        if not os.path.isdir(pasta):
            return
        for arquivo in sorted(os.listdir(pasta)):
            if arquivo.lower().endswith(".png"):
                try:
                    img = pygame.image.load(os.path.join(pasta, arquivo)).convert_alpha()
                    self.frames.append(img)
                except pygame.error as e:
                    print(f"[aviso] frame '{arquivo}' ignorado: {e}")

    def atualizar_animacao(self, dt):
        self.temporizador_animacao += dt
        if self.temporizador_animacao >= self.velocidade_animacao:
            self.temporizador_animacao = 0
            self.indice_frame = (self.indice_frame + 1) % len(self.frames)
            self.imagem = self.frames[self.indice_frame]

    def registrar_dano(self, valor, morreu=False):
        self.temporizador_tremida = 400
        self.numeros_dano.append([valor, self.DURACAO_NUMERO])
        if morreu:
            self.temporizador_morte = self.DURACAO_MORTE

    def atualizar_efeitos(self, dt):
        self.temporizador_tremida = max(0, self.temporizador_tremida - dt)
        self.temporizador_morte = max(0, self.temporizador_morte - dt)
        for n in self.numeros_dano:
            n[1] -= dt
        self.numeros_dano = [n for n in self.numeros_dano if n[1] > 0]

    def desenhar(self, tela, rect, transparente=False, vivo=True):
        destino = rect.copy()
        if self.temporizador_tremida > 0:
            destino.x += round(math.sin(self.temporizador_tremida / 18) * self.temporizador_tremida / 50)

        if not vivo:
            if self.temporizador_morte > 0:
                img = self.imagem.copy()
                img.set_alpha(round(255 * self.temporizador_morte / self.DURACAO_MORTE))
                tela.blit(img, destino)
        elif transparente:
            img = self.imagem.copy()
            img.set_alpha(90)
            tela.blit(img, destino)
        else:
            tela.blit(self.imagem, destino)

        for valor, restante in self.numeros_dano:
            progresso = 1 - restante / self.DURACAO_NUMERO
            subida = min(1, progresso * 4) * 30  # sobe rápido e fica parado
            texto = self.fonte_dano.render(str(valor), False, (255, 70, 70))
            if progresso > 0.6:
                texto.set_alpha(round(255 * (1 - progresso) / 0.4))
            # Sobre o corpo do inimigo (acima dele não cabe: o inimigo fica no topo da tela)
            tela.blit(texto, texto.get_rect(midbottom=(rect.centerx + 50, rect.centery - subida)))
