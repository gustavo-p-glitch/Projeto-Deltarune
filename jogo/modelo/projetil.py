import pygame


class Projetil:
    # tamanho=None -> o controlador ajusta a hitbox para o tamanho da imagem.
    def __init__(self, x, y, vel_x, vel_y, dano: int, passa=False, tamanho=None):
        self.tamanho_definido = tamanho is not None
        largura, altura = tamanho if tamanho else (20, 20)
        self.rect = pygame.Rect(x, y, largura, altura)
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.dano = dano
        self.passa = passa
        self.ativa = True
        self.tipo_projetil = "osso.png"
        # Projéteis podem nascer fora da caixa (ex: Lancer em x=0) e entrar depois.
        # Só são removidos ao sair DEPOIS de terem entrado.
        self.entrou_na_caixa = False
        self.frames_vida = 0
        self.MAX_FRAMES_FORA = 600  # ~10s a 60fps, evita projétil "perdido" pra sempre

    def mover(self):
        if not self.ativa:
            return
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.frames_vida += 1

    def verificar_colisao(self, rect_alma: pygame.Rect):
        if not self.ativa:
            return False
        return self.rect.colliderect(rect_alma)

    def verificar_limites(self, rect_battle_box: pygame.Rect):
        if not self.ativa:
            return
        dentro = rect_battle_box.colliderect(self.rect)
        if dentro:
            self.entrou_na_caixa = True
        elif self.entrou_na_caixa or self.frames_vida > self.MAX_FRAMES_FORA:
            self.ativa = False
