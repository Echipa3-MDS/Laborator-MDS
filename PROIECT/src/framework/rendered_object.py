from typing import Tuple
import pygame


class RenderedObject:

    def __init__(self, posX: int, posY: int, width: int, height: int) -> None:
        self._frame = pygame.Rect(posX, posY, width, height)
        self._relativePos = pygame.math.Vector2(posX, posY)
        
        self._children = []
    

    def AttachObject(self, object: 'RenderedObject') -> None:
        if object not in self._children:
            self._children.append(object)
            toMove = pygame.math.Vector2(self._frame.left, self._frame.top)
            self._children[-1].MoveBy(toMove)

    
    def DetachObject(self, object: 'RenderedObject') -> None:
        if object in self._children:
            self._children.remove(object)
            toMove = pygame.math.Vector2(-self._frame.left, -self._frame.top)
            object.MoveBy(toMove)


    def MoveBy(self, moveAmount: pygame.math.Vector2) -> None:
        parentPos = pygame.math.Vector2(self._frame.left - int(self._relativePos[0]), self._frame.top - int(self._relativePos[1]))
        self._relativePos += moveAmount
        self._frame.topleft = parentPos + self._relativePos

        for childObject in self._children:
            childObject.MoveBy(moveAmount)


    def SetAlphaLevel(self, alpha: int) -> None:
        # Implementata de tipurile derivate
        pass


    def ChangeRelativePos(self, position: pygame.math.Vector2) -> None:
        self.MoveBy(position - self._relativePos)


    def ChangeSize(self, width: int, height: int) -> None:
        self._frame.width = width
        self._frame.height = height

    
    def GetRelativePos(self) -> pygame.math.Vector2:
        return self._relativePos

    
    def GetDisplayPos(self) -> pygame.math.Vector2:
        decimals = pygame.math.Vector2(self._relativePos[0] % 1, self._relativePos[1] % 1)
        return self._frame.topleft + decimals


    def GetSize(self) -> Tuple[int, int]:
        return self._frame.size


    def GetRect(self) -> pygame.Rect:
        return self._frame
    

    def _Draw(self) -> None:
        # Implementata de tipurile derivate
        pass


    def _Visit(self) -> None:
        self._Draw()
        for childObject in self._children:
            childObject._Visit()
