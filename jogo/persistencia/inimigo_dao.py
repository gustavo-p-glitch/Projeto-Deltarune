from jogo.persistencia.dao import DAO
from jogo.excecoes import ExcecaoInimigoNaoCriado, ExcecaoInimigoSemNome, ExcecaoDuplicado

class InimigoDao(DAO):
    def __init__(self):
        super().__init__('inimigos.json')
        if not self.ler():
            self.preencher_dados()

    def adicionar(self, dados_inimigo: dict):
        if not isinstance(dados_inimigo, dict):
            raise ExcecaoInimigoNaoCriado()
        nome = dados_inimigo.get('nome')
        if not nome:
            raise ExcecaoInimigoSemNome()

        for item in self.ler():
            # Sem diferenciar maiúsculas: "sans" e "Sans" são o mesmo inimigo.
            if str(item.get('nome', '')).lower() == nome.lower():
                raise ExcecaoDuplicado(nome)
        super().adicionar(dados_inimigo)

    def remover(self, ident, chave='nome'):
        self.cache = [item for item in self.cache
                      if item.get(chave) != ident]
        self.salvar()

    def preencher_dados(self):
        dados_iniciais = [
            {"nome": "Lancer", "vida": 30, "magia": 0, "atk": 8, "defn": 1, "lootouro": 10,
             "pasta_anim": "pasta_anim_lancer"},
            {"nome": "Dummy", "vida": 50, "magia": 0, "atk": 5, "defn": 0, "lootouro": 5,
             "pasta_anim": "pasta_anim_dummy"}
        ]
        for inimigo in dados_iniciais:
            super().adicionar(inimigo)



