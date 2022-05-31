import pygame
from framework.rendered_object import RenderedObject

class Box(RenderedObject):
    def __init__(
        self,
        posX: int, 
        posY: int, 
        width: int, 
        height: int,
        bgColor: pygame.Color = None,
        bgImage: str = None,
        borderRadius: int = -1 
    ) -> None:
        super().__init__(posX, posY, width, height)

        self.bgColor = None
        if bgColor is not None:
            self.bgColor = pygame.Surface(self._frame.size)
            self.bgColor.fill(bgColor)

        self.borderRadius = borderRadius
        self.bgImage = None
        if bgImage is not None:
            image = pygame.image.load(bgImage)
            self.bgImage = pygame.transform.scale(image, self._frame.size)

    def SetAlphaLevel(self, alpha: int) -> None:
        if self.bgImage is not None:
            self.bgImage.set_alpha(alpha)
        if self.bgColor is not None:
            self.bgColor.set_alpha(alpha)

    def _Draw(self) -> None:
        display = pygame.display.get_surface()
        
        if self.bgImage is not None:
            display.blit(self.bgImage, self._frame.topleft)
        elif self.bgColor is not None:
            display.blit(self.bgColor, self._frame.topleft)
