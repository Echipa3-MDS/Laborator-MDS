import unittest
import pygame

from framework.update_scheduler import UpdateScheduler
from framework.constants import *
from game.game_session import GameSession
from game.obstacles.laser_rocket_wave import LaserRocketWave
from game.obstacles.coin_matrix import CoinMatrix


class TestLaserRocketWave(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print('\nTesting Obstacles: Lasers and Rockets Wave...\n')
        pygame.init()
        pygame.display.set_mode((800, 600))
    

    @classmethod
    def tearDownClass(cls):
        pygame.quit()


    def test_SetActive(self):
        lrWave = LaserRocketWave(GameSession())
        lrWave.SetActive()
        scheduler = UpdateScheduler.GetInstance()
        self.assertTrue(lrWave.UpdateLasers in scheduler.updatesScheduled and lrWave.UpdateRockets in scheduler.updatesScheduled)
    

    def test_CleanUp(self):
        lrWave = LaserRocketWave(GameSession())
        lrWave.SetActive()
        lrWave.CleanUp()
        scheduler = UpdateScheduler.GetInstance()
        self.assertTrue(lrWave.UpdateLasers not in scheduler.updatesScheduled and lrWave.UpdateRockets not in scheduler.updatesScheduled)


    def test_UpdateLasers(self):
        lrWave = LaserRocketWave(GameSession(), False)
        lrWave.UpdateLasers(2 * lrWave.lasers[-1].GetRect().centerx / -lrWave.gameScene.sceneXVelocity)
        self.assertIn(pygame.event.Event(pygame.USEREVENT), pygame.event.get())
    

    def test_UpdateRockets(self):
        lrWave = LaserRocketWave(GameSession())
        lrWave.UpdateLasers(2 * lrWave.lasers[-1].GetDisplayPos().x / -lrWave.gameScene.sceneXVelocity)
        lrWave.UpdateRockets(lrWave.warningDuration)
        lrWave.UpdateRockets(2 * lrWave.currentRocket.GetDisplayPos().x / lrWave.rocketSpeed)
        self.assertIn(pygame.event.Event(pygame.USEREVENT), pygame.event.get())
    

    def test_UpdateCoins(self):
        lrWave = LaserRocketWave(GameSession(), False)
        lrWave.UpdateCoins(2 * lrWave.coinBlocks[-1].GetDisplayPos().x / -lrWave.gameScene.sceneXVelocity)
        self.assertTrue(lrWave.remainingBlocks == 0)
    

    def test_ResetWave(self):
        lrWave = LaserRocketWave(GameSession())
        lrWave.ResetWave()
        self.assertTrue(lrWave.remainingLasers == lrWave.totalLasers and len(lrWave.coinBlocks) > 0 and lrWave.currentRocket is not None)
    

    def test_CheckCollision(self):
        lrWave = LaserRocketWave(GameSession(), False)
        lrWave.UpdateLasers(lrWave.lasers[0].GetRect().centerx / -lrWave.gameScene.sceneXVelocity)

        playerPixelMask = pygame.mask.Mask((DISPLAY_WIDTH, DISPLAY_HEIGHT), True)
        playerRect = pygame.Rect(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.assertTrue(lrWave.CheckCollision(playerPixelMask, playerRect))
    

    def test_CheckCoinCollision(self):
        lrWave = LaserRocketWave(GameSession(), False)
        lrWave.coinBlocks.append(CoinMatrix(0, 0, 100, 100))

        playerRect = pygame.Rect(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.assertIsNotNone(lrWave.CheckCoinCollision(playerRect))
