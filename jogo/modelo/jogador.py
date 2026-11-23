from jogo.modelo.entidade import Entidade

class Jogador(Entidade):
    def __init__(self, nome: str, magia: int, atk: int, defn: int, vida: int):
        super().__init__(nome, magia, atk, defn)
        self.__vida = vida
        self.vida_max = vida
        self.__magia_max = magia
        self.__habilidades = []
        self.__inventario = []
        self.defn_base = defn
        self.defesa_duracao = 0
        self.__congelado = False

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, vida: int):
        self.__vida = vida

    @property
    def inventario(self):
        return self.__inventario

    @property
    def habilidades(self):
        return self.__habilidades

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

    def aprender_habilidade(self, acao):
        if acao not in self.__habilidades:
            self.__habilidades.append(acao)

    def usar_item(self, nome_item):
        for item in self.__inventario:
            if item.nome == nome_item:
                if item.tipo.nome == "consumivel":
                    # item.executar() já remove do inventário; remover de novo dava ValueError.
                    return item.executar(self, self)
                return {"mensagens": [f"O item {item.nome} não pode ser usado agora."]}
        return {"mensagens": [f"{self.nome} não tem o item {nome_item}."]}

    def atualizar_status(self):
        if self.defesa_duracao > 0:
            self.defesa_duracao -= 1
            if self.defesa_duracao == 0:
                self.defn = self.defn_base

        if self.duracao_fogo > 0:
            dano_fogo = self.dano_fogo
            self.levei_dano(dano_fogo)
            self.duracao_fogo -= 1