import pygame
from jogo import recursos

class VisaoAlma:
    def __init__(self):
        try:
            self.imagem = pygame.image.load(recursos.imagem("soul2.png")).convert_alpha()
        except (pygame.error, FileNotFoundError):
            self.imagem = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(self.imagem, (255, 0, 0), (10, 10), 10)

        try:
            self.imagem_azul = pygame.image.load(recursos.imagem("blue_soul.png")).convert_alpha()
        except (pygame.error, FileNotFoundError):
            self.imagem_azul = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(self.imagem_azul, (0, 0, 255), (10, 10), 10)

        try:
            self.som_dano = pygame.mixer.Sound(recursos.audio("damage.mp3"))
            self.som_dano.set_volume(0.5)
        except (pygame.error, FileNotFoundError):
            self.som_dano = None

    def tocar_som(self):
        if self.som_dano:
            self.som_dano.play()

    def desenhar(self, modelo, rect, superficie):
        imagem_para_desenhar = None
        if modelo.estado == "azul":
            imagem_para_desenhar = self.imagem_azul
        else:
            imagem_para_desenhar = self.imagem

        if modelo.invencivel:
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                superficie.blit(imagem_para_desenhar, rect)
        else:
            superficie.blit(imagem_para_desenhar, rect)