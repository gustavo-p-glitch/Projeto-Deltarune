import pygame
from jogo.controlador.controlador_batalha import ControladorBatalha
from jogo.controlador.controlador_selecao_inimigo import ControladorSelecaoInimigo
from jogo.controlador.controlador_relatorio_batalha import ControladorRelatorioBatalha
from jogo.persistencia.relatorio_dao import RelatorioDAO

class ControladorJogo:
    def __init__(self, largura_tela, altura_tela):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        self.tela = pygame.display.set_mode((largura_tela, altura_tela))
        pygame.display.set_caption("Deltarune")
        self.largura, self.altura = largura_tela, altura_tela
        self.relogio = pygame.time.Clock()
        self.executando = True
        self.estado_jogo = "ENEMY_SELECT"
        self.controlador_selecao_inimigo = ControladorSelecaoInimigo()
        self.controlador_batalha = None
        self.controlador_relatorio = None
        self.dao_relatorio = RelatorioDAO()

    def iniciar_batalha(self, info_inimigo: dict):
        self.controlador_batalha = ControladorBatalha(self.largura, self.altura, info_inimigo)
        self.estado_jogo = "BATTLE"
        self.controlador_selecao_inimigo = None
        self.controlador_batalha.iniciar_musica()

    def ir_para_relatorio(self, relatorio):
        try:
            self.dao_relatorio.adicionar(relatorio.para_dict())
        except OSError as e:
            print(f"[aviso] não foi possível salvar o relatório: {e}")

        self.controlador_batalha.parar_musica()

        self.controlador_relatorio = ControladorRelatorioBatalha(self.largura, self.altura, relatorio)
        self.estado_jogo = "BATTLE_REPORT"
        self.controlador_batalha = None

    def ir_para_menu_selecao(self):
        self.controlador_selecao_inimigo = ControladorSelecaoInimigo()
        self.estado_jogo = "ENEMY_SELECT"
        self.controlador_relatorio = None

    def executar(self):
        while self.executando:
            dt = self.relogio.tick(60)
            self.processar_frame(dt, pygame.event.get(), pygame.key.get_pressed())
            pygame.display.flip()

        pygame.quit()

    def processar_frame(self, dt, eventos, teclas_pressionadas):
        """Um frame do jogo. Separado do executar() para dar pra testar sem janela."""
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.executando = False

            if self.estado_jogo == "ENEMY_SELECT" and self.controlador_selecao_inimigo:
                self.controlador_selecao_inimigo.manipular_evento(evento)
            elif self.estado_jogo == "BATTLE" and self.controlador_batalha:
                self.controlador_batalha.manipular_evento(evento)
            elif self.estado_jogo == "BATTLE_REPORT" and self.controlador_relatorio:
                self.controlador_relatorio.manipular_evento(evento)

        if self.estado_jogo == "BATTLE" and self.controlador_batalha:
            self.controlador_batalha.manipular_teclas_pressionadas(teclas_pressionadas)

        if self.estado_jogo == "ENEMY_SELECT" and self.controlador_selecao_inimigo:
            self.controlador_selecao_inimigo.atualizar(dt)
            inimigo_selecionado = self.controlador_selecao_inimigo.obter_inimigo_selecionado()
            if inimigo_selecionado:
                self.iniciar_batalha(inimigo_selecionado)

        elif self.estado_jogo == "BATTLE" and self.controlador_batalha:
            self.controlador_batalha.atualizar(dt)
            modelo = self.controlador_batalha.modelo
            # Espera a mensagem final ficar na tela antes de trocar de cena.
            if modelo.batalha_encerrada:
                estado_batalha = modelo.estado_batalha
                relatorio = modelo.relatorio
                relatorio.vitoria = (estado_batalha == "VITORIA")
                self.ir_para_relatorio(relatorio)

        elif self.estado_jogo == "BATTLE_REPORT" and self.controlador_relatorio:
            self.controlador_relatorio.atualizar(dt)
            if self.controlador_relatorio.terminado:
                self.ir_para_menu_selecao()

        self.tela.fill((0, 0, 0))
        if self.estado_jogo == "ENEMY_SELECT" and self.controlador_selecao_inimigo:
            self.controlador_selecao_inimigo.desenhar(self.tela)
        elif self.estado_jogo == "BATTLE" and self.controlador_batalha:
            self.controlador_batalha.desenhar(self.tela)
        elif self.estado_jogo == "BATTLE_REPORT" and self.controlador_relatorio:
            self.controlador_relatorio.desenhar(self.tela)
