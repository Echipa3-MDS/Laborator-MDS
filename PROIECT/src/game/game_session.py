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
from framework.box import Box
import framework.app as app

from game.obstacles.laser_rocket_wave import LaserRocketWave
from game.obstacles.ray_wave import RayWave
import game.pause_menu as pm
import game.second_chance as gsc
import game.game_over as gover


class GameSession(Scene):
    def __init__(self) -> None:
        super().__init__()

        self.bgLayer = RenderedObject(0, 0, 0, 0)    # Se vor atasa elemente de background
        self.gameLayer = RenderedObject(0, 0, 0, 0)  # Se vor atasa obiectele jocului (obstacole, jucator, ...)
        self.infoLayer = RenderedObject(0, 0, 0, 0)  # Se vor atasa obiecte utile utilizatorului (scor, butonul de pauza, ...)
        self.AttachObject(self.bgLayer)
        self.AttachObject(self.gameLayer)
        self.AttachObject(self.infoLayer)

        pygame.mixer.Channel(0).play(pygame.mixer.Sound(RES_DIR + "audio/Arcade-Fantasy.mp3"), loops=-1)
        if(app.App.GetInstance().IsMuted()):
            pygame.mixer.Channel(0).set_volume(0)
        else:
             pygame.mixer.Channel(0).set_volume(0.1)

        # Miscarea scenei
        self.sceneAcceleration = 2.5        # In doua minute se ajunge la velocitatea maxima
        self.sceneXVelocity = -250.0
        self.maxSceneXVelocity = -550.0
        self.sceneDeceleration = 150        # Folosite atunci cand jucatorul moare
        self.sceneVelocityOnDeath = None    #

        # Background
        self.nrLayers = 4
        self.bgLayersSpeeds = [0, 0.5, 0.75, 1]   # Procente din viteza scenei
        self.bgLayers = []
        for i in range(self.nrLayers):
            layerImg = pygame.image.load(RES_DIR + f"img/bg_layers/layer{i + 1}.png").convert_alpha()
            layerSprite1 = Sprite(layerImg, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
            layerSprite2 = Sprite(layerImg, DISPLAY_WIDTH, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
            layerSprite1.AttachObject(layerSprite2)
            self.bgLayer.AttachObject(layerSprite1)
            self.bgLayers.append(layerSprite1)
        
        # Caracter
        self.playerLives = 1
        self.ascentAcceleration = 1150
        self.gravitationalAcceleration = 1150
        self.maxAscentSpeed = 600
        self.maxFallSpeed = 600
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
        
        playerDeadFrame = [pygame.image.load(RES_DIR + "dead.bmp").convert_alpha(), pygame.image.load(RES_DIR + "dead2.bmp").convert_alpha()]
        self.playerDead = Animation(playerStartX, playerStartY, self.playerWidth, self.playerHeight, playerDeadFrame, frameTime)
        
        self.playerState = self.playerFall
        self.gameLayer.AttachObject(self.playerState)
        
        self.playerPixelMask = pygame.mask.from_surface(self.playerFall.texture)

        # Obstacole
        random.seed(time())
        self.timeBetweenWaves = 3
        self.obstacleWave = None
        self.transTimeElapsed = 0.0

        #Chenar negru
        self.chenar = Box(0, 0, 390, 32, (0, 0, 0))
        self.chenar.SetAlphaLevel(70)
        self.infoLayer.AttachObject(self.chenar)

        # Scor
        self.score = 0.0
        self.scoreText = TextObject("0m", (255, 255, 255), RES_DIR + "font\Happy School.ttf", 35, 0, 0)
        self.infoLayer.AttachObject(self.scoreText)

        # Bani
        self.collectedCoins = 0
        coinImg = pygame.image.load(RES_DIR + 'coin/coin_01.png').convert_alpha()
        coinIcon = Sprite(coinImg, self.scoreText.GetRect().right + 115, 0, 30, 30)
        self.coinsText = TextObject("0", (255, 255, 255), RES_DIR + "font\Happy School.ttf", 35, coinIcon.GetRect().right + 10, 0)
        self.infoLayer.AttachObject(self.coinsText)
        self.infoLayer.AttachObject(coinIcon)

        # Vieti caracter
        self.playerLives = 1
        heartImg = pygame.image.load(RES_DIR + 'heart.png').convert_alpha()
        heartIcon = Sprite(heartImg, self.coinsText.GetRect().right + 115, 0, 30, 30)
        self.playerLivesText = TextObject(str(self.playerLives), (255, 255, 255), RES_DIR + "font\Happy School.ttf", 35, heartIcon.GetRect().right + 10, 0)
        self.infoLayer.AttachObject(self.playerLivesText)
        self.infoLayer.AttachObject(heartIcon)
    
        # Buton pauza
        pIconPath = RES_DIR + 'pause.png'
        pIconW = 50
        pIconH = 50
        pIconX = DISPLAY_WIDTH - pIconW - 10
        pIconY = 10
        self.pauseButton = Button(pIconX, pIconY, pIconW, pIconH, bgImagePath=pIconPath)
        self.infoLayer.AttachObject(self.pauseButton)


    def OnSceneEnter(self) -> None:
        self.playerWalk.PlayAnimation()

        EventsManager.GetInstance().AddListener(pygame.USEREVENT, self.OnWaveEnd)
        EventsManager.GetInstance().AddListener(pygame.MOUSEBUTTONDOWN, self.OnButtonPause)

        scheduler = UpdateScheduler.GetInstance()
        scheduler.ScheduleUpdate(self.UpdateBackground)
        scheduler.ScheduleUpdate(self.UpdateScore)
        if self.playerState is self.playerDead:
            scheduler.ScheduleUpdate(self.UpdatePlayerDying)
            self.playerDead.PlayAnimation()
        else:
            scheduler.ScheduleUpdate(self.UpdateSceneVelocity)
            scheduler.ScheduleUpdate(self.UpdatePlayer)
        if self.obstacleWave is None:
            scheduler.ScheduleUpdate(self.WaveTransitionAgent)
        else:
            self.obstacleWave.SetActive()


    def UpdateSceneVelocity(self, deltaTime: float) -> None:
        self.sceneXVelocity -= self.sceneAcceleration * deltaTime
        if abs(self.sceneXVelocity) >= abs(self.maxSceneXVelocity):
            UpdateScheduler.GetInstance().UnscheduleUpdate(self.UpdateSceneVelocity)
            self.sceneXVelocity = self.maxSceneXVelocity
    

    def UpdateBackground(self, deltaTime: float) -> None:
        for i in range(self.nrLayers):
            layerXPos = self.bgLayers[i].GetRelativePos().x
            layerWidth = self.bgLayers[i].GetSize()[0]
            moveAmount = self.sceneXVelocity * self.bgLayersSpeeds[i] * deltaTime
            if layerXPos + moveAmount <= -layerWidth:
                moveAmount += layerWidth
            self.bgLayers[i].MoveBy((moveAmount, 0))


    def UpdateScore(self, deltaTime: float) -> None:
        moveAmount = -self.sceneXVelocity * deltaTime
        self.score += moveAmount / 40
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
            self.playerDead.PlayAnimation()
            self.sceneVelocityOnDeath = self.sceneXVelocity
            scheduler = UpdateScheduler.GetInstance()
            scheduler.UnscheduleUpdate(self.UpdateSceneVelocity)
            scheduler.UnscheduleUpdate(self.UpdatePlayer)
            scheduler.ScheduleUpdate(self.UpdatePlayerDying)
    

    def UpdatePlayerDying(self, deltaTime: float) -> None:
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
            UpdateScheduler.GetInstance().UnscheduleUpdate(self.UpdatePlayerDying)
            self.OnPlayerDead()


    def OnPlayerDead(self) -> None:
        if self.playerLives > 0:
            self.AddLives(-1)
            self.RevivePlayer()
            scheduler = UpdateScheduler.GetInstance()
            scheduler.ScheduleUpdate(self.UpdatePlayer)
            scheduler.ScheduleUpdate(self.UpdateSceneVelocity)
            scheduler.ScheduleUpdate(self.WaveTransitionAgent)
        elif self.collectedCoins >= gsc.SecondChanceInterface.newLifePrice:
            displayState = pygame.display.get_surface().copy()
            scInterface = gsc.SecondChanceInterface(self, displayState, int(self.score), self.collectedCoins)
            app.App.GetInstance().PlayNewScene(scInterface)
        else:
            displayState = pygame.display.get_surface().copy()
            finalScore = int(self.score) + self.collectedCoins
            gameOverScene = gover.GameOver(finalScore, displayState)
            app.App.GetInstance().PlayNewScene(gameOverScene)
    

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


    def OnButtonPause(self, event: pygame.event.Event) -> None:
        if self.pauseButton.CollidesWithPoint(event.pos):
            self.pauseButton.ClickedSound(app.App.GetInstance().IsMuted())
            displayState = pygame.display.get_surface().copy()
            pauseScene = pm.PauseMenu(self, displayState)
            app.App.GetInstance().PlayNewScene(pauseScene)
    

    def AddCoins(self, coins: int) -> None:
        self.collectedCoins += coins
        self.coinsText.ChangeText(str(self.collectedCoins))
    

    def AddLives(self, lives: int) -> None:
        self.playerLives += lives
        self.playerLivesText.ChangeText(str(self.playerLives))


    def RevivePlayer(self) -> None:
        self.__ChangePlayerState(self.playerWalk)
        self.sceneXVelocity = self.sceneVelocityOnDeath
        if self.obstacleWave is not None:
            self.obstacleWave.CleanUp()
            self.obstacleWave = None
        self.transTimeElapsed = 0


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
                self.AddCoins(collidedCoins)
