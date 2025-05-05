from typing import Iterable, List, Dict
from itertools import chain, accumulate, repeat

def acronym(string_list: Iterable[str]) -> str:
    return "".join(map(lambda element: element[0].upper(), string_list))


def median(int_list: Iterable[int]) -> int:
    if not int_list:
        return None
    sl = sorted(int_list)
    ln = len(int_list)
    return sl[ln // 2] if ln % 2 else (sl[ln // 2 - 1] + sl[ln // 2]) / 2


def pierwiastek(x, epsilon) -> float:
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
    

def make_alpha_dict(input_str: str) -> Dict[str, List[str]]:
    return {
        char_key: list(filter(lambda word: char_key in word, input_str.split()))
        for char_key in set(input_str)
    }
    
def flatten(input_list: List) -> List:
    return list(
        chain.from_iterable(
            map(lambda element: flatten(element) if isinstance(element, (list, tuple)) else [element], input_list)
        )
    )
    
    