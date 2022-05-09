import unittest
import pygame

from framework.app import App
from framework.scene import Scene
from framework.events_manager import EventsManager
from framework.update_scheduler import UpdateScheduler


class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\nTesting App Class...\n')

    def setUp(self):
        if App.__dict__['_App__instance'] is not None:
            App.__dict__['_App__instance'].__init__()
    

    def test_GetInstance(self):
        self.assertIsInstance(App.GetInstance(), App)
    

    def test_Singleton(self):
        app1 = App.GetInstance()
        app2 = App.GetInstance()
        self.assertEqual(id(app1), id(app2))


    def test_Init(self):
        App.Init()
        self.assertTrue(pygame.get_init())
    

    def test_Quit(self):
        App.Init()
        App.Quit()
        self.assertFalse(pygame.get_init())

    
    def test_PlayNewScene(self):
        App.Init()
        app = App.GetInstance()
        scene = Scene()
        app.PlayNewScene(scene)
        App.Quit()
        self.assertEqual(id(app.currentScene), id(scene))
    

    def test_Run(self):
        App.Init()

        class HelperScene(Scene):
            def __init__(self) -> None:
                super().__init__()
                self.numberOfUpdates = 0
                self.numberOfEvents = 0
                UpdateScheduler.GetInstance().ScheduleUpdate(self.update)
                EventsManager.GetInstance().AddListener(pygame.USEREVENT, self.event)
            
            def update(self, deltatime: float) -> None:
                self.numberOfUpdates += 1
            
            def event(self, event: pygame.event.Event) -> None:
                self.numberOfEvents += 1
        
        scene = HelperScene()

        pygame.event.post(pygame.event.Event(pygame.USEREVENT))
        pygame.event.post(pygame.event.Event(pygame.USEREVENT))
        pygame.event.post(pygame.event.Event(pygame.USEREVENT))
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        App.GetInstance().Run(scene)
        ranFrames = min(scene.numberOfUpdates, scene.numberOfEvents)
        
        App.Quit()

        self.assertGreater(ranFrames, 0)
