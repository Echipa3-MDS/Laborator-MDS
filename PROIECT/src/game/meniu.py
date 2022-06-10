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

        appObj = app.App.GetInstance()

        logoImg = pygame.image.load(RES_DIR + "img\logo.png")
        logoWidth = 350
        logoHeight = 175
        logoPosX = (DISPLAY_WIDTH / 11)*8 - logoWidth / 2
        logoPosY = 15

        self.logo = Sprite(logoImg, logoPosX, logoPosY, logoWidth, logoHeight)

        buttonWidth = 280
        buttonHeight = 60
        posX = (DISPLAY_WIDTH / 11)*8 - buttonWidth / 2
        posY = 200

        textColor = (255, 255, 255)
        font = RES_DIR + "font\Happy School.ttf"
        fontSize = 40
        bgColor = (0, 0, 0)
        bgImage = RES_DIR + "img/ButtonBg.png"
        self.ChangeBgImage(pygame.transform.scale(pygame.image.load(RES_DIR + "img/bgconcept.png"),(DISPLAY_WIDTH,DISPLAY_HEIGHT)))
        borderRadius = 5
        buttonTop = 20
        alpha = 255
        

        self.butonStart = Button(posX, posY, buttonWidth, buttonHeight, 'Start', textColor, font, fontSize, bgImage, bgColor)
        self.butonHighScores = Button(posX, posY + buttonHeight + buttonTop, buttonWidth, buttonHeight, 'Top Scoruri', textColor, font, fontSize, bgImage, bgColor)
        self.butonInstructiuni = Button(posX, posY + 2 * (buttonHeight + buttonTop), buttonWidth, buttonHeight, 'Instructiuni', textColor, font, fontSize, bgImage, bgColor)
        self.butonExit = Button(posX, posY + 3 * (buttonHeight + buttonTop), buttonWidth, buttonHeight, 'Iesire', textColor, font, fontSize, bgImage, bgColor)
        
        self.butonStart.SetAlphaLevel(alpha)
        self.butonHighScores.SetAlphaLevel(alpha)
        self.butonInstructiuni.SetAlphaLevel(alpha)
        self.butonExit.SetAlphaLevel(alpha)
        
        hsWidth = 700
        hsHeight = 400
        hsX = DISPLAY_WIDTH / 2 - hsWidth / 2
        hsY = DISPLAY_HEIGHT / 2 - hsHeight / 2

        self.scoreBoard = Box(hsX, hsY, hsWidth, hsHeight, (42, 47, 46))
        self.instructionBox = Box(hsX, hsY, hsWidth, hsHeight, (42, 47, 46))
        
        hsExitWidth = 50
        hsExitHeight = 50
        hsExitX = hsWidth - hsExitWidth
        hsExitY = 0
        self.hsExitButton = Button(hsExitX, hsExitY, hsExitWidth, hsExitHeight, 'X', textColor, font, 50, None, bgColor)
        self.hsExitButton.SetAlphaLevel(alpha)
        self.scoreBoard.AttachObject(self.hsExitButton)


        self.inExitButton = Button(hsExitX, hsExitY, hsExitWidth, hsExitHeight, 'X', textColor, font, 50, None, bgColor)
        self.inExitButton.SetAlphaLevel(alpha)
        self.instructionBox.AttachObject(self.inExitButton)

        highScore = HighScores.GetInstance()
        textHighScore = highScore.GetHighScoreString(10)
        liniHighScore = textHighScore.strip().split('\n')
        liniHighScore[-1] += ' '

        hsTop = 10
        hsFontSize = 20
        
        for it, linie in enumerate(liniHighScore):
            fontT = pygame.font.SysFont('arial', 20)
            textSurface = fontT.render(linie, True, textColor)
            textWidth = textSurface.get_width()
            textHeight = textSurface.get_height()

            linieY = hsTop + textHeight
            linieX = hsWidth / 2 - textWidth / 2

            textHSObject = TextObject(linie, (255, 255, 255), 'arial', 20, linieX, it * (linieY))
            self.scoreBoard.AttachObject(textHSObject)

        textInstructiuni = """
                            Instrucțiuni

                            Jocul este de tip 'Endless Runner' și constă în depășirea
                            obstacolelor și colectarea monedelor de către jucător, astfel obținând un scor cât mai mare.
                            Scorul final este dat de distanța parcursă adunată cu numărul de monede rămase.
                            Pe măsură ce scorul crește, dificultatea se mărește prin accelerarea obstacolelor.
                            Jocul prezintă și un sistem de vieți. În cazul în care jucătorul se lovește de obstacole,
                            poate continua dacă mai are vieți rămase sau dacă plătește 200 de monede.

                            Pentru a se feri de obstacole, jucătorul poate face caracterul 
                            să zboare folosind tasta W.
                            """
        liniInstructiuni = textInstructiuni.strip().split('\n')
        for it, linie in enumerate(liniInstructiuni):
            linie = linie.strip()
            if it > 0:
                fontT = pygame.font.SysFont('arial', hsFontSize)
            else:
                fontT = pygame.font.SysFont('arial', hsFontSize + 10)
            textSurface = fontT.render(linie, True, textColor)
            textWidth = textSurface.get_width()
            textHeight = textSurface.get_height()

            linieY = hsTop + textHeight
            linieX = hsWidth / 2 - textWidth / 2
            if it > 0:
                textHSObject = TextObject(linie, (255, 255, 255), 'arial', hsFontSize, linieX, it * (linieY))
            else:
                textHSObject = TextObject(linie, (255, 255, 255), 'arial', hsFontSize + 10, linieX, it * (linieY))
            self.instructionBox.AttachObject(textHSObject)
        muteButtonW = 50
        muteButtonH = 50
        muteButtonX = DISPLAY_WIDTH - muteButtonW - 10
        muteButtonY = 10
        self.buttonMute = Button(muteButtonX, muteButtonY, muteButtonW, muteButtonH)
        self.AttachObject(self.buttonMute)
        self.mutedIcon = pygame.transform.scale(pygame.image.load(RES_DIR + "no-sound.png"), (muteButtonW, muteButtonH))
        self.unmutedIcon = pygame.transform.scale(pygame.image.load(RES_DIR + "sound.png"), (muteButtonW, muteButtonH))
        if app.App.GetInstance().IsMuted():
            self.buttonMute.SetBgImage(self.mutedIcon)
        else:
            self.buttonMute.SetBgImage(self.unmutedIcon)

        self.AttachObject(self.logo)
        self.AttachObject(self.butonStart)
        self.AttachObject(self.butonHighScores)
        self.AttachObject(self.butonInstructiuni)
        self.AttachObject(self.butonExit)
        self.AttachObject(self.buttonMute)
        

        self.scoreBoardActive = False
        self.instructionBoxActive = False
        # self.AttachObject(self.scoreBoard)
        # self.AttachObject(self.instructionBox)

        
    
    def OnSceneEnter(self) -> None:
        super().OnSceneEnter()
        EventsManager.GetInstance().AddListener(pygame.MOUSEBUTTONDOWN, self.OnMouseDown)


    def OnMouseDown(self, event: pygame.event.Event) -> None:
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if not self.scoreBoardActive and not self.instructionBoxActive:
                butonStart = self.butonStart.GetRect()
                if butonStart.collidepoint(pos):
                    self.butonStart.ClickedSound(app.App.GetInstance().IsMuted())
                    gameScene = GameSession()
                    appObj = app.App.GetInstance()
                    appObj.PlayNewScene(gameScene)
                
                butonExit = self.butonExit.GetRect()
                if butonExit.collidepoint(pos):
                    self.butonExit.ClickedSound(app.App.GetInstance().IsMuted())
                    quitEvent = pygame.event.Event(pygame.QUIT)
                    pygame.event.post(quitEvent)
                
                butonHighScore = self.butonHighScores.GetRect()
                if butonHighScore.collidepoint(pos):
                    self.butonHighScores.ClickedSound(app.App.GetInstance().IsMuted())
                    self.DetachObject(self.logo)
                    self.DetachObject(self.butonStart)
                    self.DetachObject(self.butonHighScores)
                    self.DetachObject(self.butonInstructiuni)
                    self.DetachObject(self.butonExit)
                    self.AttachObject(self.scoreBoard)
                    self.scoreBoardActive = True
                
                butonInstructiuni = self.butonInstructiuni.GetRect()
                if butonInstructiuni.collidepoint(pos):
                    self.butonInstructiuni.ClickedSound(app.App.GetInstance().IsMuted())
                    self.DetachObject(self.logo)
                    self.DetachObject(self.butonStart)
                    self.DetachObject(self.butonHighScores)
                    self.DetachObject(self.butonInstructiuni)
                    self.DetachObject(self.butonExit)
                    self.AttachObject(self.instructionBox)
                    self.instructionBoxActive = True

            else:
                if self.scoreBoardActive:
                    butonExitHs = self.hsExitButton.GetRect()
                    if butonExitHs.collidepoint(pos):
                        self.hsExitButton.ClickedSound(app.App.GetInstance().IsMuted())
                        self.AttachObject(self.logo)
                        self.AttachObject(self.butonStart)
                        self.AttachObject(self.butonHighScores)
                        self.AttachObject(self.butonInstructiuni)
                        self.AttachObject(self.butonExit)
                        self.DetachObject(self.scoreBoard)
                        self.scoreBoardActive = False
                elif self.instructionBoxActive:
                    butonExitIn = self.inExitButton.GetRect()
                    if butonExitIn.collidepoint(pos):
                        self.inExitButton.ClickedSound(app.App.GetInstance().IsMuted())
                        self.AttachObject(self.logo)
                        self.AttachObject(self.butonStart)
                        self.AttachObject(self.butonHighScores)
                        self.AttachObject(self.butonInstructiuni)
                        self.AttachObject(self.butonExit)
                        self.DetachObject(self.instructionBox)
                        self.instructionBoxActive = False
            butonMute = self.buttonMute.GetRect()
            if butonMute.collidepoint(pos):
                appInst = app.App.GetInstance()
                appInst.SwitchMuteOption()
                if(not appInst.IsMuted()):
                    pygame.mixer.Sound(RES_DIR + "audio/Click.ogg").play()
                self.buttonMute.SetBgImage(self.mutedIcon if appInst.IsMuted() else self.unmutedIcon)