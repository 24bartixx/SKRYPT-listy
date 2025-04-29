from tasks.zad1 import *

def test_flatten(input):
    result = flatten(input)

def zad1_tests():
    
    # make_alpha_dict()
    make_alpha_dict("bAjojajo")
    
    # flatten()
    print(flatten([1, 2, 3, 4]))
    print(flatten([[1, 2], [3, 4]]))
    print(flatten([[1, 2], [3, 4, [5, 6, [7, 8]]]]))
    
    
if __name__ == "__main__":
    zad1_tests()    
