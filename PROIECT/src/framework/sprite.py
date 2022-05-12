import pygame

from .rendered_object import RenderedObject


class Sprite(RenderedObject):
    
    def __init__(
        self, 
        image: pygame.surface.Surface,
        posX: int, 
        posY: int, 
        width: int, 
        height: int
    ) -> None:
        super().__init__(posX, posY, width, height)
        self.texture = pygame.transform.scale(image, (width, height))
    

    def SetAlphaLevel(self, alpha: int) -> None:
        self.texture.set_alpha(alpha)


    def ChangeSize(self, width: int, height: int) -> None:
        super().ChangeSize(width, height)
        self.texture = pygame.transform.scale(self.texture, (width, height))

    def _Draw(self) -> None:
        pygame.display.get_surface().blit(self.texture, self._frame.topleft)
