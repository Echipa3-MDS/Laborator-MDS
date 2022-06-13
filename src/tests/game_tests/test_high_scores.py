import unittest
import copy

from game.high_scores import HighScores
from tests.constants import RES_DIR


class TestHighScores(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print('\nTesting High Scores...\n')
    
    def test_GetInstance(self):
        instance = HighScores.GetInstance()
        self.assertIsInstance(instance, HighScores)
    
    def test_Singleton(self):
        hs1 = HighScores.GetInstance()
        hs2 = HighScores.GetInstance()
        self.assertEqual(id(hs1), id(hs2))
    
    def test_Update(self):
        instance = HighScores.GetInstance()
        oldHS = copy.deepcopy(instance.GetHighScore())
        instance.Update({'test' : 0})
        newHs = instance.GetHighScore()
        self.assertNotEquals(oldHS, newHs)


