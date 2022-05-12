import pygame

from framework.scene import Scene
from framework.animation import Animation
from framework.constants import *
from framework.update_scheduler import UpdateScheduler
from framework.events_manager import EventsManager

from framework.button import Button
from framework.sprite import Sprite
from framework.rendered_object import RenderedObject
from framework.text_object import TextObject

from game.first_scene_example import FirstSceneExample
from game.high_scores import HighScores
import framework.app as app


# from framework.app import App


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

        textColor = (0, 255, 0)
        font = 'arial'
        fontSize = 40
        bgColor = (255, 0, 0)
        bgImage = None
        borderRadius = 5

        

        
        self.butonStart = Button(posX, posY, buttonWidth, buttonHeight, 'Start', textColor, font, fontSize, bgColor, bgImage, borderRadius)
        self.butonHighScores = Button(posX, posY + buttonHeight + 20, buttonWidth, buttonHeight, 'High Scores', textColor, font, fontSize, bgColor, bgImage, borderRadius)
        self.butonExit = Button(posX, posY + 2 * (buttonHeight + 20), buttonWidth, buttonHeight, 'Exit', textColor, font, fontSize, bgColor, bgImage, borderRadius)
        
        highScore = HighScores.GetInstance()
        textHighScore = highScore.GetHighScoreString(10)

        print(textHighScore.split('\n'))
        
        hsWidth = 100
        hsHeight = 400
        hsX = DISPLAY_WIDTH / 2 - hsWidth / 2
        hsY = DISPLAY_HEIGHT / 2 - hsHeight / 2

        self.highScoreBox = RenderedObject(hsX, hsY, hsWidth, hsHeight)


        # self.scoreBoard = TextObject(textBoard, textColor, font, 20, hsX, hsY)

        # self.AttachObject(self.logo)
        # self.AttachObject(self.butonStart)
        # self.AttachObject(self.butonHighScores)
        # self.AttachObject(self.butonExit)
        # self.AttachObject(self.scoreBoard)

        EventsManager.GetInstance().AddListener(pygame.MOUSEBUTTONDOWN, self.OnMouseDown)

        box = pygame.Rect(0, 0, 60, 70)
        pygame.draw.rect(pygame.display.get_surface(), (0, 0, 0), box, 0)

    def OnMouseDown(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            butonStart = self.butonStart.GetRect()
            if butonStart.collidepoint(pos):
                gameScene = FirstSceneExample()
                appObj = app.App.GetInstance()
                appObj.PlayNewScene(gameScene)
            
            butonExit = self.butonExit.GetRect()
            if butonExit.collidepoint(pos):
                quitEvent = pygame.event.Event(pygame.QUIT)
                pygame.event.post(quitEvent)






