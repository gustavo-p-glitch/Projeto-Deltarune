from jogo.modelo.atitudes.atitude import Atitude
from jogo.modelo.efeito import Efeito
from jogo.modelo.tipo import Tipo

class Habilidade(Atitude):
    def __init__(self, nome: str, tipo: Tipo, custo_magia: int, efeitos: Efeito):
        super().__init__(nome)
        self.__tipo = tipo
        self.__custo_magia = custo_magia
        self.__efeitos = efeitos

    @property
    def tipo(self):
        return self.__tipo

    @property
    def custo_magia(self):
        return self.__custo_magia

    @property
    def efeitos(self):
        return self.__efeitos

    def executar(self, jogador_usando, alvo=None):
        mensagens = []
        cura_real = 0
        dano_real = 0

        if jogador_usando.magia >= self.custo_magia:
            jogador_usando.magia -= self.__custo_magia
            mensagens.append(f"{jogador_usando.nome} usa {self.nome}!")

            if self.__efeitos.cura > 0:
                if alvo is None:
                    alvo = jogador_usando
                cura_real = alvo.curar(self.__efeitos.cura)
                mensagens.append(f"{alvo.nome} foi curado em {cura_real} pontos de vida!")

            if self.__efeitos.aumentar_ataque > 0:
                jogador_usando.atk += self.__efeitos.aumentar_ataque
                mensagens.append(f"O ataque de {jogador_usando.nome} aumentou em {self.__efeitos.aumentar_ataque}!")

            if self.__efeitos.dano_fogo > 0 and self.__efeitos.duracao_fogo > 0:
                if alvo:
                    alvo.aplicar_fogo(self.__efeitos.dano_fogo, self.__efeitos.duracao_fogo)
                    mensagens.append(f"{alvo.nome} está pegando fogo!")
        else:
            mensagens.append(f"{jogador_usando.nome} não tem magia suficiente!")

        return {"mensagens": mensagens, "cura": cura_real, "dano": dano_real}