import random
from jogo.modelo.projetil import Projetil


class SequenciadorDeAtaque:
    def __init__(self, padroes_ataque: list, nome_inimigo: str):
        self.ataque_terminou = False
        self.novos_projeteis = []
        self.novas_mensagens = []
        self.padroes_ataque = padroes_ataque
        self.nome_inimigo = nome_inimigo
        self.padrao_ataque_atual = None
        self.temporizador_ataque = 0.0
        self.indice_evento_ataque_atual = 0

    def iniciar_novo_ataque(self, alma):
        if not self.padroes_ataque:
            self.padrao_ataque_atual = {
                "nome": "AtaqueFallback",
                "duracao_ms": 2000,
                "cor_alma": "vermelho",
                "eventos": [{"tempo_ms": 0, "tipo": "definir_mensagem",
                             "texto": f"Ataques para {self.nome_inimigo} não encontrados!"}]
            }
        else:
            self.padrao_ataque_atual = random.choice(self.padroes_ataque)

        # O loop do atualizar() assume eventos em ordem de tempo.
        self.padrao_ataque_atual["eventos"].sort(key=lambda e: e.get("tempo_ms", 0))

        self.temporizador_ataque = 0.0
        self.indice_evento_ataque_atual = 0
        self.ataque_terminou = False
        self.novos_projeteis = []
        self.novas_mensagens = []

        cor_alma = self.padrao_ataque_atual.get("cor_alma", "vermelho")
        alma.mudar_cor(cor_alma)

        # Antes os eventos de tempo 0 eram processados aqui E de novo no primeiro
        # atualizar() (e a parede de ossos era ignorada aqui por falta da caixa).
        # Agora só lemos as mensagens iniciais; quem cria projéteis é o atualizar().
        mensagens_iniciais = [
            e.get("texto", "...") for e in self.padrao_ataque_atual["eventos"]
            if e.get("tempo_ms", 0) == 0 and e.get("tipo") == "definir_mensagem"
        ]
        if mensagens_iniciais:
            return mensagens_iniciais

        return [f"{self.nome_inimigo} ataca!"]

    def atualizar(self, dt, alma, rect_battle_box, dano_inimigo):
        novos_projeteis_frame = []
        novas_mensagens_frame = []

        if not self.padrao_ataque_atual:
            self.ataque_terminou = True
            return self

        self.temporizador_ataque += dt
        eventos = self.padrao_ataque_atual["eventos"]

        while self.indice_evento_ataque_atual < len(eventos):
            evento = eventos[self.indice_evento_ataque_atual]
            if self.temporizador_ataque < evento["tempo_ms"]:
                break

            if evento.get("tipo") == "definir_mensagem" and evento.get("tempo_ms", 0) == 0:
                # Já mostrada na caixa de texto antes do ataque (iniciar_novo_ataque).
                self.indice_evento_ataque_atual += 1
                continue

            novos_projeteis, novas_mensagens = self.processar_evento_ataque(
                evento, alma, rect_battle_box, dano_inimigo
            )

            if novos_projeteis:
                novos_projeteis_frame.extend(novos_projeteis)
            if novas_mensagens:
                novas_mensagens_frame.extend(novas_mensagens)

            self.indice_evento_ataque_atual += 1

        self.novos_projeteis = novos_projeteis_frame
        self.novas_mensagens = novas_mensagens_frame

        duracao = self.padrao_ataque_atual.get("duracao_ms", 5000)
        if self.temporizador_ataque >= duracao:
            self.ataque_terminou = True

        return self

    def processar_evento_ataque(self, evento: dict, alma, rect_battle_box, dano_inimigo):
        tipo_evento = evento.get("tipo")
        novos_projeteis = []
        novas_mensagens = []

        if tipo_evento == "criar_projetil":
            projetil = self.criar_projetil_simples(evento, dano_inimigo, rect_battle_box)
            if projetil:
                novos_projeteis.append(projetil)

        elif tipo_evento == "definir_mensagem":
            texto = evento.get("texto", "...")
            if texto:
                novas_mensagens.append(texto)

        elif tipo_evento == "criar_parede_ossos":
            if rect_battle_box:
                projeteis_parede = self.criar_parede_ossos(evento, rect_battle_box, dano_inimigo)
                novos_projeteis.extend(projeteis_parede)

        return novos_projeteis, novas_mensagens

    def criar_projetil_simples(self, evento: dict, dano, rect_battle_box=None):
        # x/y no attacks.json são RELATIVOS ao canto superior esquerdo da caixa de
        # batalha: (0, 0) = canto da caixa. Assim a caixa pode mudar de lugar sem
        # quebrar os ataques. Valores negativos/maiores que a caixa = nasce fora dela.
        origem_x, origem_y = rect_battle_box.topleft if rect_battle_box else (0, 0)
        tamanho = None
        if "largura" in evento and "altura" in evento:
            tamanho = (evento["largura"], evento["altura"])

        projetil = Projetil(
            origem_x + evento.get("x", 0),
            origem_y + evento.get("y", 0),
            evento.get("vx", 0),
            evento.get("vy", 5),
            dano,
            passa=evento.get("passa", False),
            tamanho=tamanho
        )
        tipo_projetil = evento.get("tipo_projetil", "osso.png")
        if tipo_projetil == "bone.png":
            tipo_projetil = "osso.png"
        projetil.tipo_projetil = tipo_projetil
        return projetil

    def criar_parede_ossos(self, evento: dict, rect_battle_box, dano):
        try:
            lado = evento.get("lado", "bottom")
            velocidade = evento.get("velocidade", 5)
            tamanho_lacuna = evento.get("tamanho_lacuna", 1)
            pos_lacuna = evento.get("pos_lacuna", 3)
            tamanho_osso = 20
            comprimento_osso = evento.get("comprimento", 40)

            caixa = rect_battle_box
            num_slots = int(caixa.width / (tamanho_osso + 4))

            if pos_lacuna == "aleatoria":
                # Sorteia o buraco, mas nunca no meio — onde a alma começa o turno.
                meio = num_slots // 2
                opcoes = [i for i in range(num_slots - tamanho_lacuna + 1)
                          if not (i - 1 <= meio < i + tamanho_lacuna + 1)]
                pos_lacuna = random.choice(opcoes)

            projeteis_criados = []

            for i in range(num_slots):
                if i >= pos_lacuna and i < (pos_lacuna + tamanho_lacuna):
                    continue

                x, y, vx, vy = 0, 0, 0, 0
                if lado == "bottom":
                    x = caixa.left + i * (tamanho_osso + 4) + 2
                    y = caixa.bottom
                    vx = 0
                    vy = -velocidade
                elif lado == "top":
                    x = caixa.left + i * (tamanho_osso + 4) + 2
                    y = caixa.top - tamanho_osso
                    vx = 0
                    vy = velocidade
                elif lado == "left":
                    x = caixa.left - tamanho_osso
                    y = caixa.top + i * (tamanho_osso + 4) + 2
                    vx = velocidade
                    vy = 0
                elif lado == "right":
                    x = caixa.right
                    y = caixa.top + i * (tamanho_osso + 4) + 2
                    vx = -velocidade
                    vy = 0

                if lado in ("bottom", "top"):
                    tamanho = (tamanho_osso, comprimento_osso)
                    if lado == "top":
                        y = caixa.top - comprimento_osso
                else:
                    tamanho = (comprimento_osso, tamanho_osso)
                    if lado == "left":
                        x = caixa.left - comprimento_osso

                projetil = Projetil(x, y, vx, vy, dano, tamanho=tamanho)
                projetil.tipo_projetil = "osso.png"
                projeteis_criados.append(projetil)

            return projeteis_criados
        except Exception:
            return []