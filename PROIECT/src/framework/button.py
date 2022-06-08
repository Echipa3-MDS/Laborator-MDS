from typing import Tuple
import pygame

from framework.rendered_object import RenderedObject
from framework.constants import RES_DIR

class Button(RenderedObject):

    def __init__(
        self,
        posX: int, 
        posY: int, 
        width: int, 
        height: int,
        text: str = None,
        textColor: pygame.Color = (255, 255, 255),
        font: str = None,
        fontSize: int = 12,
        bgImagePath: str = None,
        bgColor: pygame.Color = None,
        sound: str = RES_DIR + "audio/Click.ogg"
    ) -> None:
        super().__init__(posX, posY, width, height)

        self.font = None
        if font is not None:
            if '.' in font:
                self.font = pygame.font.Font(font, fontSize)
            else:
                self.font = pygame.font.SysFont(font, fontSize)
        
        self.text = text
        self.textColor = textColor
        self.textSurface = None
        if self.text is not None and self.font is not None:
            self.textSurface = self.font.render(self.text, True, self.textColor)
        
        self.bgColor = None
        if bgColor is not None:
            self.bgColor = pygame.Surface(self._frame.size)
            self.bgColor.fill(bgColor)
        self.bgImage = None
        if bgImagePath is not None:
            image = pygame.image.load(bgImagePath)
            self.bgImage = pygame.transform.scale(image, self._frame.size)
        if sound is not None:
            self.sound = pygame.mixer.Sound(sound)


    
    def ChangeSize(self, width: int, height: int) -> None:
        super().ChangeSize(width, height)
        if self.bgImage is not None:
            self.bgImage = self.bgImage = pygame.transform.scale(self.bgImage, self._frame.size)


    def SetText(self, text: str, textColor: pygame.Color = (255, 255, 255)) -> None:
        self.text = text
        self.textColor = textColor
        if self.font is not None:
            self.textSurface = self.textSurface = self.font.render(text, True, textColor)


    def SetFont(self, font: str, fontSize: int) -> None:
        if '.' in font:
            self.font = pygame.font.Font(font, fontSize)
        else:
            self.font = pygame.font.SysFont(font, fontSize) 
        
        if self.text is not None:
            self.textSurface = self.textSurface = self.font.render(self.text, True, self.textColor)


    def SetBgImage(self, image: str | pygame.Surface) -> None:
        if type(image) is str:
            imgSurf = pygame.image.load(image)
            self.bgImage = pygame.transform.scale(imgSurf, self._frame.size)
        elif image.get_size() != self._frame.size: 
            self.bgImage = pygame.transform.scale(image, self._frame.size)
        else:
            self.bgImage = image

    
    def SetBgColor(self, color: pygame.Color, buttonBorderRadius: int = -1) -> None:
        if self.bgColor is None:
            self.bgColor = pygame.Surface(self._frame.size)
        self.bgColor.fill(color)


    def SetAlphaLevel(self, alpha: int) -> None:
        if self.bgImage is not None:
            self.bgImage.set_alpha(alpha)
        if self.bgColor is not None:
            self.bgColor.set_alpha(alpha)
        if self.textSurface is not None:
            self.textSurface.set_alpha(alpha)


    def CollidesWithPoint(self, point: Tuple[int, int]) -> bool:
        return self._frame.collidepoint(point)

    def ClickedSound(self, muted) -> None:
        if(not muted):
            self.sound.play()
            

    def _Draw(self) -> None:
        display = pygame.display.get_surface()

        if self.bgImage is not None:
            display.blit(self.bgImage, self._frame.topleft)
        elif self.bgColor is not None:
            display.blit(self.bgColor, self._frame.topleft)
        
        if self.textSurface is not None:
            textPos = (self._frame.centerx - self.textSurface.get_width() / 2, self._frame.centery - self.textSurface.get_height() / 2)
            display.blit(self.textSurface, textPos)
