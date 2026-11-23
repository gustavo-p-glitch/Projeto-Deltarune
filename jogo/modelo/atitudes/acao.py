from jogo.modelo.atitudes.atitude import Atitude


class Acao(Atitude):
    def __init__(self, nome: str, numero: int):
        super().__init__(nome)
        self.numero = numero

    def executar(self, jogador_usando, alvo=None):
        # Antes isso incrementava `alvo.contador`, um contador separado que o Poupar
        # nunca lia — ou seja, Convencer não servia pra nada. Agora alimenta a
        # mesma barra de poupança usada pelo Poupar e pelo Checar.
        if alvo is not None and getattr(alvo, 'num', None) == self.numero and hasattr(alvo, 'contador_poupanca'):
            if alvo.poupado:
                return {"mensagens": [f"{alvo.nome} já pode ser POUPADO!"]}

            alvo.contador_poupanca += 1
            maximo = alvo.contador_poupanca_max
            mensagens = [f"{jogador_usando.nome} tenta {self.nome.lower()} {alvo.nome}...",
                         f"{alvo.nome} está se convencendo! {alvo.contador_poupanca}/{maximo}"]
            if alvo.poupado:
                mensagens.append(f"{alvo.nome} pode ser POUPADO!")
            return {"mensagens": mensagens}

        return {"mensagens": [f"{jogador_usando.nome} tenta {self.nome.lower()}... nada acontece."]}
