from jogo.modelo.projetil import Projetil
from jogo.visao.visao_projetil import VisaoProjetil


class ControladorProjetil:
    """Liga a visão a um Projetil que JÁ existe no ModeloBatalha.

    Antes, o controlador criava um segundo Projetil: o modelo calculava a colisão
    com um (20x20) e a tela desenhava outro (tamanho da imagem), que ainda andava
    em dobro. Agora existe um projétil só — o modelo move/colide, aqui só se desenha.
    """

    def __init__(self, projetil: Projetil, imagem: str):
        self._projetil = projetil
        self.visao = VisaoProjetil(imagem)

        if projetil.tamanho_definido:
            # Tamanho veio do ataque (ex: parede de ossos) -> imagem se adapta.
            self.visao.ajustar_tamanho(projetil.rect.size)
        else:
            # Sem tamanho -> hitbox assume o tamanho da imagem.
            projetil.rect.size = self.visao.imagem.get_size()

    @property
    def modelo(self):
        return self._projetil

    def requisitar_desenho(self, superficie):
        if self._projetil.ativa:
            self.visao.desenhar(superficie, self._projetil)
