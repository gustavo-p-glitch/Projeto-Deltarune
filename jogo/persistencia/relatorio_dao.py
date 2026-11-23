from jogo.persistencia.dao import DAO

class RelatorioDAO(DAO):
    def __init__(self):
        super().__init__('relatorios.json')

    def adicionar(self, dict_relatorio: dict):
        if not isinstance(dict_relatorio, dict):
            return

        if not dict_relatorio.get('timestamp'):
            return

        super().adicionar(dict_relatorio)

    def ler_todos(self):
        return self.ler()