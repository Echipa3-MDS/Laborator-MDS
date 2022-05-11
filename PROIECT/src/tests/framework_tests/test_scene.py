import unittest
import pygame

from framework.scene import Scene
from framework.rendered_object import RenderedObject
from tests.constants import RES_DIR


class TestScene(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\nTesting Scene Type...\n')

    def setUp(self):
        pygame.init()
    
    def tearDown(self):
        pygame.quit()


    def test_DrawScene(self):
        class TempRenObj(RenderedObject):
            drawCounter = 0

            def _Draw(self) -> None:
                super()._Draw()
                TempRenObj.drawCounter += 1

        scene = Scene()
        ob1 = TempRenObj(8, 7, 6, 5)
        ob2 = TempRenObj(9, 1, 2, 3)
        ob3 = TempRenObj(7, 6, 5, 4)
        scene.AttachObject(ob1)
        ob1.AttachObject(ob2)
        ob1.AttachObject(ob3)

        pygame.display.set_mode((800, 600))
        scene.DrawScene()

        self.assertEqual(TempRenObj.drawCounter, 3)

    
    def test_ChangeBgImage(self):
        scene = Scene()
        bgImage = pygame.image.load(RES_DIR + 'walk1.bmp')
        scene.ChangeBgImage(bgImage)
        self.assertEqual(scene.bgImage, bgImage)
    

    def test_ChangeBgColor(self):
        scene = Scene()
        bgColor = pygame.Color(123, 123, 123)
        scene.ChangeBgColor(bgColor)
        self.assertEqual(scene.bgColor, bgColor)

    
    def test_DrawBgImage(self):
        scene = Scene()
        bgImage = pygame.image.load(RES_DIR + 'walk1.bmp')
        scene.ChangeBgImage(bgImage)

        display = pygame.display.set_mode((800, 600))
        oldPixelBuffer = display.get_view().raw
        scene._Draw()
        newPixelBuffer = display.get_view().raw
        self.assertNotEqual(oldPixelBuffer, newPixelBuffer)
    

    def test_DrawBgColor(self):
        scene = Scene()
        bgColor = pygame.Color(215, 215, 215, 80)
        scene.ChangeBgColor(bgColor)

        display = pygame.display.set_mode((800, 600))
        oldPixelBuffer = display.get_view().raw
        scene._Draw()
        newPixelBuffer = display.get_view().raw
        self.assertNotEqual(oldPixelBuffer, newPixelBuffer)

    def test_OnSceneExit(self):
        class TestScene(Scene):
            def __init__(self) -> None:
                super().__init__()
                self.sceneExit = False
            
            def OnSceneExit(self):
                self.sceneExit = True
        
        testScene = TestScene()
        testScene.OnSceneExit()
        self.assertTrue(testScene.sceneExit)
