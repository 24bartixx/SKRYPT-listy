from timeit import timeit
from tasks.zad4 import make_generator
from tasks.zad5 import make_generator_mem
from functools import lru_cache

def test_function(function):
    print(f"\n===== {function.__name__} =====")
    
    generator = make_generator(function)
    time = timeit(lambda: next(generator), number = 32)
    print(f"Time without memoization:\t{time * 1000:.3f} ms")
    
    generator_mem = make_generator_mem(function)
    time_mem = timeit(lambda: next(generator_mem), number = 32)
    print(f"Time with memoization:\t\t{time_mem * 1000:.3f} ms")

def test_zad_5():
    
    def _non_recursive_function(n):
        result = 0
        for i in range(n):
            result += 1
        return result
    
    def _fibonacci(n):
        if n >= 3:
            return _fibonacci(n-1) + _fibonacci(n-2)
        elif n == 2:
            return 1
        return 0
    
    test_function(_non_recursive_function)
    test_function(_fibonacci)
    print()


if __name__ == "__main__":
    test_zad_5()
