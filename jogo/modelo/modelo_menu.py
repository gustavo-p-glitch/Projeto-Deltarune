class ModeloMenu:
    def __init__(self, lista_opcoes):
        self.opcoes = lista_opcoes
        self.indice_selecionado = 0
        self.sub_menu = None

    def mover_anterior(self):
        if not self.opcoes:
            return
        self.indice_selecionado = (self.indice_selecionado - 1) % len(self.opcoes)

    def mover_proximo(self):
        if not self.opcoes:
            return
        self.indice_selecionado = (self.indice_selecionado + 1) % len(self.opcoes)

    def obter_selecionado(self):
        if not self.opcoes or self.indice_selecionado >= len(self.opcoes):
            return None
        return self.opcoes[self.indice_selecionado]