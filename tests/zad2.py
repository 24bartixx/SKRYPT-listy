import unittest
from tasks.zad2 import *

class TestZad2(unittest.TestCase):

    def test_forall(self):
        result = forall(lambda x: x > 0, [1, 2, 3, 4])
        self.assertTrue(result)

        result = forall(lambda x: x > 0, [1, -2, 3, 4])
        self.assertFalse(result)

        result = forall(lambda x: x > 0, [])
        self.assertTrue(result)

    def test_exists(self):
        result = exists(lambda x: x < 0, [1, 2, 3, 4])
        self.assertFalse(result)

        result = exists(lambda x: x < 0, [1, -2, 3, 4])
        self.assertTrue(result)

        result = exists(lambda x: x < 0, [])
        self.assertFalse(result)

    def test_atleast(self):
        result = atleast(3, lambda x: x > 0, [1, 2, 3, -4, 0])
        self.assertTrue(result)
        
        result = atleast(4, lambda x: x > 0, [1, 2, 3, -4, 0])
        self.assertFalse(result)

        result = atleast(1, lambda x: x > 0, [])
        self.assertFalse(result)

    def test_atmost(self):
        result = atmost(2, lambda x: x > 0, [1, 2, 3, -4, 0])
        self.assertFalse(result)

        result = atmost(3, lambda x: x > 0, [1, 2, 3, -4, 0])
        self.assertTrue(result)

        result = atmost(1, lambda x: x > 0, [])
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()