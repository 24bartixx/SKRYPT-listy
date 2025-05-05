import time
from functools import wraps
from types import FunctionType
from tasks.zad6_logger import get_logger
import inspect

logger = get_logger()

def log(debug_level = "debug"):
    log_fun = getattr(logger, debug_level)

    def decorator(param):
        
        if isinstance(param, FunctionType):
            @wraps(param)
            def function_call(*args, **kwargs):
                log_fun(f"Function call - {param.__name__}")
                if args:
                    log_fun(f"Positional args: {args}")
                if kwargs:
                    log_fun(f"Keyword args: {kwargs}")
                start = time.perf_counter()
                result = param(*args, **kwargs)
                end = time.perf_counter()
                log_fun(f"Result: {result}")
                log_fun(f"Execution time: {((end - start) * 1000):.3f} ms")
                return result
            return function_call
        
        elif inspect.isclass(param):
            original_init = param.__init__
            @wraps(param)
            def new_init(self, *args, **kwargs):
                original_init(self, *args, **kwargs)
                log_fun(f"Class {param.__name__} initialized!")
            param.__init__ = new_init
            return param
    
        else: 
            raise TypeError("Decorator can be used only for functions and classes!")
    
    return decorator
