from jogo.visao.visao_relatorio_batalha import VisaoRelatorioBatalha
import pygame

class ControladorRelatorioBatalha:
    def __init__(self, largura, altura, modelo_relatorio):
        self.modelo = modelo_relatorio
        self.visao = VisaoRelatorioBatalha(largura, altura)
        self.terminado = False

    def manipular_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_z or evento.key == pygame.K_RETURN:
                self.terminado = True

    def atualizar(self, dt):
        pass

    def desenhar(self, superficie):
        dados_relatorio = {
            'vitoria': self.modelo.vitoria,
            'poupado': self.modelo.poupado,
            'turnos': self.modelo.turnos_passados,
            'dano_causado': self.modelo.dano_causado,
            'dano_recebido': self.modelo.dano_recebido,
            'cura': self.modelo.vida_curada
        }

        self.visao.desenhar(superficie, dados_relatorio)