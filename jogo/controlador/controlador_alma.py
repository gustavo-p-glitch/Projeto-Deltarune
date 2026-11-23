import pygame
from jogo.modelo.alma import Alma
from jogo.visao.visao_alma import VisaoAlma
from jogo.modelo.jogador import Jogador

class ControladorAlma(pygame.sprite.Sprite):
    def __init__(self, jogadores: list[Jogador]):
        super().__init__()
        self.modelo = Alma(jogadores)
        self.visao = VisaoAlma()
        self.rect = self.visao.imagem.get_rect()

    def atualizar_fisica(self, rect_battle_box: pygame.Rect, pulo_segurado: bool):
        if self.modelo.estado == "azul":
            if pulo_segurado and self.modelo.vel_y_azul < 0:
                self.modelo.vel_y_azul += self.modelo.gravidade_pulo_segurado
            else:
                self.modelo.vel_y_azul += self.modelo.gravidade_normal

            self.modelo.vel_y_azul = min(self.modelo.vel_y_azul, 7)
            self.rect.y += self.modelo.vel_y_azul

            if self.rect.bottom >= rect_battle_box.bottom:
                self.rect.bottom = rect_battle_box.bottom
                self.modelo.vel_y_azul = 0
                self.modelo.no_chao = True
            else:
                self.modelo.no_chao = False

            if self.rect.top <= rect_battle_box.top:
                self.rect.top = rect_battle_box.top
                self.modelo.vel_y_azul = 0

        return self.modelo.atualizar_invencibilidade()

    def mover(self, dx, dy, rect_battle_box: pygame.Rect):
        if self.modelo.velocidade == 0:
            return

        novo_x = self.rect.x + (dx * self.modelo.velocidade)
        self.rect.x = max(rect_battle_box.left, min(novo_x, rect_battle_box.right - self.rect.width))

        if self.modelo.estado == "vermelho":
            novo_y = self.rect.y + (dy * self.modelo.velocidade)
            self.rect.y = max(rect_battle_box.top, min(novo_y, rect_battle_box.bottom - self.rect.height))

    def pular(self):
        self.modelo.pular()

    def desenhar(self, superficie):
        self.visao.desenhar(self.modelo, self.rect, superficie)

    def tomar_dano(self, dano):
        dano_efetivo = self.modelo.levei_dano(dano)
        if dano_efetivo:
            self.visao.tocar_som()
        return dano_efetivo



