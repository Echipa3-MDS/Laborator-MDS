import pygame

from .constants import *
from .events_manager import EventsManager
from .update_scheduler import UpdateScheduler
from .scene import Scene


class App:
    __instance = None
    
    @classmethod
    def GetInstance(cls) -> 'App':
        if cls.__instance is None:
            cls.__instance = App()
        return cls.__instance


    @staticmethod
    def Init() -> bool:
        pygame.init()
        return pygame.get_init()


    @staticmethod
    def Quit() -> bool:
        pygame.quit()
        return not pygame.get_init()


    def __init__(self) -> None:
        # Fereastra aplicatiei
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("Proiect MDS")

        # Scena afisata de aplicatie
        self.currentScene = None

        self.eventManager = EventsManager.GetInstance()
        self.updateScheduler = UpdateScheduler.GetInstance()
    

    def PlayNewScene(self, scene: Scene) -> None:
        self.eventManager.ClearListeners()
        self.updateScheduler.ClearSchedule()
        self.currentScene = scene


    def Run(self, firstScene: Scene) -> None:
        self.currentScene = firstScene

        isRunning = True
        while isRunning:
            self.updateScheduler.CalculateDeltaTime()
            isRunning = self.eventManager.ProcessEvents()
            self.updateScheduler.UpdateAll()
            self.currentScene.DrawScene()
