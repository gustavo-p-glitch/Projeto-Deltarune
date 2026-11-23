import pygame
import os
from jogo import recursos

class VisaoSelecaoInimigo:
    def __init__(self):
        try:
            caminho_fonte = recursos.fonte()

            self.fonte_titulo = pygame.font.Font(caminho_fonte, 40)
            self.fonte_menu = pygame.font.Font(caminho_fonte, 32)
            self.fonte_prompt = pygame.font.Font(caminho_fonte, 24)
            self.fonte_erro = pygame.font.Font(caminho_fonte, 26)
            self.fonte_relatorio = pygame.font.Font(caminho_fonte, 20)

        except Exception:
            self.fonte_titulo = pygame.font.Font(None, 40)
            self.fonte_menu = pygame.font.Font(None, 32)
            self.fonte_prompt = pygame.font.Font(None, 24)
            self.fonte_erro = pygame.font.Font(None, 26)
            self.fonte_relatorio = pygame.font.Font(None, 20)

        try:
            self.imagem_alma_menu = pygame.image.load(recursos.imagem("soul2.png")).convert_alpha()
        except (pygame.error, FileNotFoundError):
            self.imagem_alma_menu = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(self.imagem_alma_menu, (255, 0, 0), (10, 10), 10)

    def desenhar(self, superficie: pygame.Surface, estado: str, dados_menu: dict, dados_formulario: dict, dados_relatorios: list,
             mensagem_erro: str):

        if estado == "SELECT":
            self.desenhar_menu_selecao(superficie, dados_menu, "Selecione o Inimigo", eh_exclusao=False)
        elif estado == "CREATE":
            self.desenhar_formulario_criacao(superficie, dados_formulario, mensagem_erro)
        elif estado == "DELETE":
            self.desenhar_menu_selecao(superficie, dados_menu, "Qual inimigo Excluir?", eh_exclusao=True)
        elif estado == "VIEW_REPORTS":
            self.desenhar_lista_relatorios(superficie, dados_relatorios)

    def desenhar_menu_selecao(self, superficie, dados_menu: dict, titulo: str, eh_exclusao: bool):
        opcoes = dados_menu['opcoes']
        indice_selecionado = dados_menu['indice_selecionado']
        titulo_surf = self.fonte_titulo.render(titulo, True, (255, 255, 255))
        superficie.blit(titulo_surf, (100, 50))
        x_base, y_base = 150, 150
        alma_x = x_base - 40
        alma_y = y_base + (indice_selecionado * 40) - 2
        superficie.blit(self.imagem_alma_menu, (alma_x, alma_y))

        for i, nome in enumerate(opcoes):
            cor = (255, 255, 255)
            if eh_exclusao and i == indice_selecionado:
                cor = (255, 0, 0)
            elif i == indice_selecionado:
                cor = (255, 255, 0)

            texto_surf = self.fonte_menu.render(nome, True, cor)
            superficie.blit(texto_surf, (x_base, y_base + i * 40))

        texto_prompt = "Use [Setas], [Z] Confirmar, [X] Voltar"
        prompt_surf = self.fonte_prompt.render(texto_prompt, True, (150, 150, 150))
        superficie.blit(prompt_surf, (100, 500))

    def desenhar_formulario_criacao(self, superficie, dados_formulario: dict, mensagem_erro: str):
        campos = dados_formulario['campos']
        valores = dados_formulario['valores']
        indice_ativo = dados_formulario['indice_ativo']

        titulo_surf = self.fonte_titulo.render("Criar Novo Inimigo", True, (255, 255, 255))
        superficie.blit(titulo_surf, (100, 50))

        for i, nome_campo in enumerate(campos):
            valor_campo = valores.get(nome_campo, "")
            cor = (255, 255, 255)
            prefixo = "  "

            if i == indice_ativo:
                cor = (255, 255, 0)
                prefixo = "> "
                valor_campo += "|"

            texto = f"{prefixo}{nome_campo.capitalize()}: {valor_campo}"
            texto_surf = self.fonte_menu.render(texto, True, cor)
            superficie.blit(texto_surf, (150, 150 + i * 40))

        if mensagem_erro:
            erro_surf = self.fonte_erro.render(mensagem_erro, True, (255, 100, 100))
            erro_rect = erro_surf.get_rect(center=(superficie.get_width() / 2, 460))
            superficie.blit(erro_surf, erro_rect)

        prompt_surf = self.fonte_prompt.render("Navegar: Setas | Salvar: Enter | Cancelar: Esc", True, (150, 150, 150))
        superficie.blit(prompt_surf, (100, 500))

    def desenhar_lista_relatorios(self, superficie, dados_relatorios: list):
        titulo_surf = self.fonte_titulo.render("Relatórios", True, (255, 255, 255))
        superficie.blit(titulo_surf, (100, 50))

        if not dados_relatorios:
            sem_surf = self.fonte_menu.render("Vazio.", True, (150, 150, 150))
            superficie.blit(sem_surf, (150, 150))

        x_base, y_base = 100, 150
        for i, rep in enumerate(dados_relatorios[:8]):
            resultado = 'Poupado' if rep.get('poupado') else ('Vitória' if rep['vitoria'] else 'Derrota')
            contra = f" vs {rep['inimigo']}" if rep.get('inimigo') else ""
            texto = f"{rep['data']}{contra} - {resultado} (Turnos: {rep['turnos']})"
            cor = (0, 255, 0) if rep['vitoria'] else (255, 100, 100)
            linha_surf = self.fonte_relatorio.render(texto, True, cor)
            superficie.blit(linha_surf, (x_base, y_base + i * 35))

        prompt_surf = self.fonte_prompt.render("[X] Voltar", True, (150, 150, 150))
        superficie.blit(prompt_surf, (100, 550))