import pygame
from jogo.modelo.modelo_batalha import ModeloBatalha
from jogo.visao.visao_batalha import VisaoBatalha
from jogo.visao.battlebox import BattleBox
from jogo.controlador.controlador_jogador import ControladorJogador
from jogo.controlador.controlador_inimigo import ControladorInimigo
from jogo.controlador.controlador_alma import ControladorAlma
from jogo.controlador.controlador_projetil import ControladorProjetil
from jogo.modelo.item import Item
from jogo.modelo.efeito import Efeito
from jogo.modelo.tipo import Tipo
from jogo.modelo.atitudes.ataque import Ataque
from jogo.modelo.atitudes.acao import Acao
from jogo.modelo.atitudes.checar import Checar
from jogo.modelo.atitudes.defender import Defender
from jogo.modelo.atitudes.poupar import Poupar


class ControladorBatalha:
    # Layout: inimigo no topo, caixa de texto/batalha no meio, cada aliado logo
    # acima do seu painel de HP. Posições da party = onde ficam os PÉS de cada um
    # (x = centro do painel de HP correspondente).
    POSICOES_PARTY = [(144, 488), (400, 488), (656, 488)]
    POSICAO_INIMIGO = (400, 83)
    RECT_CAIXA_BATALHA = (280, 160, 240, 240)  # fundo em y=400, acima da cabeça do Grão

    def __init__(self, largura_tela, altura_tela, info_inimigo: dict):
        p = self.POSICOES_PARTY
        self.controladores_jogadores = [
            # Lume e Grão: personagens originais (sprites gerados por gerador_personagens.py).
            # Para voltar aos desenhos antigos: imagem="kris.png"/"susie.png" e sem escala.
            ControladorJogador("Lume", 90, 10, 5, "lume", 100, pos=p[0], cor=(255, 180, 70),
                               escala=3, velocidade_animacao=380),
            ControladorJogador("Grão", 100, 20, 10, "grao", 220, pos=p[1], cor=(110, 210, 235),
                               escala=3, velocidade_animacao=420),
            ControladorJogador("Ralsei", 200, 5, 3, "ralsei.png", 90, pos=p[2], cor=(100, 230, 120))
        ]
        self.controladores_inimigos = [
            ControladorInimigo(
                nome=info_inimigo["nome"],
                vida=info_inimigo["vida"],
                magia=info_inimigo["magia"],
                atk=info_inimigo["atk"],
                defn=info_inimigo["defn"],
                loot_ouro=info_inimigo["lootouro"],
                imagens=info_inimigo["pasta_anim"],
                pos=self.POSICAO_INIMIGO
            )
        ]

        modelos_jogadores = [cj.modelo for cj in self.controladores_jogadores]
        modelos_inimigos = [ci.modelo for ci in self.controladores_inimigos]

        self.acoes_menu_principal = [
            Ataque(),
            Acao("Agir", 0),
            Acao("Item", 0),
            Poupar()
        ]

        item_biscoito = Item("Biscoito", Tipo("consumivel", "Cura."), Efeito(cura=10))
        item_cenoura = Item("TopCenoura", Tipo("consumivel", "Cura."), Efeito(cura=30))
        item_torta = Item("TortadeCaramelo", Tipo("consumivel", "cura"), Efeito(cura=100))

        for j_modelo in modelos_jogadores:
            j_modelo.aprender_habilidade(Checar(1))
            j_modelo.aprender_habilidade(Defender(15, 1))
            j_modelo.aprender_habilidade(Acao("Convencer", 1))
            j_modelo.inventario.append(item_biscoito)
            j_modelo.inventario.append(item_cenoura)
            j_modelo.inventario.append(item_torta)

        self.controlador_alma = ControladorAlma(modelos_jogadores)
        self.battle_box = BattleBox(*self.RECT_CAIXA_BATALHA)
        self.controlador_alma.rect.center = self.battle_box.rect.center
        # Mesmo objeto (não .copy()) para modelo e controlador sempre enxergarem
        # a alma no mesmo lugar.
        rect_alma_inicial = self.controlador_alma.rect

        self.modelo = ModeloBatalha(
            modelos_jogadores,
            modelos_inimigos,
            self.controlador_alma.modelo,
            self.battle_box.rect,
            rect_alma_inicial,
            self.acoes_menu_principal
        )

        self.visao = VisaoBatalha(largura_tela, altura_tela, info_inimigo.get("musica"))
        self.controladores_projeteis = []

    def iniciar_musica(self):
        self.visao.iniciar_musica()

    def parar_musica(self):
        self.visao.parar_musica()

    def manipular_evento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return

        estado_batalha = self.modelo.estado_batalha
        estado_alma = self.controlador_alma.modelo.estado

        if estado_batalha in ["PLAYER_ACTION_SEQUENCE", "ENEMY_DIALOGO", "VITORIA", "DERROTA"]:
            if evento.key in (pygame.K_z, pygame.K_RETURN):
                # 1º Z termina de "digitar" o texto, 2º Z avança
                if not self.visao.texto_completo():
                    self.visao.completar_texto()
                else:
                    self.modelo.pular_espera()
            return

        if estado_batalha == "ENEMY_TURN" and estado_alma == "azul":
            if evento.key == pygame.K_z or evento.key == pygame.K_UP or evento.key == pygame.K_w:
                self.controlador_alma.pular()

        if estado_batalha == "PLAYER_SELECT":
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                self.modelo.menu_mover_cursor("LEFT")
            elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                self.modelo.menu_mover_cursor("RIGHT")

        elif estado_batalha in ["PLAYER_SELECT_AGIR", "PLAYER_SELECT_ITEM"]:
            if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                self.modelo.menu_mover_cursor("UP")
            elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                self.modelo.menu_mover_cursor("DOWN")

        if estado_batalha.startswith("PLAYER_SELECT"):
            if evento.key == pygame.K_z:
                self.modelo.menu_selecionar_opcao()
            elif evento.key == pygame.K_x:
                self.modelo.menu_voltar()

    def manipular_teclas_pressionadas(self, teclas):
        if self.modelo.estado_batalha != "ENEMY_TURN":
            return

        dx, dy = 0, 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]: dx = -1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: dx = 1

        if self.controlador_alma.modelo.estado == "vermelho":
            if teclas[pygame.K_UP] or teclas[pygame.K_w]: dy = -1
            if teclas[pygame.K_DOWN] or teclas[pygame.K_s]: dy = 1

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        self.controlador_alma.mover(dx, dy, self.battle_box.rect)

    def atualizar(self, dt):
        self.modelo.atualizar(dt)

        if self.modelo.alma_tomou_dano_este_frame:
            self.controlador_alma.visao.tocar_som()

        for ci in self.controladores_inimigos:
            ci.atualizar(dt)
        for cj in self.controladores_jogadores:
            cj.atualizar(dt)

        self.visao.atualizar(dt, self.modelo.estado_batalha, self.modelo.mensagens_atuais,
                             self.battle_box.rect)

        if self.modelo.estado_batalha == "ENEMY_TURN":
            teclas = pygame.key.get_pressed()
            pulo_segurado = (teclas[pygame.K_z] or teclas[pygame.K_w] or teclas[pygame.K_UP])
            self.controlador_alma.atualizar_fisica(self.battle_box.rect, pulo_segurado)
        else:
            self.controlador_alma.modelo.atualizar_invencibilidade()

        if self.modelo.projeteis_novos:
            for projetil_modelo in self.modelo.projeteis_novos:
                if projetil_modelo and projetil_modelo.ativa:
                    caminho_imagem = self.obter_imagem_projetil(projetil_modelo)
                    self.controladores_projeteis.append(
                        ControladorProjetil(projetil_modelo, caminho_imagem))

            self.modelo.projeteis_novos.clear()

        # Movimento e colisão ficam no ModeloBatalha; aqui só descartamos as
        # visões de projéteis que o modelo já desativou.
        self.controladores_projeteis = [cb for cb in self.controladores_projeteis if cb.modelo.ativa]

    def obter_imagem_projetil(self, projetil_modelo):
        if hasattr(projetil_modelo, 'tipo_projetil') and projetil_modelo.tipo_projetil:
            tipo = projetil_modelo.tipo_projetil
            if tipo == "bone.png":
                return "osso.png"
            return tipo
        return "osso.png"

    def desenhar(self, superficie):
        estado = self.modelo.estado_batalha
        escolhendo = estado.startswith("PLAYER_SELECT")

        dados_jogadores = []
        for i, (cj, p) in enumerate(zip(self.controladores_jogadores, self.modelo.jogadores)):
            dados_jogadores.append({
                'nome': p.nome,
                'vida': p.vida,
                'max': p.vida_max,
                'vivo': p.estou_vivo(),
                'defesa': p.defesa_duracao > 0,
                'cor': cj.cor,
                'ativo': escolhendo and i == self.modelo.indice_jogador_atual
            })

        menu = self.modelo.menu_principal
        dados_menu = {
            'opcoes': [opt.nome for opt in menu.opcoes],
            'indice_selecionado': menu.indice_selecionado
        }
        if estado in ("PLAYER_SELECT_AGIR", "PLAYER_SELECT_ITEM") and self.modelo.menu_ativo:
            sub = self.modelo.menu_ativo
            dados_menu['submenu'] = {
                'opcoes': [opt.nome for opt in sub.opcoes],
                'descricoes': [self.descrever_opcao(opt) for opt in sub.opcoes],
                'indice_selecionado': sub.indice_selecionado
            }

        # Ordem: personagens -> caixa (texto ou batalha) -> projéteis -> alma -> UI
        for ci in self.controladores_inimigos:
            ci.requisitar_desenho_visao(superficie)
        for cj in self.controladores_jogadores:
            cj.requisitar_desenho(superficie)

        self.visao.desenhar(
            superficie,
            estado=estado,
            dados_jogadores=dados_jogadores,
            dados_menu=dados_menu,
            fala_inimigo=self.modelo.fala_inimigo,
            rect_inimigo=self.controladores_inimigos[0].rect
        )

        if estado == "ENEMY_TURN":
            # Projéteis só aparecem dentro da caixa (igual ao jogo original):
            # assim podem nascer fora dela e "entrar" sem aparecer no meio da tela.
            area_interna = self.battle_box.rect.inflate(-6, -6)
            superficie.set_clip(area_interna)
            for cb in self.controladores_projeteis:
                cb.requisitar_desenho(superficie)
            superficie.set_clip(None)

        if estado in ("ENEMY_PREPARO", "ENEMY_TURN") and self.visao.caixa_pronta(self.battle_box.rect):
            self.controlador_alma.desenhar(superficie)

    @staticmethod
    def descrever_opcao(opcao):
        efeito = getattr(opcao, 'efeito', None)
        if efeito is not None and getattr(efeito, 'cura', 0) > 0:
            return f"Cura {efeito.cura} HP"
        if isinstance(opcao, Defender):
            return f"+{opcao.valor_defesa} DEF"
        if isinstance(opcao, Checar):
            return "Ver status"
        if isinstance(opcao, Acao):
            return "Convence o inimigo"
        return ""
