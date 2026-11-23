from jogo.persistencia.inimigo_dao import InimigoDao
from jogo.persistencia.relatorio_dao import RelatorioDAO
from jogo.excecoes import ExcecaoInimigoSemNome, ExcecaoCamposNumericosInvalidos

class ModeloSelecaoInimigo:
    def __init__(self):
        self._estado = "SELECT"
        self.mensagem_erro = ""

        self.dao = InimigoDao()
        self.dao_relatorio = RelatorioDAO()

        self.lista_info_inimigos = self.dao.ler()
        self.lista_relatorios = []

        self.opcoes_menu = []
        self.indice_selecao_menu = 0
        self.atualizar_opcoes_menu()

        self.ordem_campos = ["nome", "vida", "magia", "atk", "defn", "lootouro", "pasta_anim"]
        self.ordem_info = {
            "nome": "", "vida": "50", "magia": "0", "atk": "10",
            "defn": "5", "lootouro": "10", "pasta_anim": "pasta_anim_dummy"
        }
        self.indice_campo_ativo = 0

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, novo_estado):
        self._estado = novo_estado
        self.mensagem_erro = ""

    def atualizar_opcoes_menu(self):
        self.lista_info_inimigos = self.dao.ler()
        self.opcoes_menu = [info["nome"] for info in self.lista_info_inimigos]
        self.opcoes_menu.append("--- VER RELATÓRIOS ---")
        self.opcoes_menu.append("--- CRIAR NOVO INIMIGO ---")
        self.opcoes_menu.append("--- EXCLUIR INIMIGO ---")
        self.indice_selecao_menu = min(self.indice_selecao_menu, max(0, len(self.opcoes_menu) - 1))

    def menu_mover_cima(self):
        self.indice_selecao_menu = (self.indice_selecao_menu - 1) % len(self.opcoes_menu)

    def menu_mover_baixo(self):
        self.indice_selecao_menu = (self.indice_selecao_menu + 1) % len(self.opcoes_menu)

    def obter_texto_opcao_selecionada(self):
        return self.opcoes_menu[self.indice_selecao_menu]

    def obter_dados_inimigo_selecionado(self):
        if self.indice_selecao_menu < len(self.lista_info_inimigos):
            return self.lista_info_inimigos[self.indice_selecao_menu]
        return None

    def excluir_inimigo_selecionado(self):
        if self.indice_selecao_menu < len(self.lista_info_inimigos):
            nome_para_excluir = self.lista_info_inimigos[self.indice_selecao_menu].get("nome")
            self.dao.remover(nome_para_excluir)
            self.atualizar_opcoes_menu()

    def formulario_mover_cima(self):
        self.indice_campo_ativo = (self.indice_campo_ativo - 1) % len(self.ordem_campos)

    def formulario_mover_baixo(self):
        self.indice_campo_ativo = (self.indice_campo_ativo + 1) % len(self.ordem_campos)

    def obter_campo_ativo(self):
        return self.ordem_campos[self.indice_campo_ativo]

    def atualizar_campo(self, texto):
        nome_campo = self.obter_campo_ativo()
        self.ordem_info[nome_campo] = texto

    def adicionar_inimigo(self):
        nome_capitalizado = self.ordem_info["nome"].title()

        if not nome_capitalizado:
            raise ExcecaoInimigoSemNome()

        try:
            novo_inimigo = {
                "nome": nome_capitalizado,
                "vida": int(self.ordem_info["vida"]),
                "magia": int(self.ordem_info["magia"]),
                "atk": int(self.ordem_info["atk"]),
                "defn": int(self.ordem_info["defn"]),
                "lootouro": int(self.ordem_info["lootouro"]),
                "pasta_anim": self.ordem_info["pasta_anim"],
            }
        except ValueError:
            raise ExcecaoCamposNumericosInvalidos()

        self.dao.adicionar(novo_inimigo)

        self.atualizar_opcoes_menu()
        self.ordem_info = {k: ("" if k == "nome" else v) for k, v in self.ordem_info.items()}
        self.ordem_info["vida"] = "50"
        return True

    def carregar_relatorios(self):
        self.lista_relatorios = self.dao_relatorio.ler_todos()
        self.lista_relatorios.sort(key=lambda r: r.get('timestamp', ''), reverse=True)