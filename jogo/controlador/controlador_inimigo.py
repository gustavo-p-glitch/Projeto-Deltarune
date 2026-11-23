import pygame
from jogo.modelo.inimigo import Inimigo
from jogo.visao.visao_inimigo import VisaoInimigo

class ControladorInimigo(pygame.sprite.Sprite):
    def __init__(self, nome: str, vida: int, magia: int, atk: int, defn: int, loot_ouro: int, imagens: str,
                 pos=(400, 150)):
        super().__init__()
        self.__inimigo = Inimigo(nome, vida, magia, atk, defn, loot_ouro)
        self.visao = VisaoInimigo(imagens)
        self.rect = self.visao.imagem.get_rect(center=pos)
        self._vida_anterior = vida

    @property
    def modelo(self):
        return self.__inimigo

    def visao_carregar_animacao(self, pasta):
        self.visao.carregar_animacao(pasta)

    def visao_atualizar_animacao(self, dt):
        # Antes chamava a si mesmo -> RecursionError se alguém usasse.
        self.visao.atualizar_animacao(dt)

    def atualizar(self, dt):
        vida = self.__inimigo.vida
        if vida < self._vida_anterior:
            self.visao.registrar_dano(self._vida_anterior - vida, morreu=not self.__inimigo.estou_vivo())
        self._vida_anterior = vida

        self.visao.atualizar_efeitos(dt)
        if self.__inimigo.estou_vivo() and self.visao.frames:
            self.visao.atualizar_animacao(dt)

    def requisitar_desenho_visao(self, tela):
        self.visao.desenhar(tela, self.rect, transparente=self.__inimigo.foi_poupado,
                            vivo=self.__inimigo.estou_vivo())