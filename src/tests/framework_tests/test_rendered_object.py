import unittest
import pygame

from framework.rendered_object import RenderedObject


class TestRenderedObject(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\nTesting Rendered Objects...\n')
    
    def setUp(self):
        pygame.init()
    
    def tearDown(self):
        pygame.quit()


    def test_AttachObject(self):
        ob1 = RenderedObject(0, 0, 0, 0)
        ob2 = RenderedObject(0, 0, 0, 0)
        ob1.AttachObject(ob2)
        self.assertIn(ob2, ob1._children)
    

    def test_DetachObject(self):
        ob1 = RenderedObject(0, 0, 0, 0)
        ob2 = RenderedObject(0, 0, 0, 0)
        ob1.AttachObject(ob2)
        ob1.DetachObject(ob2)
        self.assertNotIn(ob2, ob1._children)
    

    def test_MoveBy(self):
        ob1 = RenderedObject(0, 0, 0, 0)
        ob1.MoveBy((7, 11))
        self.assertEqual(ob1._frame.topleft, (7, 11))

    
    def test_ChangeRelativePos(self):
        ob1 = RenderedObject(0, 0, 0, 0)
        ob1.ChangeRelativePos((27, 4))
        self.assertEqual(ob1._relativePos, (27, 4))
    

    def test_ChangeSize(self):
        ob1 = RenderedObject(0, 0, 0, 0)
        ob1.ChangeSize(123, 456)
        self.assertEqual(ob1._frame.size, (123, 456))
    

    def test_GetRelativePos(self):
        ob1 = RenderedObject(18, 199, 0, 0)
        self.assertEqual(ob1.GetRelativePos(), (18, 199))


    def test_GetDisplayPos(self):
        ob1 = RenderedObject(20, 150, 0, 0)
        ob2 = RenderedObject(15, 30, 0, 0)
        ob1.AttachObject(ob2)
        self.assertEqual(ob2.GetDisplayPos(), (35, 180))
    

    def test_GetSize(self):
        ob1 = RenderedObject(1, 2, 77, 99)
        self.assertEqual(ob1.GetSize(), (77, 99))

    
    def test_Visit(self): 

        class TempRenObj(RenderedObject):
            drawCounter = 0

            def _Draw(self) -> None:
                super()._Draw()
                TempRenObj.drawCounter += 1
        
        ob1 = TempRenObj(0, 0, 0, 0)
        ob2 = TempRenObj(0, 0, 0, 0)
        ob3 = TempRenObj(0, 0, 0, 0)
        ob4 = TempRenObj(0, 0, 0, 0)
        ob1.AttachObject(ob2)
        ob1.AttachObject(ob3)
        ob2.AttachObject(ob4)

        ob1._Visit()

        self.assertEqual(TempRenObj.drawCounter, 4)
