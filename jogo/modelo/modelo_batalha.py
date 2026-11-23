import pygame.rect
from jogo.modelo.alma import Alma
from jogo.modelo.modelo_menu import ModeloMenu
from jogo.modelo.jogador import Jogador
from jogo.modelo.inimigo import Inimigo
from jogo.modelo.relatorio_batalha import RelatorioBatalha
from jogo.modelo.sequenciador_ataque import SequenciadorDeAtaque
from jogo.persistencia.ataque_dao import AtaqueDAO

class ModeloBatalha:
    def __init__(self, jogadores: list[Jogador], inimigos: list[Inimigo],
                 modelo_alma: Alma, rect_battle_box: pygame.Rect,
                 rect_alma_inicial: pygame.Rect,
                 acoes_menu_principal: list
                 ):

        self.jogadores = jogadores
        self.inimigos = inimigos
        self.alma = modelo_alma
        self.rect_alma = rect_alma_inicial
        self.rect_battle_box = rect_battle_box
        self.relatorio = RelatorioBatalha(inimigos[0].nome if inimigos else "")
        self.projeteis = []
        self.projeteis_novos = []
        self.estado_batalha = "PLAYER_SELECT"
        self.indice_jogador_atual = 0
        self.jogador_atual = self.jogadores[self.indice_jogador_atual]
        self.menu_principal = ModeloMenu(acoes_menu_principal)
        self.menu_agir = None
        self.menu_item = None
        self.menu_ativo = self.menu_principal
        self.acoes_jogadores_turno = []
        self.indice_sequencia_acao = 0
        self.temporizador_acao = 0
        # Tempo que cada texto fica na caixa: base + um pouco por caractere,
        # pra dar tempo do efeito de digitação terminar e de ler. Z pula.
        self.TEMPO_TEXTO_BASE = 900
        self.TEMPO_POR_CARACTERE = 40
        self.TEMPO_TEXTO_MAX = 4500
        self.DELAY_FIM_BATALHA = 2500
        self.DURACAO_PREPARO = 400  # caixa de texto virando caixa de batalha
        self.temporizador_fim = 0
        self.temporizador_inimigo = 0
        self.fala_inimigo = []  # falas durante o ataque (balão ao lado do inimigo)
        # Hitbox da alma menor que o sprite, como no Undertale/Deltarune.
        self.MARGEM_HITBOX_ALMA = 10
        nome_inimigo_capitalizado = self.inimigos[0].nome.title()
        dao_ataque = AtaqueDAO()
        padroes_ataque = dao_ataque.carregar_ataques_por_inimigo(nome_inimigo_capitalizado)
        self.sequenciador = SequenciadorDeAtaque(padroes_ataque, nome_inimigo_capitalizado)
        self.mensagens_atuais = self.mensagens_turno_jogador()
        self.relatorio.turnos_passados += 1
        self.alma_tomou_dano_este_frame = False

    @property
    def batalha_encerrada(self):
        """True quando a batalha acabou E a mensagem final já ficou na tela."""
        return self.estado_batalha in ["VITORIA", "DERROTA"] and self.temporizador_fim <= 0

    def pular_espera(self):
        if self.estado_batalha == "PLAYER_ACTION_SEQUENCE":
            self.temporizador_acao = 0
        elif self.estado_batalha == "ENEMY_DIALOGO":
            self.temporizador_inimigo = 0
        elif self.estado_batalha in ["VITORIA", "DERROTA"]:
            self.temporizador_fim = 0

    def tempo_de_leitura(self, mensagens):
        caracteres = sum(len(m) for m in mensagens)
        return min(self.TEMPO_TEXTO_MAX, self.TEMPO_TEXTO_BASE + caracteres * self.TEMPO_POR_CARACTERE)

    def mensagens_turno_jogador(self):
        """Texto de ambiente mostrado enquanto o jogador escolhe (estilo Deltarune)."""
        inimigo = self.inimigos[0]
        if inimigo.poupado:
            ambiente = f"{inimigo.nome} não quer mais lutar."
        elif inimigo.vida <= inimigo.vida_max * 0.3:
            ambiente = f"{inimigo.nome} está ofegante."
        elif self.relatorio.turnos_passados <= 1:
            ambiente = f"{inimigo.nome} bloqueia o caminho!"
        else:
            ambiente = f"{inimigo.nome} te encara."
        return [ambiente, f"O que {self.jogador_atual.nome} vai fazer?"]

    def atualizar(self, dt):
        self.alma_tomou_dano_este_frame = False
        self.verificar_fim_de_batalha()
        if self.estado_batalha in ["VITORIA", "DERROTA"]:
            self.temporizador_fim -= dt
            return

        if self.estado_batalha.startswith("PLAYER_SELECT"):
            pass
        elif self.estado_batalha == "PLAYER_ACTION_SEQUENCE":
            self.atualizar_sequencia_acao(dt)

        elif self.estado_batalha == "ENEMY_DIALOGO":
            self.temporizador_inimigo -= dt
            if self.temporizador_inimigo <= 0:
                self.estado_batalha = "ENEMY_PREPARO"
                self.temporizador_inimigo = self.DURACAO_PREPARO

        elif self.estado_batalha == "ENEMY_PREPARO":
            self.temporizador_inimigo -= dt
            if self.temporizador_inimigo <= 0:
                self.estado_batalha = "ENEMY_TURN"

        elif self.estado_batalha == "ENEMY_TURN":
            resultado = self.sequenciador.atualizar(dt,
                                                 self.alma,
                                                 self.rect_battle_box,
                                                 self.inimigos[0].atk)

            if resultado.novos_projeteis:
                self.projeteis.extend(resultado.novos_projeteis)
                self.projeteis_novos.extend(resultado.novos_projeteis)
            if resultado.novas_mensagens:
                self.fala_inimigo = resultado.novas_mensagens
            if resultado.ataque_terminou:
                self.iniciar_turno_jogador()

            self.atualizar_projeteis(dt)

    def atualizar_sequencia_acao(self, dt):
        self.temporizador_acao -= dt
        if self.temporizador_acao > 0:
            return

        if self.indice_sequencia_acao < len(self.acoes_jogadores_turno):
            (jogador, acao, alvo) = self.acoes_jogadores_turno[self.indice_sequencia_acao]
            self.indice_sequencia_acao += 1

            # Jogador caído não gasta o tempo de espera de ninguém.
            if acao is None or not jogador.estou_vivo():
                return

            if alvo is None or alvo.estou_vivo():
                resultado = acao.executar(jogador, alvo)
                self.mensagens_atuais = resultado.get("mensagens", ["..."])
                self.relatorio.vida_curada += resultado.get("cura", 0)
                self.relatorio.dano_causado += resultado.get("dano", 0)
            else:
                self.mensagens_atuais = [f"{jogador.nome} não pode agir!"]

            self.temporizador_acao = self.tempo_de_leitura(self.mensagens_atuais)
            self.verificar_fim_de_batalha()
        else:
            self.acoes_jogadores_turno.clear()
            self.iniciar_turno_inimigo()

    def atualizar_projeteis(self, dt):
        m = self.MARGEM_HITBOX_ALMA
        hitbox_alma = self.rect_alma.inflate(-m, -m)
        for projetil in self.projeteis[:]:
            projetil.mover()
            if projetil.verificar_colisao(hitbox_alma):
                dano_sofrido = self.alma.levei_dano(projetil.dano)
                if dano_sofrido > 0:
                    self.relatorio.dano_recebido += dano_sofrido
                    self.alma_tomou_dano_este_frame = True
                if dano_sofrido > 0 and not projetil.passa:
                    projetil.ativa = False
            projetil.verificar_limites(self.rect_battle_box)
            if not projetil.ativa:
                self.projeteis.remove(projetil)

    def menu_mover_cursor(self, direcao: str):
        if not self.estado_batalha.startswith("PLAYER_SELECT"): return
        if direcao in ["UP", "LEFT"]:
            self.menu_ativo.mover_anterior()
        elif direcao in ["DOWN", "RIGHT"]:
            self.menu_ativo.mover_proximo()

    def menu_selecionar_opcao(self):
        if not self.estado_batalha.startswith("PLAYER_SELECT"): return
        opcao_selecionada = self.menu_ativo.obter_selecionado()
        if not opcao_selecionada: return
        alvo_padrao = self.inimigos[0] if self.inimigos else None

        if self.estado_batalha == "PLAYER_SELECT":
            nome_acao = opcao_selecionada.nome
            if nome_acao == "Ataque" or nome_acao == "Poupar":
                self.acoes_jogadores_turno.append((self.jogador_atual, opcao_selecionada, alvo_padrao))
                self.avancar_proximo_jogador_vivo()
            elif nome_acao == "Agir":
                self.menu_agir = ModeloMenu(self.jogador_atual.habilidades)
                self.menu_ativo = self.menu_agir
                self.estado_batalha = "PLAYER_SELECT_AGIR"
            elif nome_acao == "Item":
                self.menu_item = ModeloMenu(self.jogador_atual.inventario)
                self.menu_ativo = self.menu_item
                self.estado_batalha = "PLAYER_SELECT_ITEM"
        elif self.estado_batalha == "PLAYER_SELECT_AGIR":
            self.acoes_jogadores_turno.append((self.jogador_atual, opcao_selecionada, alvo_padrao))
            self.avancar_proximo_jogador_vivo()
        elif self.estado_batalha == "PLAYER_SELECT_ITEM":
            self.acoes_jogadores_turno.append((self.jogador_atual, opcao_selecionada, self.jogador_atual))
            self.avancar_proximo_jogador_vivo()

    def menu_voltar(self):
        if self.estado_batalha in ["PLAYER_SELECT_AGIR", "PLAYER_SELECT_ITEM"]:
            self.estado_batalha = "PLAYER_SELECT"
            self.menu_ativo = self.menu_principal

    def avancar_proximo_jogador_vivo(self):
        self.estado_batalha = "PLAYER_SELECT"
        self.menu_ativo = self.menu_principal
        self.menu_agir = None
        self.menu_item = None
        self.indice_jogador_atual += 1

        if self.indice_jogador_atual >= len(self.jogadores):
            self.estado_batalha = "PLAYER_ACTION_SEQUENCE"
            self.indice_sequencia_acao = 0
            self.temporizador_acao = 0
            return

        self.jogador_atual = self.jogadores[self.indice_jogador_atual]
        if not self.jogador_atual.estou_vivo():
            self.acoes_jogadores_turno.append((self.jogador_atual, None, None))
            self.avancar_proximo_jogador_vivo()
            return

        self.mensagens_atuais = self.mensagens_turno_jogador()
        self.menu_principal.indice_selecionado = 0
        self.menu_ativo = self.menu_principal

    def limpar_projeteis(self):
        # Desativa antes de limpar: o ControladorBatalha descarta as visões
        # dos projéteis inativos, então nenhum "osso fantasma" sobra pro próximo turno.
        for projetil in self.projeteis:
            projetil.ativa = False
        self.projeteis.clear()
        self.projeteis_novos.clear()

    def iniciar_turno_inimigo(self):
        if self.estado_batalha in ["VITORIA", "DERROTA"]: return

        # Antes do ataque: a fala do inimigo aparece na caixa de texto
        # (ENEMY_DIALOGO), depois a caixa vira a caixa de batalha (ENEMY_PREPARO)
        # e só então os projéteis começam (ENEMY_TURN).
        self.estado_batalha = "ENEMY_DIALOGO"
        self.limpar_projeteis()
        self.fala_inimigo = []
        # Alma volta pro centro da caixa a cada ataque.
        self.rect_alma.center = self.rect_battle_box.center
        self.mensagens_atuais = self.sequenciador.iniciar_novo_ataque(self.alma)
        self.temporizador_inimigo = self.tempo_de_leitura(self.mensagens_atuais)

    def iniciar_turno_jogador(self):
        self.alma.mudar_cor("vermelho")
        self.limpar_projeteis()
        self.fala_inimigo = []
        if self.estado_batalha in ["VITORIA", "DERROTA"]: return
        for jogador in self.jogadores:
            jogador.atualizar_status()
        self.indice_jogador_atual = -1
        self.relatorio.turnos_passados += 1
        self.avancar_proximo_jogador_vivo()

    def verificar_fim_de_batalha(self):
        if self.estado_batalha in ["VITORIA", "DERROTA"]:
            return
        jogadores_vivos = [j for j in self.jogadores if j.estou_vivo()]
        inimigos_em_combate = [i for i in self.inimigos if i.estou_vivo() and not i.foi_poupado]

        if not jogadores_vivos:
            self.estado_batalha = "DERROTA"
            self.mensagens_atuais = ["Você perdeu..."]
        elif not inimigos_em_combate:
            self.estado_batalha = "VITORIA"
            poupados = any(i.foi_poupado for i in self.inimigos)
            self.relatorio.poupado = poupados
            # Mantém a última mensagem (ex: "X foi poupado") e adiciona o resultado.
            self.mensagens_atuais = list(self.mensagens_atuais[-2:]) + ["Você venceu a batalha!"]
        else:
            return

        self.limpar_projeteis()
        self.temporizador_fim = self.DELAY_FIM_BATALHA