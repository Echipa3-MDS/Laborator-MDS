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


    def Rotate(self, angle: float) -> 'Sprite':
        rotated = pygame.transform.rotate(self.texture, angle)
        newSprite = Sprite(rotated, 0, 0, rotated.get_width(), rotated.get_height())
        distanceToOldCenter = (self._frame.center[0] - newSprite._frame.center[0], self._frame.center[1] - newSprite._frame.center[1])
        newSprite.ChangeRelativePos(distanceToOldCenter)
        return newSprite


    def _Draw(self) -> None:
        pygame.display.get_surface().blit(self.texture, self._frame.topleft)
