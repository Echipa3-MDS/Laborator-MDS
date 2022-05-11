import pygame

from framework.rendered_object import RenderedObject


class Button(RenderedObject):

    def __init__(
        self,
        posX: int, 
        posY: int, 
        width: int, 
        height: int,
        text: str,
        textColor: pygame.Color,
        sysFont: pygame.font.Font,
        fontSize: int,
        bgColor: pygame.Color = None,
        bgImage: str = None,
        borderRadius: int = -1 
    ) -> None:
        super().__init__(posX, posY, width, height)

        self.font = pygame.font.SysFont(sysFont, fontSize)
        self.textSurface = self.font.render(text, True, textColor)
        self.textPos = (self._frame.centerx - self.textSurface.get_width() / 2, self._frame.centery - self.textSurface.get_height() / 2)        

        self.bgColor = bgColor
        self.borderRadius = borderRadius
        self.bgImage = None
        if bgImage is not None:
            image = pygame.image.load(bgImage)
            self.bgImage = pygame.transform.scale(image, self._frame.size)


    def ChangeSize(self, width: int, height: int) -> None:
        super().ChangeSize(width, height)
        self.textPos = (self._frame.centerx - self.textSurface.get_width() / 2, self._frame.centery - self.textSurface.get_height() / 2)


    def ChangeRelativePos(self, position: pygame.math.Vector2) -> None:
        super().ChangeRelativePos(position)
        self.textPos = (self._frame.centerx - self.textSurface.get_width() / 2, self._frame.centery - self.textSurface.get_height() / 2)


    def _Draw(self) -> None:
        display = pygame.display.get_surface()
        if self.bgImage is not None:
            display.blit(self.bgImage, self._frame.topleft)
        elif self.bgColor is not None:
            pygame.draw.rect(display, self.bgColor, self._frame, 0, self.borderRadius)
        display.blit(self.textSurface, self.textPos)


