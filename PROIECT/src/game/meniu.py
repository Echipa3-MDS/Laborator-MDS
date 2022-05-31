import pygame

from framework.scene import Scene
from framework.constants import *
from framework.events_manager import EventsManager

from framework.button import Button
from framework.sprite import Sprite
from framework.text_object import TextObject

from game.game_session import GameSession
from game.high_scores import HighScores
import framework.app as app

from framework.box import Box


class Meniu(Scene):    
    def __init__(self) -> None:
        super().__init__()    

        logoImg = pygame.image.load(RES_DIR + "logo.png")
        logoWidth = 400
        logoHeight = 200
        logoPosX = DISPLAY_WIDTH / 2 - logoWidth / 2
        logoPosY = 20

        self.logo = Sprite(logoImg, logoPosX, logoPosY, logoWidth, logoHeight)

        buttonWidth = 200
        buttonHeight = 50
        posX = DISPLAY_WIDTH / 2 - buttonWidth / 2
        posY = 200

        textColor = (255, 255, 255)
        font = 'arial'
        fontSize = 40
        bgColor = (0, 0, 0)
        bgImage = None
        borderRadius = 5
        buttonTop = 20
        alpha = 200
        

        self.butonStart = Button(posX, posY, buttonWidth, buttonHeight, 'Start', textColor, font, fontSize, bgImage, bgColor)
        self.butonHighScores = Button(posX, posY + buttonHeight + buttonTop, buttonWidth, buttonHeight, 'Top Scoruri', textColor, font, fontSize, bgImage, bgColor)
        self.butonExit = Button(posX, posY + 2 * (buttonHeight + buttonTop), buttonWidth, buttonHeight, 'Iesire', textColor, font, fontSize, bgImage, bgColor)
        
        self.butonStart.SetAlphaLevel(alpha)
        self.butonHighScores.SetAlphaLevel(alpha)
        self.butonExit.SetAlphaLevel(alpha)
        
        hsWidth = 500
        hsHeight = 400
        hsX = DISPLAY_WIDTH / 2 - hsWidth / 2
        hsY = DISPLAY_HEIGHT / 2 - hsHeight / 2

        self.scoreBoard = Box(hsX, hsY, hsWidth, hsHeight, (42, 47, 46))
        
        hsExitWidth = 50
        hsExitHeight = 50
        hsExitX = hsWidth - hsExitWidth
        hsExitY = 0
        self.hsExitButton = Button(hsExitX, hsExitY, hsExitWidth, hsExitHeight, 'X', textColor, font, 50, None, bgColor)
        self.hsExitButton.SetAlphaLevel(alpha)
        self.scoreBoard.AttachObject(self.hsExitButton)

        highScore = HighScores.GetInstance()
        textHighScore = highScore.GetHighScoreString(10)
        liniHighScore = textHighScore.strip().split('\n')
        liniHighScore[-1] += ' '

        hsTop = 10
        hsFontSize = 20
        
        for it, linie in enumerate(liniHighScore):
            fontT = pygame.font.SysFont(font, hsFontSize)
            textSurface = fontT.render(linie, True, textColor)
            textWidth = textSurface.get_width()
            textHeight = textSurface.get_height()

            linieY = hsTop + textHeight
            linieX = hsWidth / 2 - textWidth / 2

            textHSObject = TextObject(linie, textColor, font, hsFontSize, linieX, it * (linieY))
            self.scoreBoard.AttachObject(textHSObject)


        self.AttachObject(self.logo)
        self.AttachObject(self.butonStart)
        self.AttachObject(self.butonHighScores)
        self.AttachObject(self.butonExit)

        self.scoreBoardActive = False
        # self.AttachObject(self.scoreBoard)

        
    
    def OnSceneEnter(self) -> None:
        super().OnSceneEnter()
        EventsManager.GetInstance().AddListener(pygame.MOUSEBUTTONDOWN, self.OnMouseDown)


    def OnMouseDown(self, event: pygame.event.Event) -> None:
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if not self.scoreBoardActive:
                butonStart = self.butonStart.GetRect()
                if butonStart.collidepoint(pos):
                    gameScene = GameSession()
                    appObj = app.App.GetInstance()
                    appObj.PlayNewScene(gameScene)
                
                butonExit = self.butonExit.GetRect()
                if butonExit.collidepoint(pos):
                    quitEvent = pygame.event.Event(pygame.QUIT)
                    pygame.event.post(quitEvent)
                
                butonHighScore = self.butonHighScores.GetRect()
                if butonHighScore.collidepoint(pos):
                    self.DetachObject(self.logo)
                    self.DetachObject(self.butonStart)
                    self.DetachObject(self.butonHighScores)
                    self.DetachObject(self.butonExit)
                    self.AttachObject(self.scoreBoard)
                    self.scoreBoardActive = True
            else:
                butonExitHs = self.hsExitButton.GetRect()
                if butonExitHs.collidepoint(pos):
                    self.AttachObject(self.logo)
                    self.AttachObject(self.butonStart)
                    self.AttachObject(self.butonHighScores)
                    self.AttachObject(self.butonExit)
                    self.DetachObject(self.scoreBoard)
                    self.scoreBoardActive = False