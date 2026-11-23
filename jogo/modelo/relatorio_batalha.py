import datetime


class RelatorioBatalha:
    def __init__(self, nome_inimigo: str = ""):
        self.nome_inimigo = nome_inimigo
        self.dano_recebido = 0
        self.vida_curada = 0
        self.turnos_passados = 0
        self.dano_causado = 0
        self.vitoria = False
        self.poupado = False

        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def para_dict(self):
        return {
            "timestamp": self.timestamp,
            "inimigo": self.nome_inimigo,
            "vitoria": self.vitoria,
            "poupado": self.poupado,
            "turnos_passados": self.turnos_passados,
            "dano_causado": self.dano_causado,
            "dano_recebido": self.dano_recebido,
            "vida_curada": self.vida_curada
        }
