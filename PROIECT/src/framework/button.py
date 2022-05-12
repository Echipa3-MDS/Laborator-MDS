from typing import Tuple
import pygame

from framework.rendered_object import RenderedObject


class Button(RenderedObject):

    def __init__(
        self,
        posX: int, 
        posY: int, 
        width: int, 
        height: int,
        text: str = None,
        textColor: pygame.Color = (255, 255, 255),
        sysFont: str = None,
        fontSize: int = 12,
        bgImagePath: str = None,
        bgColor: pygame.Color = None,
        buttonBorderRadius: int = -1
    ) -> None:
        super().__init__(posX, posY, width, height)

        self.font = None
        if sysFont is not None:
            self.font = pygame.font.SysFont(sysFont, fontSize)
        
        self.text = text
        self.textColor = textColor
        self.textSurface = None
        if self.text is not None and self.font is not None:
            self.textSurface = self.font.render(self.text, True, self.textColor)
            self.textPos = (self._frame.centerx - self.textSurface.get_width() / 2, self._frame.centery - self.textSurface.get_height() / 2)
        
        self.bgColor = bgColor
        self.borderRadius = buttonBorderRadius
        self.bgImage = None
        if bgImagePath is not None:
            self.bgImage = pygame.image.load(bgImagePath)

    
    def ChangeSize(self, width: int, height: int) -> None:
        super().ChangeSize(width, height)
        if self.textSurface is not None:
            self.textPos = (self._frame.centerx - self.textSurface.get_width() / 2, self._frame.centery - self.textSurface.get_height() / 2)
        if self.bgImage is not None:
            self.bgImage = self.bgImage = pygame.transform.scale(self.bgImage, self._frame.size)


    def ChangeRelativePos(self, position: pygame.math.Vector2) -> None:
        super().ChangeRelativePos(position)
        if self.textSurface is not None:
            self.textPos = (self._frame.centerx - self.textSurface.get_width() / 2, self._frame.centery - self.textSurface.get_height() / 2)


    def SetText(self, text: str, textColor: pygame.Color = (255, 255, 255)) -> None:
        self.text = text
        self.textColor = textColor
        if self.font is not None:
            self.textSurface = self.textSurface = self.font.render(text, True, textColor)
            self.textPos = (self._frame.centerx - self.textSurface.get_width() / 2, self._frame.centery - self.textSurface.get_height() / 2)


    def SetSysFont(self, font: str, fontSize: int) -> None:
        self.font = pygame.font.SysFont(font, fontSize)
        if self.text is not None:
            self.textSurface = self.textSurface = self.font.render(self.text, True, self.textColor)
            self.textPos = (self._frame.centerx - self.textSurface.get_width() / 2, self._frame.centery - self.textSurface.get_height() / 2)


    def SetCustomFont(self, fontPath: str, fontSize: int) -> None:
        self.font = pygame.font.Font(fontPath, fontSize)
        if self.text is not None:
            self.textSurface = self.textSurface = self.font.render(self.text, True, self.textColor)
            self.textPos = (self._frame.centerx - self.textSurface.get_width() / 2, self._frame.centery - self.textSurface.get_height() / 2)


    def SetBgImage(self, imagePath: str) -> None:
        image = pygame.image.load(imagePath)
        self.bgImage = pygame.transform.scale(image, self._frame.size)

    
    def SetBgColor(self, color: pygame.Color, buttonBorderRadius: int = -1) -> None:
        self.bgColor = color
        self.borderRadius = buttonBorderRadius


    def CollidesWithPoint(self, point: Tuple[int, int]) -> bool:
        return self._frame.collidepoint(point)


    def _Draw(self) -> None:
        display = pygame.display.get_surface()

        if self.bgImage is not None:
            display.blit(self.bgImage, self._frame.topleft)
        elif self.bgColor is not None:
            pygame.draw.rect(display, self.bgColor, self._frame, 0, self.borderRadius)
        
        if self.textSurface is not None:
            display.blit(self.textSurface, self.textPos)
