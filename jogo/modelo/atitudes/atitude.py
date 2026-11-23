from abc import ABC, abstractmethod


class Atitude(ABC):
    def __init__(self, nome):
        self.nome = nome

    @abstractmethod
    def executar(self, jogador_usando, alvo=None) -> dict:
        """Retorna {"mensagens": [...], "dano": int, "cura": int}."""
