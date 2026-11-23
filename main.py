from jogo.controlador.controlador_jogo import ControladorJogo

LARGURA = 800
ALTURA = 600

if __name__ == "__main__":
    # O ControladorJogo já faz pygame.init(), cria a janela e chama pygame.quit().
    ControladorJogo(LARGURA, ALTURA).executar()
