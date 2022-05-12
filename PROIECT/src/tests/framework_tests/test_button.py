import unittest
import pygame

from framework.button import Button
from tests.constants import RES_DIR


class TestButton(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print('\nTesting Buttons...\n')
    
    def setUp(self):
        pygame.init()
    
    def tearDown(self):
        pygame.quit()

    
    def test_SizeChanging(self):
        button = Button(0, 0, 20, 20, 'TEST', (5, 5, 5), 'Consolas', 12)
        button.ChangeSize(18, 99)
        self.assertEqual(button.textPos, (9 - button.textSurface.get_rect().width / 2, 49 - button.textSurface.get_rect().height / 2))
    

    def test_RelativePosChanging(self):
        button = Button(0, 0, 20, 20, 'TEST', (5, 5, 5), 'Consolas', 12)
        button.ChangeRelativePos((50, 100))
        self.assertEqual(button.textPos, (50 + 20 / 2 - button.textSurface.get_rect().width / 2, 100 + 20 / 2 - button.textSurface.get_rect().height / 2))


    def test_DrawBgImage(self):
        img = RES_DIR + 'walk1.bmp'
        button = Button(0, 0, 50, 50, 'TEST', (0, 0, 0), 'Consolas', 12, img)

        display = pygame.display.set_mode((800, 600))
        oldPixelBuffer = display.get_view().raw
        button._Draw()
        newPixelBuffer = display.get_view().raw
        self.assertNotEqual(oldPixelBuffer, newPixelBuffer)
    

    def test_DrawBgColor(self):
        bgColor = (120, 120, 120)
        button = Button(0, 0, 50, 50, 'TEST', (0, 0, 0), 'Consolas', 12, None, bgColor)

        display = pygame.display.set_mode((800, 600))
        oldPixelBuffer = display.get_view().raw
        button._Draw()
        newPixelBuffer = display.get_view().raw
        self.assertNotEqual(oldPixelBuffer, newPixelBuffer)


    def test_CollidesWithPoint(self):
        button = Button(0, 0, 150, 150)
        point = (100, 50)
        self.assertTrue(button.CollidesWithPoint(point))
