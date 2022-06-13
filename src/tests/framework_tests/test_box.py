import unittest
import pygame

from framework.box import Box
from tests.constants import RES_DIR


class TestBox(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print('\nTesting Boxes...\n')
    
    def setUp(self):
        pygame.init()
    
    def tearDown(self):
        pygame.quit()


    def test_DrawBgImage(self):
        img = RES_DIR + 'walk1.bmp'
        box = Box(0, 0, 20, 20, (0, 0, 0), img, 5)

        display = pygame.display.set_mode((800, 600))
        oldPixelBuffer = display.get_view().raw
        box._Draw()
        newPixelBuffer = display.get_view().raw
        self.assertNotEqual(oldPixelBuffer, newPixelBuffer)
    

    def test_DrawBgColor(self):
        bgColor = (120, 120, 120)
        box = Box(0, 0, 20, 20, bgColor)

        display = pygame.display.set_mode((800, 600))
        oldPixelBuffer = display.get_view().raw
        box._Draw()
        newPixelBuffer = display.get_view().raw
        self.assertNotEqual(oldPixelBuffer, newPixelBuffer)
