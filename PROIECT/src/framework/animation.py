import pygame

from .rendered_object import RenderedObject
from .update_scheduler import UpdateScheduler


class Animation(RenderedObject):

    def __init__(
        self, 
        posX: int, 
        posY: int, 
        width: int, 
        height: int,
        textures: list[pygame.surface.Surface],
        transitionTime: float
    ) -> None:
        super().__init__(posX, posY, width, height)
        self.frames = [pygame.transform.scale(texture, (width, height)) for texture in textures]
        self.numberOfFrames = len(self.frames)
        self.frameIndex = 0
        self.timeBetweenFrames = transitionTime
        self.timeSinceChange = 0
        self.updateScheduler = UpdateScheduler.GetInstance()


    def PlayAnimation(self) -> None:
        self.updateScheduler.ScheduleUpdate(self.__updateFrame)
    

    def StopAnimation(self) -> None:
        self.updateScheduler.UnscheduleUpdate(self.__updateFrame)


    def ResetAnimation(self) -> None:
        self.frameIndex = 0
        self.timeSinceChange = 0


    def ChangeTransitionTime(self, transitionTime: float) -> None:
        self.timeBetweenFrames = transitionTime


    def SetAlphaLevel(self, alpha: int) -> None:
        for tex in self.frames:
            tex.set_alpha(alpha)


    def ChangeSize(self, width: int, height: int) -> None:
        super().ChangeSize(width, height)
        self.frames = [pygame.transform.scale(texture, (width, height)) for texture in self.frames]

    def Rotate(self, angle: float) -> 'Animation':
        rotated = [pygame.transform.rotate(texture, angle) for texture in self.frames]
        newAnimation = Animation( 0, 0, rotated[0].get_width(), rotated[0].get_height(), rotated, self.timeBetweenFrames)
        distanceToOldCenter = (self._frame.center[0] - newAnimation._frame.center[0], self._frame.center[1] - newAnimation._frame.center[1])
        newAnimation.ChangeRelativePos(distanceToOldCenter)
        return newAnimation
        
    def __updateFrame(self, deltaTime: float) -> None:
        self.timeSinceChange += deltaTime
        if self.timeSinceChange >= self.timeBetweenFrames:
            self.frameIndex = (self.frameIndex + int(self.timeSinceChange / self.timeBetweenFrames)) % self.numberOfFrames
            self.timeSinceChange = 0


    def _Draw(self) -> None:
        pygame.display.get_surface().blit(self.frames[self.frameIndex], self._frame.topleft)
