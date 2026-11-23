from jogo.modelo.tipo import Tipo
from jogo.modelo.efeito import Efeito

class Item:
    def __init__(self, nome: str, tipo: Tipo, efeito: Efeito):
        self.nome = nome
        self.tipo = tipo
        self.efeito = efeito

    def executar(self, portador: 'Jogador', alvo: 'Jogador'):
        if self.tipo.nome != "consumivel":
            return {"mensagens": [f"{self.nome} não pode ser usado agora."]}

        cura_real = 0
        if self.efeito.cura > 0:
            cura_real = alvo.curar(self.efeito.cura)

        if self in portador.inventario:
            portador.inventario.remove(self)

        return {
            "mensagens": [f"{portador.nome} usou {self.nome}!", f"Recuperou {cura_real} HP."],
            "cura": cura_real
        }