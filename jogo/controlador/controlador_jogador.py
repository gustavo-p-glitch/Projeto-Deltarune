import pygame
from jogo.modelo.jogador import Jogador
from jogo.visao.visao_jogador import VisaoJogador

class ControladorJogador(pygame.sprite.Sprite):
    def __init__(self, nome: str, magia: int, atk: int, defn: int, imagem: str, vida: int, pos=(0, 0),
                 cor=(255, 255, 255), escala=None, velocidade_animacao=None):
        super().__init__()
        self.__jogador = Jogador(nome, magia, atk, defn, vida)
        self.visao = VisaoJogador(imagem, escala, velocidade_animacao)
        # pos = onde ficam os PÉS do personagem (assim sprites de alturas diferentes alinham)
        self.rect = self.visao.imagem.get_rect(midbottom=pos)
        self.pos = pos
        self.cor = cor  # cor do painel de HP e do nome

    @property
    def modelo(self):
        return self.__jogador

    def atualizar(self, dt):
        self.visao.atualizar(dt, self.__jogador.vida)

    def tomar_dano(self, dano: int):
        self.__jogador.levei_dano(dano)

    def jogador_vivo(self):
        return self.__jogador.estou_vivo()

    def jogador_curar(self, quantidade: int):
        self.__jogador.curar(quantidade)

    def jogador_conhecimento(self, acao):
        self.__jogador.aprender_habilidade(acao)

    def jogador_usar(self, nome_item):
        self.__jogador.usar_item(nome_item)

    def jogador_atualizar_status(self):
        self.__jogador.atualizar_status()

    def requisitar_desenho(self, tela):
        self.visao.desenhar(self.__jogador, self.rect, tela)