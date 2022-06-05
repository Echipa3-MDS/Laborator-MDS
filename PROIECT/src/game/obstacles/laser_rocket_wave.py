import pygame
import random

from framework.update_scheduler import UpdateScheduler
from framework.sprite import Sprite
from framework.constants import *
from framework.animation import Animation
from game.obstacles.coin_matrix import CoinMatrix
import game.game_session as gs


class LaserRocketWave:
    def __init__(self, gameScene: 'gs.GameSession', haveRockets = True) -> None:
        self.gameScene = gameScene
        
        # Lasere
        self.totalLasers = 12
        self.remainingLasers = 12
        self.gapBetweenLasers = 5 * self.gameScene.playerWalk.GetRect().width

        self.laserWidth = 250
        self.laserHeight = 40
        frameTime = 0.115
        laserImgs = [
            pygame.image.load(RES_DIR + 'img/laser/laser1.png'),
            pygame.image.load(RES_DIR + 'img/laser/laser2.png'),
            pygame.image.load(RES_DIR + 'img/laser/laser3.png'),
            pygame.image.load(RES_DIR + 'img/laser/laser2.png')
        ]
        self.baseLaserSprites = Animation(0, 0, self.laserWidth, self.laserHeight, laserImgs, frameTime)
        self.lasers = []
        self.lasersPixelMasks = []

        # Rachete
        self.haveRockets = haveRockets
        self.warningDuration = 2.0
        self.warningTraceSpeed = 100
        self.rocketSpeed = 200           # Velocitatea rachetei = Velocitatea scenei + viteza rachetei

        self.rocketWidth = 200
        self.rocketHeight = 35
        self.warningWidth = 50
        self.warningHeight = 50
        self.warningImg = pygame.image.load(RES_DIR + 'img/rocket_warning.png')
        self.rocketFrameTime = 0.05
        self.rocketImg = [
            pygame.image.load(RES_DIR + 'img/rocket/rocket1.png'),
            pygame.image.load(RES_DIR + 'img/rocket/rocket2.png'),
            pygame.image.load(RES_DIR + 'img/rocket/rocket3.png'),
            pygame.image.load(RES_DIR + 'img/rocket/rocket2.png')
        ]
        self.currentRocket = None
        self.warningTime = 0.0

        # Bani
        self.hasCoins = True
        self.blockSpawnChance = 35
        self.coinBlocks = []
        self.remainingBlocks = None

        self.ResetWave()


    def SetActive(self) -> None:
        scheduler = UpdateScheduler.GetInstance()
        scheduler.ScheduleUpdate(self.UpdateLasers)
        scheduler.ScheduleUpdate(self.UpdateCoins)
        if self.haveRockets:
            scheduler.ScheduleUpdate(self.UpdateRockets)
        for block in self.coinBlocks:
            block.SetActive()


    def CleanUp(self):
        scheduler = UpdateScheduler.GetInstance()
        scheduler.UnscheduleUpdate(self.UpdateLasers)
        scheduler.UnscheduleUpdate(self.UpdateCoins)
        if self.haveRockets:
            scheduler.UnscheduleUpdate(self.UpdateRockets)
            if self.currentRocket is not None:
                self.gameScene.gameLayer.DetachObject(self.currentRocket)
        for laser in self.lasers:
            self.gameScene.gameLayer.DetachObject(laser)
        for block in self.coinBlocks:
            block.CleanUp()
            self.gameScene.gameLayer.DetachObject(block)


    def UpdateLasers(self, deltaTime: float) -> None:
        moveAmount = pygame.Vector2(self.gameScene.sceneXVelocity * deltaTime, 0)
        for i in range(self.remainingLasers - 1, -1, -1):
            self.lasers[i].MoveBy(moveAmount)

            laserRect = self.lasers[i].GetRect()
            if laserRect.right < 0:
                self.gameScene.gameLayer.DetachObject(self.lasers[i])
                self.lasers.pop(i)
                self.lasersPixelMasks.pop(i)
                self.remainingLasers -= 1
                if self.remainingLasers == 0 and not self.haveRockets:
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT))

    
    def UpdateRockets(self, deltaTime: float) -> None:
        if self.warningTime < self.warningDuration:
            self.warningTime += deltaTime
            
            playerY = self.gameScene.playerState.GetRelativePos().y
            warningY = self.currentRocket.GetRelativePos().y
            traceDirectionY = (-1 if playerY < warningY else 1)
            moveAmountY = min(abs(playerY - warningY), abs(self.warningTraceSpeed * deltaTime)) * traceDirectionY
            
            self.currentRocket.MoveBy((0, moveAmountY))
            if self.warningTime >= self.warningDuration:
               self.__LaunchRocket()
        else:
            moveAmountX = (self.gameScene.sceneXVelocity - self.rocketSpeed) * deltaTime
            self.currentRocket.MoveBy((moveAmountX, 0))
            if self.currentRocket.GetRect().right < 0:
                if self.__LasersEnded():
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT))
                else:
                    self.gameScene.gameLayer.DetachObject(self.currentRocket)
                    self.__ResetRocket()


    def UpdateCoins(self, deltaTime: float) -> None:
        moveAmount = pygame.Vector2(self.gameScene.sceneXVelocity * deltaTime, 0)
        for i in range(self.remainingBlocks - 1, -1, -1):
            self.coinBlocks[i].MoveBy(moveAmount)
            blockRect = self.coinBlocks[i].GetRect()
            if blockRect.right < 0:
                self.coinBlocks[i].CleanUp()
                self.gameScene.gameLayer.DetachObject(self.coinBlocks[i])
                self.coinBlocks.pop(i)
                self.remainingBlocks -= 1


    def ResetWave(self) -> None:
        # Lasere
        self.remainingLasers = self.totalLasers
        self.lasers = [self.baseLaserSprites.Rotate(random.randint(0, 180)) for _ in range(self.totalLasers)]
        self.lasersPixelMasks = [pygame.mask.from_surface(laser.frames[0]) for laser in self.lasers]
        for i in range(self.totalLasers):
            self.lasers[i].PlayAnimation()
            laserX = DISPLAY_WIDTH + i * (self.baseLaserSprites.GetSize()[0] + self.gapBetweenLasers)
            laserY = random.randint(0, DISPLAY_HEIGHT - self.lasers[i].GetSize()[1])
            self.lasers[i].ChangeRelativePos((laserX, laserY))
            self.gameScene.gameLayer.AttachObject(self.lasers[i])

        # Blocuri de bani
        self.remainingBlocks = 0
        for i in range(self.totalLasers):
            if random.randint(1, 100) <= self.blockSpawnChance:
                laserX = self.lasers[i].GetRect().x
                laserTop = self.lasers[i].GetRect().top
                laserBottom = self.lasers[i].GetRect().bottom
                areaStart, areaEnd = (0, laserTop) if laserTop > DISPLAY_HEIGHT - laserBottom else (laserBottom + 1, DISPLAY_HEIGHT)
                spawnAreaHeight = areaEnd - areaStart
                minHeight = 2 * CoinMatrix.coinHeight
                blockHeight = random.randint(minHeight, int(0.5 * spawnAreaHeight)) if spawnAreaHeight >= minHeight else 0
                blockWidth = self.baseLaserSprites.GetSize()[0]
                blockX = laserX
                blockY = areaStart + random.randint(0, spawnAreaHeight - blockHeight + 1)
                self.coinBlocks.append(CoinMatrix(blockX, blockY, blockWidth, blockHeight))
                self.gameScene.gameLayer.AttachObject(self.coinBlocks[-1])
                self.remainingBlocks += 1

        # Rachete
        if self.haveRockets:
            self.__ResetRocket()
    

    def CheckCollision(self, playerPixelMask: pygame.mask.Mask, playerRect: pygame.Rect) -> bool:
        # Lasere
        for i in range(self.remainingLasers):
            laserRect = self.lasers[i].GetRect()
            laserOffset = (laserRect.x - playerRect.x, laserRect.y - playerRect.y)
            if playerPixelMask.overlap(self.lasersPixelMasks[i], laserOffset) is not None:
                return True
        
        # Rachete
        if self.haveRockets and self.warningTime >= self.warningDuration:
            rocketRect = self.currentRocket.GetRect()
            rocketOffset = (rocketRect.x - playerRect.x, rocketRect.y - playerRect.y)
            if playerPixelMask.overlap(self.rocketPixelMask, rocketOffset):
                return True

        return False


    def CheckCoinCollision(self, playerRect: pygame.Rect) -> int | None:
        collidedCoins = 0
        for block in self.coinBlocks:
            coins = block.CheckCollision(playerRect)
            if coins is not None:
                collidedCoins += coins
        return (collidedCoins if collidedCoins != 0 else None)


    def __ResetRocket(self) -> None:
        warningX = DISPLAY_WIDTH - self.warningWidth
        warningY = random.randint(0, DISPLAY_HEIGHT - self.warningHeight)
        self.currentRocket = Sprite(self.warningImg, warningX, warningY, self.warningWidth, self.warningHeight)
        self.gameScene.gameLayer.AttachObject(self.currentRocket)
        self.warningTime = 0.0


    def __LaunchRocket(self) -> None:
        self.gameScene.gameLayer.DetachObject(self.currentRocket)
        rocketY = self.currentRocket.GetRelativePos().y
        self.currentRocket = Animation(DISPLAY_WIDTH, rocketY, self.rocketWidth, self.rocketHeight, self.rocketImg, self.rocketFrameTime)
        self.rocketPixelMask = pygame.mask.from_surface(self.currentRocket.frames[0])
        self.currentRocket.PlayAnimation()
        self.gameScene.gameLayer.AttachObject(self.currentRocket)
    

    def __LasersEnded(self) -> bool:
        return self.remainingLasers == 0
