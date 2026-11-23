import pygame
import os
from jogo import recursos

class VisaoRelatorioBatalha:
    def __init__(self, largura_tela, altura_tela):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

        try:
            caminho_fonte = recursos.fonte()
            self.fonte_titulo = pygame.font.Font(caminho_fonte, 48)
            self.fonte_stats = pygame.font.Font(caminho_fonte, 32)
            self.fonte_prompt = pygame.font.Font(caminho_fonte, 24)
        except Exception:
            self.fonte_titulo = pygame.font.Font(None, 48)
            self.fonte_stats = pygame.font.Font(None, 32)
            self.fonte_prompt = pygame.font.Font(None, 24)

    def desenhar(self, superficie: pygame.Surface, dados: dict):
        if dados.get('poupado'):
            texto_titulo = "POUPADO!"
        else:
            texto_titulo = "VITÓRIA!" if dados.get('vitoria') else "DERROTA"
        cor_titulo = (0, 255, 0) if dados.get('vitoria') else (255, 0, 0)

        titulo_surf = self.fonte_titulo.render(texto_titulo, True, cor_titulo)
        titulo_rect = titulo_surf.get_rect(center=(self.largura_tela / 2, 100))
        superficie.blit(titulo_surf, titulo_rect)

        stats = [
            f"Turnos Passados: {dados.get('turnos', 0)}",
            f"Dano Causado: {dados.get('dano_causado', 0)}",
            f"Dano Recebido: {dados.get('dano_recebido', 0)}",
            f"Vida Curada: {dados.get('cura', 0)}"
        ]

        y_pos_stats = 180
        for i, texto_stat in enumerate(stats):
            stat_surf = self.fonte_stats.render(texto_stat, True, (255, 255, 255))
            stat_rect = stat_surf.get_rect(center=(self.largura_tela / 2, y_pos_stats + i * 40))
            superficie.blit(stat_surf, stat_rect)

        prompt_surf = self.fonte_prompt.render("Pressione [Z] para continuar", True, (150, 150, 150))
        prompt_rect = prompt_surf.get_rect(center=(self.largura_tela / 2, self.altura_tela - 100))
        superficie.blit(prompt_surf, prompt_rect)