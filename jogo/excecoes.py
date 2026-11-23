class ExcecaoDuplicado(Exception):
    def __init__(self, nome_alvo):
        self.mensagem = f"Já existe um inimigo chamado '{nome_alvo}'. Escolha outro."
        super().__init__(self.mensagem)

class ExcecaoInimigoSemNome(Exception):
    def __init__(self):
        self.mensagem = "O campo 'Nome' é obrigatório e não pode estar vazio!"
        super().__init__(self.mensagem)

class ExcecaoInimigoNaoCriado(Exception):
    def __init__(self):
        self.mensagem = "Erro interno: Os dados fornecidos não são válidos."
        super().__init__(self.mensagem)

class ExcecaoCamposNumericosInvalidos(Exception):
    def __init__(self):
        self.mensagem = "Os campos Vida, Atk, Magia, etc. devem ser números inteiros!"
        super().__init__(self.mensagem)

class ExcecaoDadosCorrompidos(Exception):
    def __init__(self):
        self.mensagem = "O arquivo de dados está corrompido."
        super().__init__(self.mensagem)

class ExcecaoAtaqueMalFormatado(Exception):
    def __init__(self, detalhe=""):
        self.mensagem = f"Erro no JSON de ataque"
        super().__init__(self.mensagem)

class ExcecaoManaInsuficiente(Exception):
    def __init__(self, custo, atual):
        self.mensagem = f"TP Insuficiente!"
        super().__init__(self.mensagem)

class ExcecaoItemNaoUsavel(Exception):
    def __init__(self, nome_item):
        self.mensagem = f"O item '{nome_item}' não pode ser usado agora."
        super().__init__(self.mensagem)

class ExcecaoRecursoNaoEncontrado(Exception):
    def __init__(self, recurso):
        self.mensagem = f"Erro: O recurso '{recurso}' não foi encontrado."
        super().__init__(self.mensagem)