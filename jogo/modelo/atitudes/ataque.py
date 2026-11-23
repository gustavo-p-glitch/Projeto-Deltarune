from jogo.modelo.atitudes.atitude import Atitude
import random

class Ataque(Atitude):
    def __init__(self):
        super().__init__("Ataque")

    def executar(self, jogador_usando, alvo=None):
        if not alvo:
            return {"mensagens": [f"{jogador_usando.nome} ataca o ar!"]}

        dano_base = jogador_usando.atk
        dano_final = random.randint(int(dano_base * 0.9), int(dano_base * 1.1))
        dano_final = max(1, dano_final)

        dano_real_sofrido = alvo.levei_dano(dano_final)

        mensagens = [f"{jogador_usando.nome} ataca {alvo.nome}!",
                     f"Causou {dano_real_sofrido} de dano."]

        return {"mensagens": mensagens, "dano": dano_real_sofrido}