from tkinter import N
import pygame

from framework.rendered_object import RenderedObject


class TextObject(RenderedObject):

    def __init__(
        self,
        text: str,
        textColor: pygame.Color,
        sysFont: pygame.font.Font,
        fontSize: int, 
        posX: int, 
        posY: int,
    ) -> None:
        super().__init__(posX, posY, 0, 0)

        self.text = text
        self.textColor = textColor
        
        self.font = pygame.font.SysFont(sysFont, fontSize)
        self.textSurface = self.font.render(text, True, textColor)

        self._frame.width = self.textSurface.get_width()
        self._frame.height = self.textSurface.get_height()
    

    def ChangeText(self, text: str, textColor: pygame.Color = (255, 255, 255)) -> None:
        if self.text == text and self.textColor == textColor:
            return
        self.text = text
        self.textColor = textColor
        self.textSurface = self.font.render(self.text, True, self.textColor)


    def _Draw(self) -> None:
        pygame.display.get_surface().blit(self.textSurface, self._frame.topleft)


