from jogo.modelo.atitudes.atitude import Atitude


class Poupar(Atitude):
    def __init__(self):
        super().__init__("Poupar")

    def executar(self, jogador_usando, alvo=None):
        if not alvo:
            return {"mensagens": [f"{jogador_usando.nome} tenta poupar!"]}

        if getattr(alvo, 'poupado', False):
            # Antes fazia `alvo.vida = 0` — poupar matava o inimigo.
            alvo.foi_poupado = True
            return {"mensagens": [f"{jogador_usando.nome} poupou {alvo.nome}!"]}

        # Como no Deltarune: POUPAR só funciona depois de encher a barra com AGIR.
        # (Antes, 3 Poupar seguidos no mesmo turno já liberavam a vitória.)
        progresso = getattr(alvo, 'contador_poupanca', 0)
        maximo = getattr(alvo, 'contador_poupanca_max', 3)
        return {"mensagens": [f"{jogador_usando.nome} tenta poupar {alvo.nome}...",
                              f"Ainda não! ({progresso}/{maximo}) Tente AGIR > Convencer."]}
