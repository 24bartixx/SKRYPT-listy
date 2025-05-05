import unittest
from types import FunctionType
from tasks.zad4 import make_generator


class TestZad4(unittest.TestCase):
    
    def _fibonacci(self,n):
        if n <= 0:
            raise ValueError("Input must be a non-negative integer!")
        
        num1 = 0
        num2 = 1
        
        for _ in range(n-1):
            new_num = num1 + num2
            num1 = num2
            num2 = new_num
        
        return num1
            
    def _arithmetic_sequence(self, a0, r, n):
        return a0 + (n-1) * r

    def _geomethic_sequence(self, a0, r, n):
        return a0 * r**(n-1)
    
    def test_fibonacci(self):
        generator = make_generator(self._fibonacci)
        self.assertEqual(next(generator), 0)
        self.assertEqual(next(generator), 1)
        self.assertEqual(next(generator), 1)
        self.assertEqual(next(generator), 2)
        self.assertEqual(next(generator), 3)
        self.assertEqual(next(generator), 5)
        self.assertEqual(next(generator), 8)
        self.assertEqual(next(generator), 13)
        
    def test_arithmetic_sequence(self):
        generator = make_generator(lambda n: self._arithmetic_sequence(2,1,n))
        self.assertEqual(next(generator), 2)
        self.assertEqual(next(generator), 3)
        self.assertEqual(next(generator), 4)
        self.assertEqual(next(generator), 5)
        self.assertEqual(next(generator), 6)
        self.assertEqual(next(generator), 7)
        
    def test_geometric_sequence(self):
        generator = make_generator(lambda n: self._geomethic_sequence(3,2,n))
        self.assertEqual(next(generator), 3)
        self.assertEqual(next(generator), 6)
        self.assertEqual(next(generator), 12)
        self.assertEqual(next(generator), 24)
        self.assertEqual(next(generator), 48)
        self.assertEqual(next(generator), 96)
        self.assertEqual(next(generator), 192)

    
if __name__ == "__main__":
    unittest.main()
    