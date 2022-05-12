import pygame

from .constants import *
from .events_manager import EventsManager
from .update_scheduler import UpdateScheduler
from .scene import Scene

from game.first_scene_example import FirstSceneExample


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

        # Prima scena rulata de aplicatie
        firstScene = FirstSceneExample()

        # Scena afisata de aplicatie
        self.currentScene = firstScene

        self.eventManager = EventsManager.GetInstance()
        self.updateScheduler = UpdateScheduler.GetInstance()
    

    def PlayNewScene(self, scene: Scene) -> None:
        self.currentScene.OnSceneExit()
        self.eventManager.ClearListeners()
        self.updateScheduler.ClearSchedule()
        self.currentScene = scene
        self.currentScene.OnSceneEnter()


    def Run(self) -> None:
        self.currentScene.OnSceneEnter()
        
        isRunning = True
        while isRunning:
            self.updateScheduler.CalculateDeltaTime()
            isRunning = self.eventManager.ProcessEvents()
            self.updateScheduler.UpdateAll()
            self.currentScene.DrawScene()
            
        self.currentScene.OnSceneExit()
