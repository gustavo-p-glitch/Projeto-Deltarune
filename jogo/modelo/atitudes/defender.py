from jogo.modelo.atitudes.atitude import Atitude

class Defender(Atitude):
    def __init__(self, valor_defesa: int = 15, duracao: int = 2):
        super().__init__("Defender")
        self.valor_defesa = valor_defesa
        self.duracao = duracao

    def executar(self, jogador_usando, alvo=None):
        if not hasattr(jogador_usando, 'defn_base'):
            jogador_usando.defn_base = jogador_usando.defn

        jogador_usando.defn = jogador_usando.defn_base + self.valor_defesa
        jogador_usando.defesa_duracao = self.duracao

        mensagens = [f"{jogador_usando.nome} defende!",
                     f"Defesa aumentada em {self.valor_defesa}."]

        return {"mensagens": mensagens}