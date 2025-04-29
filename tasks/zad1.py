from typing import Iterable, List, Dict
from itertools import chain

def acronym(string_list: Iterable[str]) -> str:
    return "".join(map(lambda element: element[0].upper(), string_list))


def median(int_list: Iterable[int]) -> int:
    sl = sorted(int_list)
    ln = len(int_list)
    return sl[ln // 2] if ln % 2 else (sl[ln // 2] + sl[ln // 2 + 1] / 2)


def pierwiastek(x, epsilon) -> float:
    ...
    

def make_alpha_dict(input_str: str) -> Dict[str, List[str]]:
    return {
        char_key: filter
        for char_key in set(input_str)
    }

    
    
    ...
    
def flatten(input_list: List) -> List:
    return list(
        chain.from_iterable(
            map(lambda element: flatten(element) if isinstance(element, (list, tuple)) else [element], input_list)
        )
    )
    
    