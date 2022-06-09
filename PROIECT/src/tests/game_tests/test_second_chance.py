import unittest
import pygame

import framework.app as app
from game.second_chance import SecondChanceInterface
from game.game_session import GameSession
from game.game_over import GameOver


class TestSecondChance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\nTesting Second Chance Interface...\n')
        pygame.init()
        pygame.display.set_mode((800, 600))


    @classmethod
    def tearDownClass(cls):
        pygame.quit

    
    def test_UpdateInterface(self):
        gameSession = GameSession()
        displayState = pygame.Surface((1, 1))
        scInterface = SecondChanceInterface(gameSession, displayState, 100, 200)

        scInterface.remainingTime = 10
        scInterface.UpdateInterface(2)
        self.assertEqual(scInterface.remainingTime, 8)

    
    def test_ToGameOver(self):
        gameSession = GameSession()
        displayState = pygame.Surface((1, 1))
        scInterface = SecondChanceInterface(gameSession, displayState, 102, 103)

        app.App.GetInstance().currentScene = scInterface
        scInterface.ToGameOver()
        self.assertIsInstance(app.App.GetInstance().currentScene, GameOver)
    

    def test_ButtonBuy(self):
        gameSession = GameSession()
        displayState = pygame.Surface((1, 1))
        scInterface = SecondChanceInterface(gameSession, displayState, 171, 169)

        app.App.GetInstance().currentScene = scInterface
        SecondChanceInterface.newLifePrice = 100
        gameSession.collectedCoins = 700
        
        scInterface.OnButtonBuy(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': scInterface.buttonBuyLife.GetRect().center}))
        self.assertTrue(app.App.GetInstance().currentScene is gameSession and gameSession.collectedCoins == 600)

    
    def test_ButtonQuit(self):
        gameSession = GameSession()
        displayState = pygame.Surface((1, 1))
        scInterface = SecondChanceInterface(gameSession, displayState, 372, 341)

        app.App.GetInstance().currentScene = scInterface
        scInterface.OnButtonQuit(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': scInterface.buttonQuit.GetRect().center}))
        self.assertTrue(isinstance(app.App.GetInstance().currentScene, GameOver))
