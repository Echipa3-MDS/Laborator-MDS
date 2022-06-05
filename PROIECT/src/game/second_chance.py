import pygame

from framework.scene import Scene
from framework.text_object import TextObject
from framework.button import Button
from framework.constants import *
from framework.events_manager import EventsManager
from framework.update_scheduler import UpdateScheduler
import framework.app as app

from game.game_over import GameOver
import game.game_session as gs


class SecondChanceInterface(Scene):
    
    newLifePrice = 200

    def __init__(self, gameScene: 'gs.GameSession', displayState: pygame.Surface, playerScore: int, collectedCoins: int) -> None:
        super().__init__()

        self.givenTime = 15

        self.gameScene = gameScene
        self.displayState = displayState
        self.playerScore = playerScore
        self.collectedCoins = collectedCoins

        darkBgSurface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT)).convert_alpha()
        darkBgSurface.fill((0, 0, 0, 125))
        gameFrameBg = self.displayState.copy()
        gameFrameBg.blit(darkBgSurface, (0, 0))
        self.ChangeBgImage(gameFrameBg)

        buyQuestionText = f"Cumperi inca o viata? ({self.newLifePrice} monede)"
        self.buyQuestion = TextObject(buyQuestionText, (255, 255, 255), RES_DIR + "font\Happy School.ttf", 30, 0, 0)
        bqRect = self.buyQuestion.GetRect()
        self.buyQuestion.ChangeRelativePos((DISPLAY_WIDTH / 2 - bqRect.width / 2, DISPLAY_HEIGHT / 2 - bqRect.height * 2))
        self.AttachObject(self.buyQuestion)

        buttonWidth = 200
        buttonHeight = 50
        self.buttonBuyLife = Button(DISPLAY_WIDTH / 2 - 30 - buttonWidth, DISPLAY_HEIGHT / 2 + 10, buttonWidth, buttonHeight, 'Cumpara', (255, 255, 255), RES_DIR + "font\Happy School.ttf", 30, RES_DIR + "img/ButtonBg.png", (255, 224, 0))
        self.buttonQuit = Button(DISPLAY_WIDTH / 2 + 30, DISPLAY_HEIGHT / 2 + 10, buttonWidth, buttonHeight, 'Iesire', (255, 255, 255), RES_DIR + "font\Happy School.ttf", 30, RES_DIR + "img/ButtonBg.png", (216, 216, 216))
        self.AttachObject(self.buttonBuyLife)
        self.AttachObject(self.buttonQuit)

        self.timer = TextObject(str(self.givenTime), (255, 255, 255), RES_DIR + "font\Happy School.ttf", 40, 0, 0)
        timerRect = self.timer.GetRect()
        self.timer.ChangeRelativePos((DISPLAY_WIDTH / 2 - timerRect.width / 2, DISPLAY_HEIGHT / 2 + self.buttonQuit.GetRect().height + 30))
        self.AttachObject(self.timer)
        self.remainingTime = self.givenTime


    def OnSceneEnter(self) -> None:
        UpdateScheduler.GetInstance().ScheduleUpdate(self.UpdateInterface)
        EventsManager.GetInstance().AddListener(pygame.MOUSEBUTTONDOWN, self.OnButtonBuy)
        EventsManager.GetInstance().AddListener(pygame.MOUSEBUTTONDOWN, self.OnButtonQuit)


    def UpdateInterface(self, deltaTime: float) -> None:
        if self.remainingTime > 0:
            self.remainingTime -= deltaTime
            self.timer.ChangeText(str(int(self.remainingTime) + 1))
        else:
            self.ToGameOver()
    

    def OnButtonBuy(self, event: pygame.event.Event) -> None:
        if self.buttonBuyLife.CollidesWithPoint(event.pos):  
            self.buttonBuyLife.ClickedSound(app.App.GetInstance().IsMuted())          
            self.gameScene.AddCoins(-self.newLifePrice)
            self.gameScene.RevivePlayer()
            app.App.GetInstance().PlayNewScene(self.gameScene)


    def OnButtonQuit(self, event: pygame.event.Event) -> None:
        if self.buttonQuit.CollidesWithPoint(event.pos):
            self.buttonQuit.ClickedSound(app.App.GetInstance().IsMuted())
            pygame.mixer.Channel(0).stop()
            self.ToGameOver()
    

    def ToGameOver(self) -> None:
        finalScore = self.playerScore + self.collectedCoins
        gameOverScene = GameOver(finalScore, self.displayState)
        app.App.GetInstance().PlayNewScene(gameOverScene)