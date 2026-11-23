from jogo.modelo.entidade import Entidade

class Inimigo(Entidade):
    def __init__(self, nome: str, vida: int, magia: int, atk: int, defn: int, loot_ouro: int):
        super().__init__(nome, magia, atk, defn)
        self.__vida = vida
        self.vida_max = vida
        self.__loot_ouro = loot_ouro
        self.__contador_poupanca = 0
        self.__poupado = False      # pode ser poupado (barra de misericórdia cheia)
        self.foi_poupado = False    # foi efetivamente poupado -> sai da batalha sem morrer
        self.__contador_poupanca_max = 3
        self.num = 1  # id da ação de AGIR que funciona neste inimigo (ver Acao)

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, vida):
        self.__vida = vida

    @property
    def contador_poupanca(self):
        return self.__contador_poupanca

    @contador_poupanca.setter
    def contador_poupanca(self, contador_poupanca: int):
        self.__contador_poupanca = contador_poupanca
        if self.__contador_poupanca >= self.__contador_poupanca_max:
            self.poupado = True

    @property
    def contador_poupanca_max(self):
        return self.__contador_poupanca_max

    @property
    def poupado(self):
        return self.__poupado

    @poupado.setter
    def poupado(self, poupado: bool):
        self.__poupado = poupado

    def levei_dano(self, dano: int):
        dano_recebido = max(0, dano - self.defn)
        vida_antes = self.__vida
        self.vida = max(0, self.vida - dano_recebido)
        vida_perdida_real = vida_antes - self.__vida
        return vida_perdida_real

    def estou_vivo(self):
        return self.vida > 0

    def curar(self, quantidade: int):
        vida_antes = self.__vida
        self.vida = min(self.vida + quantidade, self.vida_max)
        vida_curada_real = self.vida - vida_antes
        return vida_curada_real