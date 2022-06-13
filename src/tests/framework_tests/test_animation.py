import unittest
import pygame

from framework.animation import Animation
from framework.update_scheduler import UpdateScheduler
from tests.constants import RES_DIR


class TestAnimation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\nTesting Animations...\n')
    
    def setUp(self):
        pygame.init()
    
    def tearDown(self):
        pygame.quit()


    def test_AnimationPlay(self):
        frames = [pygame.image.load(RES_DIR + 'walk1.bmp'), pygame.image.load(RES_DIR + 'walk2.bmp')]
        animation = Animation(0, 0, 100, 100, frames, 0.2)
        
        if UpdateScheduler.__dict__['_UpdateScheduler__instance'] is not None:
            UpdateScheduler.__dict__['_UpdateScheduler__instance'].__init__()
        us = UpdateScheduler.GetInstance()
        
        animation.PlayAnimation()
        self.assertEqual(len(us.updatesScheduled), 1)
    

    def test_AnimationStop(self):
        frames = [pygame.image.load(RES_DIR + 'walk1.bmp'), pygame.image.load(RES_DIR + 'walk2.bmp')]
        animation = Animation(0, 0, 100, 100, frames, 0.2)
        
        if UpdateScheduler.__dict__['_UpdateScheduler__instance'] is not None:
            UpdateScheduler.__dict__['_UpdateScheduler__instance'].__init__()
        us = UpdateScheduler.GetInstance()
        
        us.ScheduleUpdate(animation._Animation__updateFrame)
        animation.StopAnimation()
        self.assertNotIn(animation._Animation__updateFrame, us.updatesScheduled)
    

    def test_AnimationReset(self):
        frames = [pygame.image.load(RES_DIR + 'walk1.bmp'), pygame.image.load(RES_DIR + 'walk2.bmp')]
        animation = Animation(0, 0, 100, 100, frames, 0.2)
        
        animation.frameIndex = 99
        animation.timeSinceChange = 109
        animation.ResetAnimation()
        self.assertTrue(animation.frameIndex == 0 and animation.timeSinceChange == 0)
    

    def test_TransitionTimeChanging(self):
        frames = [pygame.image.load(RES_DIR + 'walk1.bmp'), pygame.image.load(RES_DIR + 'walk2.bmp')]
        animation = Animation(0, 0, 100, 100, frames, 0.2)
            
        animation.timeBetweenFrames = 123
        animation.ChangeTransitionTime(43.5)
        self.assertEqual(animation.timeBetweenFrames, 43.5)
    

    def test_SizeChanging(self):
        frames = [pygame.image.load(RES_DIR + 'walk1.bmp'), pygame.image.load(RES_DIR + 'walk2.bmp')]
        animation = Animation(0, 1, 102, 109, frames, 0.5)

        animation.ChangeSize(18, 51)
        self.assertTrue(animation.frames[0].get_rect().size == (18, 51) and animation.frames[1].get_rect().size == (18, 51))
    

    def test_FrameUpdate(self):
        frames = [pygame.image.load(RES_DIR + 'walk1.bmp'), pygame.image.load(RES_DIR + 'walk2.bmp')]
        animation = Animation(7, 0, 140, 10, frames, 0.1)

        animation._Animation__updateFrame(0.05)
        animation._Animation__updateFrame(0.05)
        self.assertTrue(animation.frameIndex == 1 and animation.timeSinceChange == 0)


    def test_Draw(self):
        frames = [pygame.image.load(RES_DIR + 'walk1.bmp'), pygame.image.load(RES_DIR + 'walk2.bmp')]
        animation = Animation(14, 11, 10, 18, frames, 0.2)

        display = pygame.display.set_mode((800, 600))
        oldPixelBuffer = display.get_view().raw
        animation._Draw()
        newPixelBuffer = display.get_view().raw
        self.assertNotEqual(oldPixelBuffer, newPixelBuffer)

        
