import pygame

from framework.scene import Scene
from framework.animation import Animation
from framework.constants import *
from framework.update_scheduler import UpdateScheduler
from framework.events_manager import EventsManager


class FirstSceneExample(Scene):
    """
    Deplasare a unui caracter. SPACEBAR schimba directia de deplasare. ESC pentru a inchide aplicatia.
    """

    def __init__(self) -> None:
        super().__init__()  # IMPORTANT! Trebuie apelat in cadrul tuturor scenelor create

        whiteColor = (255, 255, 255)
        self.ChangeBgColor(whiteColor)

        playerTex1 = pygame.image.load(RES_DIR + "walk1.bmp")
        playerTex2 = pygame.image.load(RES_DIR + "walk2.bmp")
        playerTextures = [playerTex1, playerTex2]
        playerWidth = 80
        playerHeight = 80
        playerX = 0
        playerY = DISPLAY_HEIGHT / 2 - playerHeight / 2
        self.moveDirection = pygame.math.Vector2(1, 0)
        
        # Timpul dintre cadrele animatiei (in secunde)
        frameTime = 0.15

        self.playerAnim = Animation(playerX, playerY, playerWidth, playerHeight, playerTextures, frameTime)
        self.AttachObject(self.playerAnim)


    def OnSceneEnter(self) -> None:
        self.playerAnim.PlayAnimation()
        UpdateScheduler.GetInstance().ScheduleUpdate(self.update)
        EventsManager.GetInstance().AddListener(pygame.KEYDOWN, self.OnKeyDown)


    def update(self, deltaTime: float) -> None:
        relativePos = self.playerAnim.GetRelativePos()
        playerWidth = self.playerAnim.GetSize()[0]
        sceneWidth = self.GetSize()[0]

        if self.moveDirection.x > 0:
            # Merge spre dreapta
            if relativePos.x > sceneWidth:
                # Daca a depasit marginea din dreapta, duce caracterul inainte de marginea din stanga
                newPos = (-playerWidth, relativePos.y)
                self.playerAnim.ChangeRelativePos(newPos)
        elif self.moveDirection.x < 0:
            # Merge spre stanga
            if relativePos.x + playerWidth < 0:
                # Daca a depasit marginea din stanga, Duce caracterul dupa marginea din dreapta
                newPos = (sceneWidth, relativePos.y)
                self.playerAnim.ChangeRelativePos(newPos)
        
        # Viteza de deplasare a caracterului (numarul de unitati (pixeli) pe secunda)
        moveSpeed = 150

        moveVelocity = self.moveDirection * moveSpeed
        moveAmount = moveVelocity * deltaTime
        self.playerAnim.MoveBy(moveAmount)
    

    def OnKeyDown(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_SPACE:
            self.moveDirection.x = -self.moveDirection.x
        elif event.key == pygame.K_ESCAPE:
            quitEvent = pygame.event.Event(pygame.QUIT)
            pygame.event.post(quitEvent)
