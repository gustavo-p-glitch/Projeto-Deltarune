import os
import math
import pygame
from jogo import recursos
from jogo.visao import gerador_botoes
class VisaoBatalha:
    """Layout (tela 800x600):

        y  10-160  inimigo, no centro
        y 160-400  caixa de texto (200-350) / caixa de batalha (160-400), no meio
        y 390-490  party, cada um em cima do seu painel de HP
        y 494-540  painéis de HP da party
        y 548-592  botões LUTAR / AGIR / ITEM / POUPAR
    """

    RECT_CAIXA_TEXTO = pygame.Rect(20, 200, 760, 150)
    Y_PAINEIS = 494
    ALTURA_PAINEL = 46
    Y_BOTOES = 548
    VELOCIDADE_TEXTO = 50  # caracteres por segundo (efeito de digitação)
    COR_BORDA_CAIXA = (255, 255, 255)

    ESTADOS_CAIXA_BATALHA = ("ENEMY_PREPARO", "ENEMY_TURN")

    def __init__(self, largura_tela, altura_tela, arquivo_musica=None):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

        try:
            caminho_fonte = recursos.fonte()
            self.fonte = pygame.font.Font(caminho_fonte, 26)
            self.fonte_pequena = pygame.font.Font(caminho_fonte, 20)
            self.fonte_balao = pygame.font.Font(caminho_fonte, 18)
        except (pygame.error, FileNotFoundError):
            self.fonte = pygame.font.Font(None, 30)
            self.fonte_pequena = pygame.font.Font(None, 24)
            self.fonte_balao = pygame.font.Font(None, 22)

        self.coracao = self._carregar_coracao()
        self.botoes = self._carregar_botoes()

        # Estado do efeito de digitação
        self._mensagens_alvo = None
        self._linhas = []
        self._caracteres_visiveis = 0.0
        self._total_caracteres = 0

        # Caixa animada (interpola entre caixa de texto e caixa de batalha)
        self._caixa = [float(v) for v in self.RECT_CAIXA_TEXTO]
        self._tempo = 0

        self.arquivo_musica = arquivo_musica
        self.musica_carregada = False
        self.carregar_musica()

    # ------------------------------------------------------------------ assets
    def _carregar_coracao(self):
        try:
            img = pygame.image.load(recursos.imagem("soul2.png")).convert_alpha()
            return img.subsurface(img.get_bounding_rect()).copy()
        except (pygame.error, FileNotFoundError):
            img = pygame.Surface((16, 16), pygame.SRCALPHA)
            pygame.draw.circle(img, (255, 0, 0), (8, 8), 8)
            return img

    def _carregar_botoes(self):
        """Usa botoes/*.png se existirem; senão gera na hora (gerador_botoes.py)."""
        botoes = {}
        for nome in gerador_botoes.ICONES:
            for selecionado in (False, True):
                arquivo = recursos.botao(f"{nome}{'_sel' if selecionado else ''}.png")
                try:
                    img = pygame.image.load(arquivo).convert_alpha()
                except (pygame.error, FileNotFoundError):
                    img = gerador_botoes.criar_botao(nome, selecionado)
                botoes[(nome, selecionado)] = img
        return botoes

    def carregar_musica(self):
        if not self.arquivo_musica:
            return
        try:
            pygame.mixer.music.load(recursos.audio(self.arquivo_musica))
            pygame.mixer.music.set_volume(0.3)
            self.musica_carregada = True
        except pygame.error as e:
            print(f"[aviso] música '{self.arquivo_musica}' não carregou: {e}")

    def iniciar_musica(self):
        if self.musica_carregada:
            pygame.mixer.music.play(-1)

    def parar_musica(self):
        if self.musica_carregada:
            pygame.mixer.music.fadeout(500)

    # ------------------------------------------------------------- atualização
    def atualizar(self, dt, estado, mensagens, rect_batalha):
        self._tempo += dt

        chave = tuple(mensagens)
        if chave != self._mensagens_alvo:
            self._mensagens_alvo = chave
            self._linhas = self._quebrar_mensagens(mensagens)
            self._total_caracteres = sum(len(l) for l in self._linhas)
            self._caracteres_visiveis = 0.0
        self._caracteres_visiveis += self.VELOCIDADE_TEXTO * dt / 1000

        alvo = rect_batalha if estado in self.ESTADOS_CAIXA_BATALHA else self.RECT_CAIXA_TEXTO
        fator = min(1.0, dt / 1000 * 12)
        for i, v in enumerate(alvo):
            self._caixa[i] += (v - self._caixa[i]) * fator
            if abs(v - self._caixa[i]) < 1:
                self._caixa[i] = float(v)

    def texto_completo(self):
        return self._caracteres_visiveis >= self._total_caracteres

    def completar_texto(self):
        self._caracteres_visiveis = self._total_caracteres

    def caixa_atual(self):
        return pygame.Rect(*[round(v) for v in self._caixa])

    def caixa_pronta(self, rect_batalha):
        return self.caixa_atual() == rect_batalha

    def _quebrar_mensagens(self, mensagens):
        """Cada mensagem vira um parágrafo começando com '* ' (estilo Undertale)."""
        largura_max = self.RECT_CAIXA_TEXTO.width - 60
        linhas = []
        for msg in mensagens:
            prefixo, palavras = "* ", []
            texto = str(msg).strip()
            if texto.startswith("*"):  # já veio com asterisco no JSON -> não duplica
                texto = texto[1:].strip()
            for palavra in texto.split():
                candidata = prefixo + " ".join(palavras + [palavra])
                if palavras and self.fonte.size(candidata)[0] > largura_max:
                    linhas.append(prefixo + " ".join(palavras))
                    prefixo, palavras = "  ", [palavra]
                else:
                    palavras.append(palavra)
            linhas.append(prefixo + " ".join(palavras))
        return linhas[:4]  # cabem 4 linhas na caixa

    # ----------------------------------------------------------------- desenho
    def desenhar(self, superficie, estado, dados_jogadores, dados_menu, fala_inimigo, rect_inimigo):
        caixa = self.caixa_atual()
        pygame.draw.rect(superficie, (0, 0, 0), caixa)
        pygame.draw.rect(superficie, self.COR_BORDA_CAIXA, caixa, 3)

        if caixa == self.RECT_CAIXA_TEXTO and estado not in self.ESTADOS_CAIXA_BATALHA:
            if estado in ("PLAYER_SELECT_AGIR", "PLAYER_SELECT_ITEM"):
                self._desenhar_submenu(superficie, dados_menu.get('submenu', {}))
            else:
                self._desenhar_texto(superficie)

        self._desenhar_paineis(superficie, dados_jogadores, estado)
        self._desenhar_botoes(superficie, estado, dados_menu)

        if estado == "ENEMY_TURN" and fala_inimigo:
            self._desenhar_balao(superficie, fala_inimigo, rect_inimigo)

    def _desenhar_texto(self, superficie):
        restantes = int(self._caracteres_visiveis)
        x = self.RECT_CAIXA_TEXTO.x + 24
        y = self.RECT_CAIXA_TEXTO.y + 18
        for linha in self._linhas:
            if restantes <= 0:
                break
            visivel = linha[:restantes]
            restantes -= len(linha)
            superficie.blit(self.fonte.render(visivel, False, (255, 255, 255)), (x, y))
            y += 31

    def _desenhar_submenu(self, superficie, submenu):
        opcoes = submenu.get('opcoes', [])
        descricoes = submenu.get('descricoes', [])
        idx = submenu.get('indice_selecionado', 0)
        x = self.RECT_CAIXA_TEXTO.x + 60
        y = self.RECT_CAIXA_TEXTO.y + 18

        if not opcoes:
            superficie.blit(self.fonte.render("* (vazio)", False, (150, 150, 150)), (x, y))
            return

        for i, nome in enumerate(opcoes[:4]):
            cor = (255, 255, 0) if i == idx else (255, 255, 255)
            superficie.blit(self.fonte.render(f"* {nome}", False, cor), (x, y + i * 31))
        coracao_rect = self.coracao.get_rect(midright=(x - 10, y + idx * 31 + 14))
        superficie.blit(self.coracao, coracao_rect)

        if idx < len(descricoes) and descricoes[idx]:
            texto = self.fonte_pequena.render(descricoes[idx], False, (160, 160, 160))
            superficie.blit(texto, texto.get_rect(topright=(self.RECT_CAIXA_TEXTO.right - 24, y + 4)))

    def _desenhar_paineis(self, superficie, dados_jogadores, estado):
        n = max(1, len(dados_jogadores))
        espaco = 8
        largura = (self.RECT_CAIXA_TEXTO.width - espaco * (n - 1)) // n
        for i, p in enumerate(dados_jogadores):
            rect = pygame.Rect(self.RECT_CAIXA_TEXTO.x + i * (largura + espaco), self.Y_PAINEIS,
                               largura, self.ALTURA_PAINEL)
            cor = p.get('cor', (255, 255, 255))
            ativo = p.get('ativo', False)

            pygame.draw.rect(superficie, (0, 0, 0), rect)
            pygame.draw.rect(superficie, cor if ativo else (90, 90, 90), rect, 3 if ativo else 1)

            cor_nome = cor if p['vivo'] else (120, 120, 120)
            nome = p['nome'].upper() + ("  DEF" if p['defesa'] and p['vivo'] else "")
            superficie.blit(self.fonte_pequena.render(nome, False, cor_nome), (rect.x + 10, rect.y + 4))

            # Barra de HP
            barra = pygame.Rect(rect.x + 10, rect.y + 28, rect.width - 120, 10)
            pygame.draw.rect(superficie, (100, 0, 0), barra)
            if p['vivo'] and p['max'] > 0:
                cheio = barra.copy()
                cheio.width = max(1, round(barra.width * p['vida'] / p['max']))
                pygame.draw.rect(superficie, (255, 220, 0) if ativo else cor, cheio)

            texto_hp = f"{p['vida']}/{p['max']}" if p['vivo'] else "CAÍDO"
            cor_hp = (255, 255, 255) if p['vivo'] else (200, 60, 60)
            hp = self.fonte_pequena.render(texto_hp, False, cor_hp)
            superficie.blit(hp, hp.get_rect(midright=(rect.right - 10, rect.y + 31)))

    def _desenhar_botoes(self, superficie, estado, dados_menu):
        opcoes = dados_menu.get('opcoes', [])
        idx = dados_menu.get('indice_selecionado', 0)
        escolhendo = estado.startswith("PLAYER_SELECT")
        no_menu_principal = estado == "PLAYER_SELECT"

        n = max(1, len(opcoes))
        largura = gerador_botoes.TAMANHO_BOTAO[0]
        espaco = (self.largura_tela - n * largura) // (n + 1)
        for i, opcao in enumerate(opcoes):
            nome = gerador_botoes.MAPA_OPCOES.get(opcao, "agir")
            selecionado = escolhendo and i == idx
            img = self.botoes[(nome, selecionado)]
            x = espaco + i * (largura + espaco)
            superficie.blit(img, (x, self.Y_BOTOES))

            if selecionado:
                ix, iy = gerador_botoes.POS_ICONE
                tam_icone = 13 * gerador_botoes.ESCALA_ICONE
                centro = (x + ix + tam_icone // 2, self.Y_BOTOES + iy + tam_icone // 2)
                if no_menu_principal:
                    # Coração no lugar do ícone, como no Undertale
                    superficie.blit(self.coracao, self.coracao.get_rect(center=centro))
                else:
                    # No submenu o coração está dentro da caixa; o botão mostra o ícone
                    icone = gerador_botoes.desenhar_icone(nome, gerador_botoes.COR_SELECIONADO)
                    superficie.blit(icone, icone.get_rect(center=centro))

    def _desenhar_balao(self, superficie, falas, rect_inimigo):
        linhas = []
        for fala in falas:
            atual = ""
            for palavra in fala.split():
                tentativa = (atual + " " + palavra).strip()
                if self.fonte_balao.size(tentativa)[0] > 150 and atual:
                    linhas.append(atual)
                    atual = palavra
                else:
                    atual = tentativa
            linhas.append(atual)

        altura = 14 + len(linhas) * 20
        rect = pygame.Rect(0, 0, 170, altura)
        # Balão à direita do inimigo, com a ponta apontando pra ele
        rect.midleft = (rect_inimigo.right + 14, rect_inimigo.centery - 20)
        pygame.draw.rect(superficie, (255, 255, 255), rect, border_radius=6)
        ponta = [(rect.left + 2, rect.centery - 6), (rect.left + 2, rect.centery + 6),
                 (rect.left - 12, rect.centery)]
        pygame.draw.polygon(superficie, (255, 255, 255), ponta)
        for i, linha in enumerate(linhas):
            superficie.blit(self.fonte_balao.render(linha, False, (0, 0, 0)), (rect.x + 8, rect.y + 7 + i * 20))
