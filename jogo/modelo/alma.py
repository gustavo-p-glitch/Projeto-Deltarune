import random
from jogo.modelo.jogador import Jogador

class Alma:
    def __init__(self, jogadores: list[Jogador]):
        self.jogadores = jogadores
        self.invencivel = False
        self.temporizador_invencibilidade = 0
        self.duracao_invencibilidade = 60
        self.velocidade = 5
        self.estado = "vermelho"
        self.vel_y_azul = 0.0
        self.forca_pulo = -8
        self.gravidade_normal = 0.5
        self.gravidade_pulo_segurado = 0.2
        self.no_chao = False

    def mudar_cor(self, cor: str):
        if self.estado != cor:
            self.estado = cor
            self.vel_y_azul = 0
            self.no_chao = False

    def pular(self):
        if self.estado == "azul" and self.no_chao:
            self.vel_y_azul = self.forca_pulo
            self.no_chao = False

    @property
    def vida_atual(self):
        return sum(player.vida for player in self.jogadores if player.estou_vivo())

    def levei_dano(self, dano):
        if self.invencivel:
            return 0
        vivos = [j for j in self.jogadores if j.estou_vivo()]
        if not vivos:
            return 0
        # No Deltarune o golpe cai num membro aleatório da party
        # (antes era sempre o primeiro vivo, então o Kris apanhava sozinho).
        alvo = random.choice(vivos)
        dano_sofrido_real = alvo.levei_dano(dano)
        if dano_sofrido_real > 0:
            self.invencivel = True
            self.temporizador_invencibilidade = self.duracao_invencibilidade
        return dano_sofrido_real

    def atualizar_invencibilidade(self):
        if self.invencivel:
            self.temporizador_invencibilidade -= 1
            if self.temporizador_invencibilidade <= 0:
                self.invencivel = False
        return any(jogador.estou_vivo() for jogador in self.jogadores)