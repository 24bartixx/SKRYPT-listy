from cmath import sqrt
import unittest
from tasks.zad1 import *

class TestZad2(unittest.TestCase):
    
    def test_acronym(self):
        result = acronym(["Politechnika", "Warszawska"])
        self.assertEqual(result, "PW")
        
        result = acronym(["Główny", "Urząd", "Statystyczny"])
        self.assertEqual(result, "GUS")
        
        result = acronym(["You", "only", "live", "once"])
        self.assertEqual(result, "YOLO")
        
        result = acronym(["By", "the", "way"])
        self.assertEqual(result, "BTW")
        
        result = acronym([])
        self.assertEqual(result, "")
        
        
    def test_median(self):
        result = median([1, 3, 2])
        self.assertEqual(result, 2)

        result = median([1, 3, 2, 4])
        self.assertEqual(result, 2.5)

        result = median([-1, -3, -2])
        self.assertEqual(result, -2)

        result = median([])
        self.assertIsNone(result)

        result = median([i for i in range(0, 1001)])
        self.assertEqual(result, 500)
            
            
    def test_pierwiastek(self):
        with self.assertRaises(ValueError):
            pierwiastek(-1, 1e-10)
        
        self.assertAlmostEqual(pierwiastek(0, 1e-10), 0, delta = 1e-10)
        self.assertAlmostEqual(pierwiastek(1, 1e-10), 1, delta = 1e-10)
        
        for val in [0.01, 0.25, 2, 4, 7, 153, 1000, 2341059]:
            with self.subTest(val=val):
                self.assertAlmostEqual(pierwiastek(val, 1e-10), sqrt(val), delta = 1e-10)
                
        
    def test_make_alpha_dict(self):
        test_str = "on i ona"
        result = make_alpha_dict(test_str)
        
        assert set(result.keys()) == set(test_str)

        assert result["o"] == ["on", "ona"]
        assert result["n"] == ["on", "ona"]
        assert result["i"] == ["i"]
        assert result["a"] == ["ona"]
        assert result[" "] == []
        
        test_str = "Alice asked Adam to add an anti-aging agent; Adam's answer amazed Alice!"
        result = make_alpha_dict(test_str)
        
        assert set(result.keys()) == set(test_str)
        
        assert result["A"] == ["Alice", "Adam", "Adam's", "Alice!"]
        assert result["l"] == ["Alice", "Alice!"]
        assert result["i"] == ["Alice", "anti-aging", "Alice!"]
        assert result["c"] == ["Alice", "Alice!"]
        assert result["e"] == ["Alice", "asked", "agent;", "answer", "amazed", "Alice!"]
        assert result["a"] == ["asked", "Adam", "add", "an", "anti-aging", "agent;", "Adam's", "answer", "amazed"]
        assert result["s"] == ["asked", "Adam's", "answer"]
        assert result["k"] == ["asked"]
        assert result["d"] == ["asked", "Adam", "add", "Adam's", "amazed"]
        assert result["A"] == ["Alice", "Adam", "Adam's", "Alice!"]
        assert result["m"] == ["Adam", "Adam's", "amazed"]
        assert result["t"] == ["to", "anti-aging", "agent;"]
        assert result["o"] == ["to"]
        assert result["n"] == ["an", "anti-aging", "agent;", "answer"]
        assert result["g"] == ["anti-aging", "agent;"]
        assert result[";"] == ["agent;"]
        assert result["-"] == ["anti-aging"] 
        assert result["'"] == ["Adam's"]           
        assert result["!"] == ["Alice!"] 
        assert result[" "] == []
        
        test_str = ""
        result = make_alpha_dict(test_str)
        
        
    def test_flatten(self):
        result = flatten([1, [2, 3], [[4, 5], 6]])
        self.assertEqual(result, [1, 2, 3, 4, 5, 6])
        
        result = flatten([1, [2, [3, [4, 5]]]])
        self.assertEqual(result, [1, 2, 3, 4, 5])
        
        result = flatten([1, 2, 3])
        self.assertEqual(result, [1, 2, 3])
        
        result = flatten([[[[1]]]])
        self.assertEqual(result, [1])
        
        result = flatten([])
        self.assertEqual(result, [])
        
        result = flatten([1, [], 2, [3, []], 4])
        self.assertEqual(result, [1, 2, 3, 4])
        
        result = flatten([[[[1]]]])
        self.assertEqual(result, [1])

    
if __name__ == "__main__":
    unittest.main()
    