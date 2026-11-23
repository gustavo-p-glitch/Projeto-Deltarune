from jogo.modelo.atitudes.atitude import Atitude

class Checar(Atitude):
    def __init__(self, num: int):
        super().__init__("Checar")
        self.__num = num

    @property
    def num(self):
        return self.__num

    def executar(self, jogador_usando, alvo=None):
        if not alvo:
            return {"mensagens": [f"{jogador_usando.nome} checa nada"]}

        vida_max = getattr(alvo, 'vida_max', 0)
        mensagem = f"{jogador_usando.nome} checa {alvo.nome}: "
        mensagem += f"Vida: {alvo.vida}/{vida_max}, "
        mensagem += f"Magia: {alvo.magia}, "
        mensagem += f"Ataque: {alvo.atk}, "
        mensagem += f"Defesa: {alvo.defn}"

        if hasattr(alvo, 'poupado'):
            poupavel = "sim" if alvo.poupado else f"{alvo.contador_poupanca}/3"
            mensagem += f", Poupável: {poupavel}"

        return {"mensagens": [mensagem]}