import unittest
import pygame

from framework.text_object import TextObject


class TestTextObj(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print('\nTesting Text Objects...\n')
    
    def setUp(self):
        pygame.init()
    
    def tearDown(self):
        pygame.quit()


    def test_FontLoading(self):
        txt = TextObject('TEST', (0, 0, 0), 'Consolas', 14, 0, 0)
        self.assertIsInstance(txt.font, pygame.font.Font)
    

    def test_SurfaceRendering(self):
        txt = TextObject('TEST', (0, 0, 0), 'Consolas', 14, 0, 0)
        self.assertIsInstance(txt.textSurface, pygame.Surface)

    
    def test_TextChanging(self):
        txt = TextObject('TEST', (3, 2, 1), 'Times New Roman', 14, 123, 53)
        txt.ChangeText('TEXT_CHANGE')
        self.assertEqual(txt.text, 'TEXT_CHANGE')
    

    def test_Draw(self):
        txt = TextObject('TEST', (3, 2, 1), 'Times New Roman', 14, 123, 53)
        
        display = pygame.display.set_mode((800, 600))
        oldPixelBuffer = display.get_view().raw
        txt._Draw()
        newPixelBuffer = display.get_view().raw
        self.assertNotEqual(oldPixelBuffer, newPixelBuffer)
