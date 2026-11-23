import pygame

class BattleBox:
    def __init__(self, x, y, largura, altura):
        self.rect = pygame.Rect(x, y, largura, altura)

    def desenhar(self, superficie):
        pygame.draw.rect(superficie, (0, 0, 0), self.rect)
        pygame.draw.rect(superficie, (255, 255, 255), self.rect, 2)