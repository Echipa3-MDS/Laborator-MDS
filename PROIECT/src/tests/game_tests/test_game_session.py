import unittest
import pygame

import framework.app as app
from framework.constants import *
from framework.update_scheduler import UpdateScheduler
from game.game_session import GameSession
from game.game_over import GameOver
from game.pause_menu import PauseMenu
from game.obstacles.ray_wave import RayWave


class TestGameSession(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print('\nTesting Game Session...\n')
        pygame.init()
        pygame.display.set_mode((800, 600))
    

    @classmethod
    def tearDownClass(cls):
        pygame.quit()
    

    def test_UpdateSceneVelocity(self):
        gameSession = GameSession()
        gameSession.sceneXVelocity = -200
        gameSession.sceneAcceleration = 50
        gameSession.UpdateSceneVelocity(1)
        self.assertEqual(gameSession.sceneXVelocity, -250)
    

    def test_UpdateBackground(self):
        gameSession = GameSession()
        gameSession.sceneXVelocity = -200
        gameSession.bg.ChangeRelativePos((100, 100))
        gameSession.UpdateBackground(1)
        self.assertEqual(gameSession.bg.GetRelativePos().x, -100)
    

    def test_UpdateScore(self):
        gameSession = GameSession()
        scoreBefore = gameSession.score
        gameSession.UpdateScore(1.6)
        self.assertNotEqual(scoreBefore, gameSession.score)
    

    def test_UpdatePlayer(self):
        gameSession = GameSession()
        gameSession.playerYVelocity = 50
        gameSession.playerState.GetRect().top = 200
        gameSession.gravitationalAcceleration = 20
        gameSession.UpdatePlayer(1)
        self.assertEqual(gameSession.playerState.GetRect().top, 170)


    def test_UpdatePlayerDying(self):
        gameSession = GameSession()
        UpdateScheduler.GetInstance().ScheduleUpdate(gameSession.UpdatePlayerDying)

        gameSession.playerYVelocity = -50
        gameSession.playerState.GetRect().top = DISPLAY_HEIGHT - 70
        gameSession.gravitationalAcceleration = 20
        gameSession.UpdatePlayerDying(1)
        gameSession.sceneXVelocity = -100
        gameSession.sceneDeceleration = 100
        gameSession.UpdatePlayerDying(1)
        
        gameSession.UpdatePlayerDying(1)
        self.assertNotIn(gameSession.UpdatePlayerDying, UpdateScheduler.GetInstance().updatesScheduled)

    
    def test_OnPlayerDead(self):
        gameSession = GameSession()
        app.App.GetInstance().currentScene = gameSession

        gameSession.playerLives = 1
        gameSession.OnPlayerDead()
        gameSession.collectedCoins = 0
        gameSession.OnPlayerDead()
        self.assertIsInstance(app.App.GetInstance().currentScene, GameOver)
    

    def test_WaveTransitionAgent(self):
        gameSession = GameSession()
        gameSession.obstacleWave = None
        gameSession.WaveTransitionAgent(gameSession.timeBetweenWaves)
        self.assertIsNotNone(gameSession.obstacleWave)
    

    def test_OnWaveEnd(self):
        gameSession = GameSession()
        gameSession.obstacleWave = RayWave(gameSession)
        gameSession.OnWaveEnd(pygame.event.Event(pygame.USEREVENT))
        self.assertTrue(gameSession.obstacleWave is None and gameSession.WaveTransitionAgent in UpdateScheduler.GetInstance().updatesScheduled)


    def test_OnButtonPause(self):
        gameSession = GameSession()
        app.App.GetInstance().currentScene = gameSession
        gameSession.OnButtonPause(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': gameSession.pauseButton.GetRect().center}))
        self.assertIsInstance(app.App.GetInstance().currentScene, PauseMenu)
    

    def test_AddCoins(self):
        gameSession = GameSession()
        gameSession.collectedCoins = 80
        gameSession.AddCoins(40)
        self.assertEqual(gameSession.collectedCoins, 120)
    

    def test_AddLives(self):
        gameSession = GameSession()
        gameSession.playerLives = 5
        gameSession.AddLives(2)
        self.assertEqual(gameSession.playerLives, 7)
    

    def test_RevivePlayer(self):
        gameSession = GameSession()
        gameSession.RevivePlayer()
        self.assertTrue(gameSession.playerState is gameSession.playerWalk and gameSession.sceneXVelocity == gameSession.sceneVelocityOnDeath)
