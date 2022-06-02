import unittest
import pygame

from game.meniu import Meniu
from game.game_over import GameOver
from framework.app import App


class TestGameOver(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print('\nTesting GameOver...\n')
    
    def setUp(self) -> None:
        pygame.init()

    def tearDown(self) -> None:
        pygame.quit()

    def test_ButonIesire(self):
        appInstance = App.GetInstance()
        appInstance.currentScene = GameOver(100)
        buton = appInstance.currentScene.butonIesire.GetRect()
        appInstance.currentScene.OnMouseDown(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=buton.center))
        self.assertIsInstance(App.GetInstance().currentScene, Meniu)
    
    def test_ButonSalveaza(self):
        appInstance = App.GetInstance()
        appInstance.currentScene = GameOver(100)
        buton = appInstance.currentScene.butonSave.GetRect()
        appInstance.currentScene.OnMouseDown(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=buton.center))

        inputBoxActive = appInstance.currentScene.inputBoxActive
        inputBox = appInstance.currentScene.inputBox
        childrenList= appInstance.currentScene._children

        self.assertTrue(inputBoxActive and inputBox in childrenList)
    
    def test_InputBox(self):
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

    
    

