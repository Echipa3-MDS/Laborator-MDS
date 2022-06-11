import pygame
import random
from os.path import join as pathJoin

from framework.sprite import Sprite
from framework.constants import *
from framework.update_scheduler import UpdateScheduler
import game.game_session as gs


class RayWave:
    def __init__(self, gameScene: 'gs.GameSession') -> None:
        self.gameScene = gameScene

        self.rayHeight = 40
        self.rayOff = pygame.image.load(pathJoin(RES_STATIC_TEXTURES_DIR, 'beam', 'beam_off.bmp')).convert_alpha()
        self.rayOffWidth = 47
        self.rayOn = pygame.image.load(pathJoin(RES_STATIC_TEXTURES_DIR, 'beam', 'beam_on.bmp')).convert_alpha()
        self.rayOnWidth = self.rayOn.get_width() + 6

        self.rayOffDuration = 2.5
        self.rayOnDuration = 2
        self.rayOffTimeElapsed = 0.0
        self.rayOnTimeElapsed = 0.0
        self.maxNrOfRays = DISPLAY_HEIGHT // self.rayHeight
        self.nrOmittedRays = 3
        self.nrOfRays = self.maxNrOfRays - self.nrOmittedRays
        self.rays = []
        self.rayOnPixelMask = pygame.mask.from_surface(pygame.transform.scale(self.rayOn, (self.rayOnWidth, self.rayHeight)))

        self.hasCoins = False

        self.scheduler = UpdateScheduler.GetInstance()
        self.ResetWave()


    def SetActive(self) -> None:
        if self.rayOffTimeElapsed < self.rayOffDuration:
            self.scheduler.ScheduleUpdate(self.UpdateRayOff)
        else:
            self.scheduler.ScheduleUpdate(self.UpdateRayOn)


    def CleanUp(self):
        self.scheduler.UnscheduleUpdate(self.UpdateRayOff)
        self.scheduler.UnscheduleUpdate(self.UpdateRayOn)
        for ray in self.rays:
            self.gameScene.gameLayer.DetachObject(ray)

    
    def UpdateRayOff(self, deltaTime: float) -> None:
        self.rayOffTimeElapsed += deltaTime
        if self.rayOffTimeElapsed >= self.rayOffDuration:
            self.scheduler.UnscheduleUpdate(self.UpdateRayOff)
            
            for i in range(self.nrOfRays):
                self.gameScene.gameLayer.DetachObject(self.rays[i])
                rayOffPos = self.rays[i].GetRelativePos()
                self.rays[i] = Sprite(self.rayOn, rayOffPos.x, rayOffPos.y, self.rayOnWidth, self.rayHeight)
                self.gameScene.gameLayer.AttachObject(self.rays[i])
            
            self.scheduler.ScheduleUpdate(self.UpdateRayOn)
            

    def UpdateRayOn(self, deltaTime: float) -> None:
        self.rayOnTimeElapsed += deltaTime
        if self.rayOnTimeElapsed >= self.rayOnDuration:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT))


    def ResetWave(self) -> None:
        self.rayOffTimeElapsed = 0.0
        self.rayOnTimeElapsed = 0.0

        omittedStartPos = random.randint(0, self.nrOfRays)
        part1 = [Sprite(self.rayOff, 0, i * self.rayHeight, self.rayOffWidth, self.rayHeight) for i in range(omittedStartPos)]
        part2 = [Sprite(self.rayOff, 0, i * self.rayHeight, self.rayOffWidth, self.rayHeight) for i in range(omittedStartPos + self.nrOmittedRays, self.maxNrOfRays, 1)]
        self.rays = part1 + part2
        for ray in self.rays:
            self.gameScene.gameLayer.AttachObject(ray)
        

    def CheckCollision(self, playerPixelMask: pygame.mask.Mask, playerRect: pygame.Rect) -> bool:
        if self.rayOffTimeElapsed >= self.rayOffDuration:
            for i in range(self.nrOfRays):
                rayRect = self.rays[i].GetRect()
                rayOffset = (rayRect.x - playerRect.x, rayRect.y - playerRect.y)
                if playerPixelMask.overlap(self.rayOnPixelMask, rayOffset) is not None:
                    return True
        return False
