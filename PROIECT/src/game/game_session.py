import pygame
import random
from time import time

from framework.rendered_object import RenderedObject
from framework.scene import Scene
from framework.sprite import Sprite
from framework.text_object import TextObject
from framework.button import Button
from framework.update_scheduler import UpdateScheduler
from framework.events_manager import EventsManager
from framework.animation import Animation
from framework.constants import *
import framework.app as app

from game.obstacles.laser_rocket_wave import LaserRocketWave
from game.obstacles.ray_wave import RayWave

import game.meniu as gm


class GameSession(Scene):
    def __init__(self) -> None:
        super().__init__()
        
        self.gameLayer = RenderedObject(0, 0, 0, 0)  # Se vor atasa obiectele jocului (obstacole, jucator, ...)
        self.infoLayer = RenderedObject(0, 0, 0, 0)  # Se vor atasa obiecte utile utilizatorului (scor, butonul de pauza, ...)
        self.AttachObject(self.gameLayer)
        self.AttachObject(self.infoLayer)

        # Miscarea scenei
        self.sceneAcceleration = 0
        self.sceneXVelocity = -250.0
        self.sceneDeceleration = 100        # Folosite atunci cand jucatorul moare
        self.sceneVelocityOnDeath = None    #

        # Background
        loopBgImage = pygame.image.load(RES_DIR + "loop_bg.png").convert()
        loopBg1 = Sprite(loopBgImage, 0, 0, loopBgImage.get_width() * 1.5, DISPLAY_HEIGHT)
        loopBg2 = Sprite(loopBgImage, loopBgImage.get_width() * 1.5, 0, loopBgImage.get_width() * 1.5, DISPLAY_HEIGHT)
        loopBg1.AttachObject(loopBg2)
        self.bg = loopBg1
        self.gameLayer.AttachObject(self.bg)

        # Caracter
        self.playerLives = 1
        self.ascentAcceleration = 1100
        self.gravitationalAcceleration = 1100
        self.maxAscentSpeed = 550
        self.maxFallSpeed = 550
        self.playerYVelocity = 0.0

        self.playerWidth = 60
        self.playerHeight = 60
        playerStartX = DISPLAY_WIDTH / 10
        playerStartY = DISPLAY_HEIGHT / 2 - self.playerHeight / 2
        
        frameTime = 0.15  # Timpul dintre cadrele animatiei (in secunde)
        playerWalkFrames = [pygame.image.load(RES_DIR + "walk1.bmp").convert_alpha(), pygame.image.load(RES_DIR + "walk2.bmp").convert_alpha()]
        self.playerWalk = Animation(playerStartX, playerStartY, self.playerWidth, self.playerHeight, playerWalkFrames, frameTime)
        
        playerFallFrame = pygame.image.load(RES_DIR + 'beggining.bmp').convert_alpha()
        self.playerFall = Sprite(playerFallFrame, playerStartX, playerStartY, self.playerWidth, self.playerHeight)
        
        playerAscentFrame = pygame.image.load(RES_DIR + 'flying.bmp').convert_alpha()
        self.playerAscent = Sprite(playerAscentFrame, playerStartX, playerStartY, 60, 101)
        
        playerDeadFrame = pygame.image.load(RES_DIR + "dead.bmp").convert_alpha()
        self.playerDead = Sprite(playerDeadFrame, playerStartX, playerStartY, self.playerWidth, self.playerHeight)
        
        self.playerState = self.playerFall
        self.gameLayer.AttachObject(self.playerState)
        
        self.playerPixelMask = pygame.mask.from_surface(self.playerFall.texture)

        # Obstacole
        random.seed(time())
        self.timeBetweenWaves = 3
        self.obstacleWave = None
        self.transTimeElapsed = 0.0

        # Scor
        self.score = 0.0
        self.scoreText = TextObject("0m", (255, 255, 255), "Arial", 26, 0, 0)
        self.infoLayer.AttachObject(self.scoreText)

        # Bani
        self.collectedCoins = 0
        coinImg = pygame.image.load(RES_DIR + 'coin/coin_01.png').convert_alpha()
        coinIcon = Sprite(coinImg, self.scoreText.GetRect().right + 100, 0, 30, 30)
        self.coinsText = TextObject("0", (255, 255, 255), "Arial", 26, coinIcon.GetRect().right + 10, 0)
        self.infoLayer.AttachObject(self.coinsText)
        self.infoLayer.AttachObject(coinIcon)

        # Vieti caracter
        self.playerLives = 1
        heartImg = pygame.image.load(RES_DIR + 'heart.png').convert_alpha()
        heartIcon = Sprite(heartImg, self.coinsText.GetRect().right + 100, 0, 30, 30)
        self.playerLivesText = TextObject(str(self.playerLives), (255, 255, 255), 'Arial', 26, heartIcon.GetRect().right + 10, 0)
        self.infoLayer.AttachObject(self.playerLivesText)
        self.infoLayer.AttachObject(heartIcon)
    
        # Interfata "a doua sansa"
        self.newLifePrice = 200
        self.givenTime = 15

        notEnoughMoneyText = f"Nu ai destule monede pentru a cumpara vieti. (min. {self.newLifePrice} monede)"
        self.notEnoughMoney = TextObject(notEnoughMoneyText, (255, 255, 255), 'Arial', 30, 0, 0)
        nemRect = self.notEnoughMoney.GetRect()
        self.notEnoughMoney.ChangeRelativePos((DISPLAY_WIDTH / 2 - nemRect.width / 2, DISPLAY_HEIGHT / 2 - nemRect.height * 2))

        buyQuestionText = f"Cumperi inca o viata? ({self.newLifePrice} monede)"
        self.buyQuestion = TextObject(buyQuestionText, (255, 255, 255), 'Arial', 30, 0, 0)
        bqRect = self.buyQuestion.GetRect()
        self.buyQuestion.ChangeRelativePos((DISPLAY_WIDTH / 2 - bqRect.width / 2, DISPLAY_HEIGHT / 2 - bqRect.height * 2))

        buttonWidth = 150
        buttonHeight = 50
        self.buttonBuyLife = Button(DISPLAY_WIDTH / 2 - 30 - buttonWidth, DISPLAY_HEIGHT / 2 + 10, buttonWidth, buttonHeight, 'Cumpara', (0, 0, 0), 'Arial', 26, None, (255, 224, 0))
        self.buttonQuit = Button(DISPLAY_WIDTH / 2 + 30, DISPLAY_HEIGHT / 2 + 10, buttonWidth, buttonHeight, 'Iesire', (255, 255, 255), 'Arial', 26, None, (216, 216, 216))

        self.timer = TextObject(str(self.givenTime), (255, 255, 255), 'Arial', 40, 0, 0)
        timerRect = self.timer.GetRect()
        self.timer.ChangeRelativePos((DISPLAY_WIDTH / 2 - timerRect.width / 2, DISPLAY_HEIGHT / 2 + self.buttonQuit.GetRect().height + 30))

        darkBgSurface = pygame.Surface((1, 1)).convert_alpha()
        darkBgSurface.fill((0, 0, 0, 150))
        self.darkBg = Sprite(darkBgSurface, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        
        self.remainingTime = self.givenTime


    def OnSceneEnter(self) -> None:
        self.playerWalk.PlayAnimation()

        EventsManager.GetInstance().AddListener(pygame.USEREVENT, self.OnWaveEnd)

        scheduler = UpdateScheduler.GetInstance()
        scheduler.ScheduleUpdate(self.UpdateSceneVelocity)
        scheduler.ScheduleUpdate(self.UpdateBackground)
        scheduler.ScheduleUpdate(self.UpdateScore)
        if self.playerState is self.playerDead:
            scheduler.ScheduleUpdate(self.UpdatePlayerDead)
        else:
            scheduler.ScheduleUpdate(self.UpdatePlayer)
        if self.obstacleWave is None:
            scheduler.ScheduleUpdate(self.WaveTransitionAgent)
        else:
            self.obstacleWave.SetActive()


    def UpdateSceneVelocity(self, deltaTime: float) -> None:
        self.sceneXVelocity -= self.sceneAcceleration * deltaTime


    def UpdateBackground(self, deltaTime: float) -> None:
        bgXPos = self.bg.GetRelativePos().x
        bgWidth = self.bg.GetSize()[0]
        bgMoveAmount = self.sceneXVelocity * deltaTime
        if bgXPos + bgMoveAmount <= -bgWidth:
            bgMoveAmount += bgWidth
        self.bg.MoveBy((bgMoveAmount, 0))


    def UpdateScore(self, deltaTime: float) -> None:
        moveAmount = -self.sceneXVelocity * deltaTime
        self.score += moveAmount / 25
        self.scoreText.ChangeText(str(int(self.score)) + 'm')


    def UpdatePlayer(self, deltaTime: float) -> None:
        playerStateRect = self.playerState.GetRect()
        playerTop = playerStateRect.top 
        playerBottom =  playerTop + self.playerHeight - 1

        if pygame.key.get_pressed()[pygame.K_w]:
            if playerTop > 0:
                self.playerYVelocity = min(self.maxAscentSpeed, self.playerYVelocity + self.ascentAcceleration * deltaTime)
            self.__ChangePlayerState(self.playerAscent)
        elif playerBottom < DISPLAY_HEIGHT:
            self.playerYVelocity = max(-self.maxFallSpeed, self.playerYVelocity - self.gravitationalAcceleration * deltaTime)
            self.__ChangePlayerState(self.playerFall)
        else:
            self.__ChangePlayerState(self.playerWalk)

        yMoveAmount = -self.playerYVelocity * deltaTime
    
        if yMoveAmount != 0:
            if playerBottom + yMoveAmount > DISPLAY_HEIGHT:
                yMoveAmount = DISPLAY_HEIGHT - playerBottom
            elif playerTop + yMoveAmount < 0:
                yMoveAmount = -playerTop

            if playerBottom + yMoveAmount == DISPLAY_HEIGHT or playerTop + yMoveAmount == 0:
                self.playerYVelocity = 0

            self.playerState.MoveBy((0, yMoveAmount))
        
        playerRect = pygame.Rect(playerStateRect.x, playerStateRect.y, self.playerWidth, self.playerHeight)

        # Testeaza coliziunea cu monede
        self.__CheckCoinCollision(playerRect)

        # Testeaza coliziunea cu obstacole
        if self.obstacleWave is not None and self.obstacleWave.CheckCollision(self.playerPixelMask, playerRect):
            self.__ChangePlayerState(self.playerDead)
            self.sceneVelocityOnDeath = self.sceneXVelocity
            scheduler = UpdateScheduler.GetInstance()
            scheduler.UnscheduleUpdate(self.UpdateSceneVelocity)
            scheduler.UnscheduleUpdate(self.UpdatePlayer)
            scheduler.ScheduleUpdate(self.UpdatePlayerDead)
    

    def UpdatePlayerDead(self, deltaTime: float) -> None:
        playerStateRect = self.playerState.GetRect()
        playerRect = pygame.Rect(playerStateRect.x, playerStateRect.y, self.playerWidth, self.playerHeight)
        playerBottom =  playerRect.bottom
        
        if playerBottom < DISPLAY_HEIGHT:
            self.playerYVelocity = max(-self.maxFallSpeed, self.playerYVelocity - self.gravitationalAcceleration * deltaTime)
            yMoveAmount = -self.playerYVelocity * deltaTime
            if playerBottom + yMoveAmount > DISPLAY_HEIGHT:
                yMoveAmount = DISPLAY_HEIGHT - playerBottom
            self.playerState.MoveBy((0, yMoveAmount))
            self.__CheckCoinCollision(playerRect)
        elif self.sceneXVelocity < 0:
            self.sceneXVelocity = min(0, self.sceneXVelocity + self.sceneDeceleration * deltaTime)
            self.__CheckCoinCollision(playerRect)
        else:
            scheduler = UpdateScheduler.GetInstance()
            scheduler.UnscheduleUpdate(self.UpdatePlayerDead)
            if self.playerLives > 0:
                self.__RevivePlayer()
            else:
                # Initializare interfata "A doua sansa"
                scheduler.UnscheduleUpdate(self.UpdateBackground)
                scheduler.UnscheduleUpdate(self.UpdateScore)
                scheduler.ScheduleUpdate(self.UpdateSecondChance)

                self.darkBg.AttachObject(self.infoLayer)
                self.DetachObject(self.infoLayer)
                self.AttachObject(self.darkBg)

                self.remainingTime = self.givenTime
                self.timer.ChangeText(str(self.remainingTime))
                self.infoLayer.AttachObject(self.timer)

                if self.collectedCoins < self.newLifePrice:
                    self.infoLayer.AttachObject(self.notEnoughMoney)
                    self.infoLayer.AttachObject(self.buttonQuit)
                    self.buttonQuit.GetRect().x = DISPLAY_WIDTH / 2 - self.buttonQuit.GetSize()[0] / 2
                    EventsManager.GetInstance().AddListener(pygame.MOUSEBUTTONDOWN, self.OnButtonQuit)
                else:
                    self.infoLayer.AttachObject(self.buyQuestion)
                    self.infoLayer.AttachObject(self.buttonBuyLife)
                    self.infoLayer.AttachObject(self.buttonQuit)
                    EventsManager.GetInstance().AddListener(pygame.MOUSEBUTTONDOWN, self.OnButtonBuy)
                    EventsManager.GetInstance().AddListener(pygame.MOUSEBUTTONDOWN, self.OnButtonQuit)


    def UpdateSecondChance(self, deltaTime: float) -> None:
        if self.remainingTime > 0:
            self.remainingTime -= deltaTime
            self.timer.ChangeText(str(int(self.remainingTime) + 1))
        else:
            self.score += self.collectedCoins
            app.App.GetInstance().PlayNewScene(gm.Meniu())


    def WaveTransitionAgent(self, deltaTime: float) -> None:
        self.transTimeElapsed += deltaTime
        if self.transTimeElapsed >= self.timeBetweenWaves:
            UpdateScheduler.GetInstance().UnscheduleUpdate(self.WaveTransitionAgent)

            # Alege, in mod aleatoriu, un val nou de obstacole
            nr = random.randint(1, 100)
            if nr <= 25:
                self.obstacleWave = LaserRocketWave(self, False)
            elif nr <= 50:
                self.obstacleWave = LaserRocketWave(self)
            else:
                self.obstacleWave = RayWave(self)
            
            self.obstacleWave.SetActive()


    def OnWaveEnd(self, event: pygame.event.Event) -> None:
        self.obstacleWave.CleanUp()
        self.obstacleWave = None
        if self.playerState is not self.playerDead:
            self.transTimeElapsed = 0
            UpdateScheduler.GetInstance().ScheduleUpdate(self.WaveTransitionAgent)


    def __ChangePlayerState(self, newState: Sprite | Animation) -> None:
        if self.playerState is not newState:
            self.gameLayer.DetachObject(self.playerState)
            newState.MoveBy(self.playerState.GetRelativePos() - newState.GetRelativePos())
            self.playerState = newState
            self.gameLayer.AttachObject(self.playerState)
    

    def __CheckCoinCollision(self, playerRect: pygame.Rect) -> None:
        if self.obstacleWave is not None and self.obstacleWave.hasCoins:
            collidedCoins = self.obstacleWave.CheckCoinCollision(playerRect)
            if collidedCoins is not None:
                self.collectedCoins += collidedCoins
                self.coinsText.ChangeText(str(self.collectedCoins))
    

    def __RevivePlayer(self) -> None:
        scheduler = UpdateScheduler.GetInstance()

        self.playerLives -= 1
        self.playerLivesText.ChangeText(str(self.playerLives))
        self.__ChangePlayerState(self.playerWalk)
        scheduler.ScheduleUpdate(self.UpdatePlayer)
        scheduler.ScheduleUpdate(self.UpdateScore)

        self.sceneXVelocity = self.sceneVelocityOnDeath
        scheduler.ScheduleUpdate(self.UpdateSceneVelocity)
        scheduler.ScheduleUpdate(self.UpdateBackground)

        if self.obstacleWave is not None:
            self.obstacleWave.CleanUp()
            self.obstacleWave = None
        self.transTimeElapsed = 0
        scheduler.ScheduleUpdate(self.WaveTransitionAgent)
    

    def OnButtonBuy(self, event: pygame.event.Event) -> None:
        if self.buttonBuyLife.CollidesWithPoint(event.pos):
            EventsManager.GetInstance().RemoveListener(pygame.MOUSEBUTTONDOWN, self.OnButtonBuy)
            EventsManager.GetInstance().RemoveListener(pygame.MOUSEBUTTONDOWN, self.OnButtonQuit)
            UpdateScheduler.GetInstance().UnscheduleUpdate(self.UpdateSecondChance)
            
            self.darkBg.DetachObject(self.infoLayer)
            self.DetachObject(self.darkBg)
            self.AttachObject(self.infoLayer)
            self.infoLayer.DetachObject(self.buyQuestion)
            self.infoLayer.DetachObject(self.buttonBuyLife)
            self.infoLayer.DetachObject(self.buttonQuit)
            self.infoLayer.DetachObject(self.timer)
            
            self.collectedCoins -= self.newLifePrice
            self.coinsText.ChangeText(str(self.collectedCoins))
            self.playerLives += 1
            self.__RevivePlayer()


    def OnButtonQuit(self, event: pygame.event.Event) -> None:
        if self.buttonQuit.CollidesWithPoint(event.pos):
            self.score += self.collectedCoins
            app.App.GetInstance().PlayNewScene(gm.Meniu())
