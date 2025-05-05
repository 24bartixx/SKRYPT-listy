def forall(pred, iterable):
    for element in iterable:
        if not pred(element):
            return False
    return True

def exists(pred, iterable):
    for element in iterable:
        if pred(element):
            return True
    return False

def _get_good_count(pred, iterable):
    good = 0
    for element in iterable:
        if pred(element):
            good += 1
    return good

def atleast(n, pred, iterable):
    return _get_good_count(pred, iterable) >= n

def atmost(n, pred, iterable):
    return _get_good_count(pred, iterable) <= n