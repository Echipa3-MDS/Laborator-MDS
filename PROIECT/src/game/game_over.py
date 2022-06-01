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
        self.top = 0
        self.scor = int(scor)

        self.ChangeBgImage(objImgBg)

        self.darkOverlay = Box(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, (0, 0, 0))
        self.darkOverlay.SetAlphaLevel(125)

        marginTop = 20

        gameOverImg = pygame.image.load(RES_DIR + "game_over.png")
        GOIWidth = 400
        GOIHeight = 200
        GOIPosX = DISPLAY_WIDTH / 2 - GOIWidth / 2
        GOIPosY = self.top + marginTop

        self.top += GOIPosY + GOIHeight

        self.GOI = Sprite(gameOverImg, GOIPosX, GOIPosY, GOIWidth, GOIHeight)

        self.font = 'arial'
        self.fontSize = 40
        self.textColor = (0, 0, 0)

        textWidth, textHeight = self.textWidthHeight("Scorul obținut: " + str(self.scor), self.font, self.fontSize)
        textPosX = DISPLAY_WIDTH / 2 - textWidth / 2
        textPosY = self.top + marginTop
        self.top += textHeight + marginTop
        self.mesajScor = TextObject("Scorul obținut: " + str(self.scor), (255, 255, 255), self.font, self.fontSize, textPosX, textPosY)

       
        self.inputBoxWidth = 400
        self.inputBoxHeight = 50
        inputBoxposX = DISPLAY_WIDTH / 2 - self.inputBoxWidth / 2
        inputBoxposY = self.top + marginTop

        self.inputBox = Box(inputBoxposX, inputBoxposY, self.inputBoxWidth, self.inputBoxHeight, (255, 255, 255))

        textWidth, textHeight = self.textWidthHeight("Scor salvat", self.font, self.fontSize)

        textPosX = DISPLAY_WIDTH / 2 - textWidth / 2
        textPosY = self.top + marginTop

        self.top += max(textHeight, self.inputBoxHeight) + marginTop

        self.mesajScorSalvat = TextObject("Scor salvat", (255, 255, 255), self.font, self.fontSize, textPosX, textPosY)

        self.ibText = ""

        textWidth, textHeight = self.textWidthHeight("Nume jucător", self.font, self.fontSize)

        linieY = self.inputBoxHeight / 2 - textHeight / 2
        linieX = self.inputBoxWidth / 2 - textWidth / 2
        
        self.emptyText = TextObject("Nume jucător", (50, 50, 50), self.font, self.fontSize, linieX, linieY)

        self.textITObject = self.emptyText
        self.inputBox.AttachObject(self.textITObject)

        # self.AttachObject(self.inputBox)

        self.inputBoxActive = False

        self.buttonWidth = 250
        self.buttonHeight = 50
        self.buttonPosX = DISPLAY_WIDTH / 2 - self.buttonWidth / 2
        self.buttonPosY = self.top + marginTop
        self.buttonTextColor = (255, 255, 255)

        self.butonSave = Button(self.buttonPosX + self.buttonWidth, self.buttonPosY, self.buttonWidth, self.buttonHeight, 'Salvează scor', self.buttonTextColor, self.font, self.fontSize, bgColor=(0, 0, 0))
        self.butonSave.SetAlphaLevel(200)

        self.butonIesire = Button(self.buttonPosX - self.buttonWidth, self.buttonPosY, self.buttonWidth, self.buttonHeight, 'Ieșire', self.buttonTextColor, self.font, self.fontSize, bgColor=(0, 0, 0))
        self.butonIesire.SetAlphaLevel(200)


        self.AttachObject(self.darkOverlay)
        self.AttachObject(self.GOI)
        self.AttachObject(self.mesajScor)
        # self.AttachObject(self.mesajScorSalvat)
        # self.AttachObject(self.inputBox)


        self.AttachObject(self.butonSave)
        self.AttachObject(self.butonIesire)

        self.saved = False

    def textWidthHeight(self, text, font, fontSize):
        fontT = pygame.font.SysFont(font, fontSize)
        textSurface = fontT.render(text, True, (0, 0, 0))
        textWidth = textSurface.get_width()
        textHeight = textSurface.get_height()

        return textWidth, textHeight
    
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
            if self.ibText == "":
                self.textITObject = self.emptyText
            else:
                self.textITObject = TextObject(self.ibText, self.textColor, self.font, self.fontSize, linieX, linieY)
            self.inputBox.AttachObject(self.textITObject)
        else:
            self.ibText = oldText
    
    def OnKeyDown(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:

            if self.inputBoxActive == False:
                return

            if event.key == pygame.K_RETURN:
                if self.ibText != "":
                    highScore = HighScores.GetInstance()
                    dictHS = highScore.GetHighScore()
                    dictHS[self.ibText] = self.scor
                    highScore.UpdateAndSave(dictHS)
                else:
                    return

                self.DetachObject(self.butonSave)
                self.DetachObject(self.butonIesire)

                self.butonIesire = Button(self.buttonPosX, self.buttonPosY, self.buttonWidth, self.buttonHeight, 'Ieșire', self.buttonTextColor, self.font, self.fontSize, bgColor=(0, 0, 0))
                self.butonIesire.SetAlphaLevel(200)
                self.AttachObject(self.butonIesire)

                self.DetachObject(self.inputBox)
                self.inputBoxActive = False

                self.AttachObject(self.mesajScorSalvat)
                self.saved = True

            elif event.key == pygame.K_BACKSPACE:
                self.updateText(self.ibText[:-1])
            else:
                key = event.unicode
                if key.isalnum():
                    self.updateText(self.ibText + event.unicode)


    def OnMouseDown(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            butonIesire = self.butonIesire.GetRect()
            if butonIesire.collidepoint(pos):
                appObj = app.App.GetInstance()
                meniu = gm.Meniu()
                appObj.PlayNewScene(meniu)
            
            butonSave = self.butonSave.GetRect()
            if butonSave.collidepoint(pos) and self.saved == False:
                if self.inputBoxActive == False:
                    self.inputBoxActive = True
                    self.AttachObject(self.inputBox)
                    self.butonSave.SetText("Salvează")
                else:
                    if self.ibText != "":
                        highScore = HighScores.GetInstance()
                        dictHS = highScore.GetHighScore()
                        dictHS[self.ibText] = self.scor
                        highScore.UpdateAndSave(dictHS)
                    else:
                        return

                    self.DetachObject(self.butonSave)
                    self.DetachObject(self.butonIesire)

                    self.butonIesire = Button(self.buttonPosX, self.buttonPosY, self.buttonWidth, self.buttonHeight, 'Ieșire', self.buttonTextColor, self.font, self.fontSize, bgColor=(0, 0, 0))
                    self.butonIesire.SetAlphaLevel(200)
                    self.AttachObject(self.butonIesire)

                    self.DetachObject(self.inputBox)
                    self.inputBoxActive = False

                    self.AttachObject(self.mesajScorSalvat)
                    self.saved = True



