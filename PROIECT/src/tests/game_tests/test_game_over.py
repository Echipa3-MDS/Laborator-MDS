import imp
import unittest
import copy
from numpy import unicode_
import pygame

from game.meniu import Meniu
from game.game_over import GameOver
from game.game_session import GameSession
from framework.app import App
from framework.scene import Scene
from tests.constants import RES_DIR


class TestGameOver(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print('\nTesting GameOver...\n')
    
    @staticmethod
    def Init() -> bool:
        pygame.init()
        return pygame.get_init()


    @staticmethod
    def Quit() -> bool:
        pygame.quit()
        return not pygame.get_init()

    def test_ButonIesire(self):
        pygame.init()
        appInstance = App.GetInstance()
        appInstance.currentScene = GameOver(100)
        buton = appInstance.currentScene.butonIesire.GetRect()
        appInstance.currentScene.OnMouseDown(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=buton.center))
        self.assertIsInstance(App.GetInstance().currentScene, Meniu)
    
    def test_ButonSalveaza(self):
        pygame.init()
        appInstance = App.GetInstance()
        appInstance.currentScene = GameOver(100)
        buton = appInstance.currentScene.butonSave.GetRect()
        appInstance.currentScene.OnMouseDown(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=buton.center))

        inputBoxActive = appInstance.currentScene.inputBoxActive
        inputBox = appInstance.currentScene.inputBox
        childrenList= appInstance.currentScene._children

        self.assertTrue(inputBoxActive and inputBox in childrenList)
    
    def test_InputBox(self):
        pygame.init()
        appInstance = App.GetInstance()
        appInstance.currentScene = GameOver(100)
        buton = appInstance.currentScene.butonSave.GetRect()
        appInstance.currentScene.OnMouseDown(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=buton.center))

        appInstance.currentScene.OnKeyDown(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_t, unicode = 'T'))
        appInstance.currentScene.OnKeyDown(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e, unicode = 'e'))
        appInstance.currentScene.OnKeyDown(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s, unicode = 'S'))
        appInstance.currentScene.OnKeyDown(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_t, unicode = 't'))
        appInstance.currentScene.OnKeyDown(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e, unicode = 'e'))
        appInstance.currentScene.OnKeyDown(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE))

        self.assertEqual(appInstance.currentScene.ibText, "TeSt")

    
    

