import unittest
import pygame

from framework.update_scheduler import UpdateScheduler
from framework.constants import *
from game.game_session import GameSession
from game.obstacles.ray_wave import RayWave


class TestRayWave(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print('\nTesting Obstacles: Ray Wave...\n')
        pygame.init()
        pygame.display.set_mode((800, 600))
    

    @classmethod
    def tearDownClass(cls):
        pygame.quit()


    def test_SetActive(self):
        rayWave = RayWave(GameSession())
        rayWave.SetActive()
        scheduler = UpdateScheduler.GetInstance()
        self.assertIn(rayWave.UpdateRayOff, scheduler.updatesScheduled)
    

    def test_CleanUp(self):
        gameSession = GameSession()
        rayWave = RayWave(gameSession)
        
        scheduler = UpdateScheduler.GetInstance()
        scheduler.ScheduleUpdate(rayWave.UpdateRayOn)

        rayWave.CleanUp()

        self.assertNotIn(rayWave.UpdateRayOn, scheduler.updatesScheduled)

    
    def test_UpdateRayOff(self):
        gameSession = GameSession()
        rayWave = RayWave(gameSession)

        scheduler = UpdateScheduler.GetInstance()
        scheduler.ScheduleUpdate(rayWave.UpdateRayOff)

        rayWave.UpdateRayOff(rayWave.rayOffDuration)

        self.assertTrue(rayWave.UpdateRayOff not in scheduler.updatesScheduled and rayWave.UpdateRayOn in scheduler.updatesScheduled)

    
    def test_UpdateRayOn(self):
        gameSession = GameSession()
        rayWave = RayWave(gameSession)
        rayWave.UpdateRayOn(rayWave.rayOnDuration)
        self.assertIn(pygame.event.Event(pygame.USEREVENT), pygame.event.get())
    

    def test_ResetWave(self):
        gameSession = GameSession()
        rayWave = RayWave(gameSession)
        self.assertTrue(None not in rayWave.rays and rayWave.rayOffTimeElapsed == 0.0 and rayWave.rayOnTimeElapsed == 0.0)


    def test_CheckCollision(self):
        gameSession = GameSession()
        rayWave = RayWave(gameSession)

        rayWave.UpdateRayOff(rayWave.rayOffDuration)

        playerPixelMask = pygame.mask.Mask((DISPLAY_WIDTH, DISPLAY_HEIGHT), True)
        playerRect = pygame.Rect(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)

        self.assertTrue(rayWave.CheckCollision(playerPixelMask, playerRect))
