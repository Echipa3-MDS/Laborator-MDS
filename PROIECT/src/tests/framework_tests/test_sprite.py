import unittest
import pygame

from framework.sprite import Sprite
from tests.constants import RES_DIR


class TestSprite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\nTesting Sprites...\n')
    
    def setUp(self):
        pygame.init()
    
    def tearDown(self):
        pygame.quit()


    def test_SizeChanging(self):
        img = pygame.image.load(RES_DIR + 'walk1.bmp')
        sprite = Sprite(img, 0, 0, 50, 50)
        sprite.ChangeSize(18, 99)
        self.assertEqual(sprite.texture.get_rect().size, (18, 99))
    

    def test_Draw(self):
        img = pygame.image.load(RES_DIR + 'walk1.bmp')
        sprite = Sprite(img, 0, 0, 100, 100)

        display = pygame.display.set_mode((800, 600))
        oldPixelBuffer = display.get_view().raw
        sprite._Draw()
        newPixelBuffer = display.get_view().raw
        self.assertNotEqual(oldPixelBuffer, newPixelBuffer)
