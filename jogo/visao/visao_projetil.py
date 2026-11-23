import pygame
import os
from jogo import recursos


class VisaoProjetil:
    _cache = {}  # evita recarregar o mesmo PNG do disco a cada osso criado

    def __init__(self, imagem):
        self.imagem = self._carregar(imagem)

    @classmethod
    def _carregar(cls, imagem):
        if imagem in cls._cache:
            return cls._cache[imagem]

        caminho_imagem = recursos.imagem(imagem)
        superficie = None
        if os.path.exists(caminho_imagem):
            try:
                superficie = pygame.image.load(caminho_imagem).convert_alpha()
                # Recorta a borda transparente: o osso.png tem 33x100, mas o osso
                # visível é 9x71 — sem isso a hitbox ficava bem mais larga que o desenho.
                recorte = superficie.get_bounding_rect()
                if recorte.width and recorte.height:
                    superficie = superficie.subsurface(recorte).copy()
            except pygame.error:
                superficie = None

        if superficie is None:
            superficie = pygame.Surface((30, 30), pygame.SRCALPHA)
            if "osso" in imagem:
                superficie.fill((255, 255, 255))
            elif "spade" in imagem:
                superficie.fill((0, 0, 255))
            else:
                superficie.fill((255, 0, 0))

        cls._cache[imagem] = superficie
        return superficie

    def ajustar_tamanho(self, tamanho):
        largura, altura = tamanho
        img = self.imagem
        # Sprite vertical (osso) num projétil deitado -> gira antes de escalar.
        if largura > altura and img.get_height() > img.get_width():
            img = pygame.transform.rotate(img, 90)
        self.imagem = pygame.transform.scale(img, (largura, altura))

    def desenhar(self, superficie, projetil):
        if projetil.ativa:
            superficie.blit(self.imagem, projetil.rect)
