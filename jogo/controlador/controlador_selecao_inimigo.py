import pygame
from jogo.modelo.modelo_selecao_inimigo import ModeloSelecaoInimigo
from jogo.visao.visao_selecao_inimigo import VisaoSelecaoInimigo

class ControladorSelecaoInimigo:
    def __init__(self):
        self.modelo = ModeloSelecaoInimigo()
        self.visao = VisaoSelecaoInimigo()
        self._inimigo_selecionado_este_frame = None

    def desenhar(self, superficie: pygame.Surface):
        dados_menu = {
            'opcoes': self.modelo.opcoes_menu,
            'indice_selecionado': self.modelo.indice_selecao_menu
        }

        dados_formulario = {
            'campos': self.modelo.ordem_campos,
            'valores': self.modelo.ordem_info,
            'indice_ativo': self.modelo.indice_campo_ativo
        }

        dados_relatorios = []
        for r in self.modelo.lista_relatorios:
            dados_relatorios.append({
                'data': r.get('timestamp', 'N/A'),
                'vitoria': r.get('vitoria', False),
                'turnos': r.get('turnos_passados', 0),
                'inimigo': r.get('inimigo', ''),
                'poupado': r.get('poupado', False)
            })

        self.visao.desenhar(
            superficie,
            estado=self.modelo.estado,
            dados_menu=dados_menu,
            dados_formulario=dados_formulario,
            dados_relatorios=dados_relatorios,
            mensagem_erro=self.modelo.mensagem_erro
        )

    def manipular_evento(self, evento):
        self.modelo.mensagem_erro = ""

        if self.modelo.estado == "SELECT":
            self.manipular_evento_selecao(evento)
        elif self.modelo.estado == "CREATE":
            self.manipular_evento_criacao(evento)
        elif self.modelo.estado == "DELETE":
            self.manipular_evento_exclusao(evento)
        elif self.modelo.estado == "VIEW_REPORTS":
            self.manipular_evento_relatorios(evento)

    def manipular_teclas_pressionadas(self, teclas):
        pass

    def atualizar(self, dt):
        pass

    def manipular_evento_selecao(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                self.modelo.menu_mover_cima()
            elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                self.modelo.menu_mover_baixo()

            elif evento.key == pygame.K_z:
                opcao = self.modelo.obter_texto_opcao_selecionada()

                if opcao == "--- CRIAR NOVO INIMIGO ---":
                    self.modelo.estado = "CREATE"
                elif opcao == "--- EXCLUIR INIMIGO ---":
                    self.modelo.estado = "DELETE"
                elif opcao == "--- VER RELATÓRIOS ---":
                    self.modelo.carregar_relatorios()
                    self.modelo.estado = "VIEW_REPORTS"
                else:
                    dados_inimigo = self.modelo.obter_dados_inimigo_selecionado()
                    if dados_inimigo:
                        self._inimigo_selecionado_este_frame = dados_inimigo

    def manipular_evento_exclusao(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                self.modelo.menu_mover_cima()
            elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                self.modelo.menu_mover_baixo()
            elif evento.key == pygame.K_z:
                self.modelo.excluir_inimigo_selecionado()
                self.modelo.estado = "SELECT"
            elif evento.key == pygame.K_x:
                self.modelo.estado = "SELECT"

    def manipular_evento_relatorios(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_x or evento.key == pygame.K_z:
                self.modelo.estado = "SELECT"

    def manipular_evento_criacao(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.modelo.formulario_mover_cima()
            elif evento.key == pygame.K_DOWN:
                self.modelo.formulario_mover_baixo()

            nome_campo_ativo = self.modelo.obter_campo_ativo()
            texto_atual = self.modelo.ordem_info[nome_campo_ativo]

            if evento.key == pygame.K_RETURN:
                try:
                    self.modelo.adicionar_inimigo()
                    self.modelo.estado = "SELECT"
                except Exception as e:
                    self.modelo.mensagem_erro = str(e)

            elif evento.key == pygame.K_ESCAPE:
                # Era K_x: impossível digitar qualquer nome com a letra "x".
                self.modelo.estado = "SELECT"
            elif evento.key == pygame.K_BACKSPACE:
                self.modelo.atualizar_campo(texto_atual[:-1])
            elif evento.unicode and evento.key not in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                                                       pygame.K_RETURN, pygame.K_TAB, pygame.K_ESCAPE]:
                self.modelo.atualizar_campo(texto_atual + evento.unicode)

    def obter_inimigo_selecionado(self):
        dados = self._inimigo_selecionado_este_frame
        self._inimigo_selecionado_este_frame = None
        return dados