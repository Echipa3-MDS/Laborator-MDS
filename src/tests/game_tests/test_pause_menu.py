import unittest
import pygame

from game.pause_menu import PauseMenu
from game.game_session import GameSession
from game.meniu import Meniu
import framework.app as app


class TestPauseMenu(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\nTesting Pause Menu...\n')
        pygame.init()
        pygame.display.set_mode((800, 600))


    @classmethod
    def tearDownClass(cls):
        pygame.quit

    
    def test_ButtonResume(self):
        gameSession = GameSession()
        pmenu = PauseMenu(gameSession, pygame.Surface((1, 1)))
        
        app.App().GetInstance().currentScene = pmenu
        clickEvent = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (pmenu.buttonResume.GetDisplayPos())})
        pmenu.OnButtonResume(clickEvent)

        self.assertIs(app.App.GetInstance().currentScene, gameSession)
    

    def test_ButtonQuit(self):
        gameSession = GameSession()
        pmenu = PauseMenu(gameSession, pygame.Surface((1, 1)))
        
        app.App().GetInstance().currentScene = pmenu
        clickEvent = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (pmenu.buttonQuit.GetDisplayPos())})
        pmenu.OnButtonQuit(clickEvent)

        self.assertIsInstance(app.App.GetInstance().currentScene, Meniu)


    def test_ButtonMute(self):
        gameSession = GameSession()
        pmenu = PauseMenu(gameSession, pygame.Surface((1, 1)))
        
        app.App().GetInstance().currentScene = pmenu
        clickEvent = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (pmenu.buttonMute.GetDisplayPos())})
        stateBeforeCall = app.App.GetInstance().appMuted
        pmenu.OnButtonMute(clickEvent)

        self.assertNotEqual(app.App.GetInstance().appMuted, stateBeforeCall)
