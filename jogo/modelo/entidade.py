from abc import ABC, abstractmethod

class Entidade(ABC):
    def __init__(self, nome: str, magia: int, atk: int, defn: int):
        self.nome = nome
        self.magia = magia
        self.atk = atk
        self.defn = defn
        self.dano_fogo = 0
        self.duracao_fogo = 0
        self.congelado = False

    @abstractmethod
    def levei_dano(self, dano: int):
        pass

    @abstractmethod
    def estou_vivo(self):
        pass

    def aplicar_fogo(self, dano, duracao):
        self.dano_fogo = dano
        self.duracao_fogo = duracao