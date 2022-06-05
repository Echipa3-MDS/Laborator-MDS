import sched
import unittest
import pygame

from framework.update_scheduler import UpdateScheduler
from framework.constants import *
from game.obstacles.coin_matrix import CoinMatrix


class TestCoinMatrix(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print('\nTesting Obstacles: Coin Matrix...\n')
        pygame.init()
        pygame.display.set_mode((800, 600))
    

    @classmethod
    def tearDownClass(cls):
        pygame.quit()


    def test_SetActive(self):
        coinMatrix = CoinMatrix(0, 0, 100, 100)
        scheduler = UpdateScheduler.GetInstance()
        
        scheduler.ClearSchedule()
        coinMatrix.SetActive()
        
        isActive = True
        for row in coinMatrix.coinMatrix:
            for coin in row:
                isActive = isActive and (coin._Animation__updateFrame in scheduler.updatesScheduled)
        self.assertTrue(isActive)


    def test_CleanUp(self):
        coinMatrix = CoinMatrix(0, 0, 100, 100)
        scheduler = UpdateScheduler.GetInstance()
        
        scheduler.ClearSchedule()
        coinMatrix.SetActive()
        coinMatrix.CleanUp()
    
        isNotActive = True
        for row in coinMatrix.coinMatrix:
            for coin in row:
                isNotActive = isNotActive and (coin._Animation__updateFrame not in scheduler.updatesScheduled)
        self.assertTrue(isNotActive)
    

    def test_CheckCollision(self):
        coinMatrix = CoinMatrix(0, 0, 100, 100)
        playerRect = pygame.Rect(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.assertIsNotNone(coinMatrix.CheckCollision(playerRect))
