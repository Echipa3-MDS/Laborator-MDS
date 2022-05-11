import pygame

from .rendered_object import RenderedObject
from .constants import *


class Scene(RenderedObject):

    def __init__(self) -> None:
        super().__init__(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.bgColor = pygame.Color(255, 255, 255)
        self.bgImage = None


    def DrawScene(self) -> None:
        self._Visit()
        pygame.display.update()


    def ChangeBgImage(self, image: pygame.surface.Surface) -> None:
        self.bgImage = image


    def ChangeBgColor(self, color: pygame.Color) -> None:
        self.bgColor = color


    def OnSceneExit(self) -> None:
        # Implementata de tipurile derivate
        pass


    def _Draw(self) -> None:
        if self.bgImage is not None:
            pygame.display.get_surface().blit(self.bgImage, self._frame)
        else:
            pygame.display.get_surface().fill(self.bgColor)
