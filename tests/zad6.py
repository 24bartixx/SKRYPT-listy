from itertools import accumulate, repeat
from tasks.zad6 import log

@log()
def _pierwiastek1(x, epsilon) -> float:
    if x < 0:
        raise ValueError("The aguement must be non-negative!")
    if x == 0:
        return 0.0
    
    return next(filter(
        lambda value: abs(x - value**2) < epsilon, 
        accumulate(
            iterable = repeat(None), 
            func = lambda y, _: (y+x/y)/2, 
            initial = x // 2 if x > 1 else 1
        ) 
    ))
    
@log(debug_level = "info")
def _pierwiastek2(x, epsilon) -> float:
    if x < 0:
        raise ValueError("The aguement must be non-negative!")
    if x == 0:
        return 0.0
    
    return next(filter(
        lambda value: abs(x - value**2) < epsilon, 
        accumulate(
            iterable = repeat(None), 
            func = lambda y, _: (y+x/y)/2, 
            initial = x // 2 if x > 1 else 1
        ) 
    ))

@log(debug_level = "warn")
class _Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

def test_zad_6():
    
    _pierwiastek1(124284013981984321089481284239518, 0.00000000000000000000000000001)
    _pierwiastek2(124284013981984321089481284239518, 0.00000000000000000000000000001)
    
    _Person("Jan", "Nowak")
        
    try:
        log()(100)
    except TypeError:
        print("TypeError for invalid argument! Good!")

if __name__ == "__main__":
    test_zad_6()
    