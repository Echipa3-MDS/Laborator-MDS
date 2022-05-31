import pygame

from framework.scene import Scene
from framework.constants import *
from framework.events_manager import EventsManager

from framework.button import Button
from framework.sprite import Sprite
from framework.text_object import TextObject
from framework.rendered_object import RenderedObject

from game.high_scores import HighScores
import framework.app as app

from framework.box import Box
import game.meniu as gm

class GameOver(Scene):
    def __init__(self, scor : int, objImgBg : pygame.surface.Surface = None) -> None:
        super().__init__()

        self.scor = int(scor)

        if objImgBg != None:
            self.bgPreviousScene = Sprite(objImgBg, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
            self.AttachObject(self.bgPreviousScene)

        self.darkOverlay = Box(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, (0, 0, 0))
        self.darkOverlay.SetAlphaLevel(100)
        self.AttachObject(self.darkOverlay)


        gameOverImg = pygame.image.load(RES_DIR + "game_over.png")
        GOIWidth = 400
        GOIHeight = 200
        GOIPosX = DISPLAY_WIDTH / 2 - GOIWidth / 2
        GOIPosY = 20

        self.GOI = Sprite(gameOverImg, GOIPosX, GOIPosY, GOIWidth, GOIHeight)

        self.AttachObject(self.GOI)

        self.inputBoxWidth = 400
        self.inputBoxHeight = 50
        inputBoxposX = DISPLAY_WIDTH / 2 - self.inputBoxWidth / 2
        inputBoxposY = 200

        self.inputBox = Box(inputBoxposX, inputBoxposY, self.inputBoxWidth, self.inputBoxHeight, (255, 255, 255))

        self.font = 'arial'
        self.fontSize = 40
        self.textColor = (0, 0, 0)

        self.ibText = ""

        fontT = pygame.font.SysFont(self.font, self.fontSize)
        textSurface = fontT.render(self.ibText, True, self.textColor)
        textWidth = textSurface.get_width()
        textHeight = textSurface.get_height()

        linieY = self.inputBoxHeight / 2 - textHeight / 2
        linieX = self.inputBoxWidth / 2 - textWidth / 2

        self.textITObject = TextObject(self.ibText, self.textColor, self.font, self.fontSize, linieX, linieY)
        self.inputBox.AttachObject(self.textITObject)

        self.AttachObject(self.inputBox)

        buttonWidth = 200
        buttonHeight = 50
        posX = DISPLAY_WIDTH / 2 - buttonWidth / 2
        posY = 270
        buttonTextColor = (255, 255, 255)

        self.butonNext = Button(posX, posY, buttonWidth, buttonHeight, 'Next', buttonTextColor, self.font, self.fontSize, bgColor=(0, 0, 0))
        self.butonNext.SetAlphaLevel(200)

        self.AttachObject(self.butonNext)
    
    def OnSceneEnter(self) -> None:
        super().OnSceneEnter()
        EventsManager.GetInstance().AddListener(pygame.KEYDOWN, self.OnKeyDown)
        EventsManager.GetInstance().AddListener(pygame.MOUSEBUTTONDOWN, self.OnMouseDown)
    
    def updateText(self, text: str) -> None:
        oldText = self.ibText
        self.ibText = text
        fontT = pygame.font.SysFont(self.font, self.fontSize)
        textSurface = fontT.render(self.ibText, True, self.textColor)
        textWidth = textSurface.get_width()
        textHeight = textSurface.get_height()

        linieY = self.inputBoxHeight / 2 - textHeight / 2
        linieX = self.inputBoxWidth / 2 - textWidth / 2

        if textWidth < self.inputBoxWidth:
            self.inputBox.DetachObject(self.textITObject)
            self.textITObject = TextObject(self.ibText, self.textColor, self.font, self.fontSize, linieX, linieY)
            self.inputBox.AttachObject(self.textITObject)
        else:
            self.ibText = oldText
    
    def OnKeyDown(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.ibText != "":
                    highScore = HighScores.GetInstance()
                    dictHS = highScore.GetHighScore()
                    dictHS[self.ibText] = self.scor
                    highScore.UpdateAndSave(dictHS)

                appObj = app.App.GetInstance()
                meniu = gm.Meniu()
                appObj.PlayNewScene(meniu)

            elif event.key == pygame.K_BACKSPACE:
                self.updateText(self.ibText[:-1])
            else:
                key = event.unicode
                if key.isalnum():
                    self.updateText(self.ibText + event.unicode.upper())


    def OnMouseDown(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            butonNext = self.butonNext.GetRect()
            if butonNext.collidepoint(pos):
                if self.ibText != "":
                    highScore = HighScores.GetInstance()
                    dictHS = highScore.GetHighScore()
                    dictHS[self.ibText] = self.scor
                    highScore.UpdateAndSave(dictHS)

                appObj = app.App.GetInstance()
                meniu = gm.Meniu()
                appObj.PlayNewScene(meniu)



