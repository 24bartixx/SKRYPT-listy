from tasks.zad4 import make_generator
from functools import cache

import textwrap
import inspect
import ast


def _make_self_recursive(func):
    # inspect.getsource() - get source code of the function
    # dedent - remove leading whitespaces from every line  (necessary for ast.parse())
    source_code = textwrap.dedent(inspect.getsource(func))
    
    # create abstract syntax tree (AST)(AST is structure that describes syntax of the function)
    tree = ast.parse(source_code)

    func_name = func.__name__
        
    class RewriteRecursiveCall(ast.NodeTransformer):
        def visit_Call(self, node):
            # call visit() on all node's children
            # necessarry for nested recusrive calls like factorial(factorial(...))
            self.generic_visit(node)
            # if function call has the same name
            # ast.Name is name of the variable
            if isinstance(node.func, ast.Name) and node.func.id == func_name:
                # return Call with different name, idk what's Load() though but it's necessary
                return ast.Call(
                    func=ast.Name(id='self', ctx=ast.Load()), 
                    args=node.args, 
                    keywords=node.keywords
                )
            return node

    # Get transformed tree
    tree = RewriteRecursiveCall().visit(tree)
    # used to recalculate location information of new nodes during complication (lineno, col_offset)
    ast.fix_missing_locations(tree)

    # ast.FunctionDef - full description, name, arguments, body
    function_definition = tree.body[0]
    function_definition.args.args.insert(0,
        ast.arg(
            arg='self',
            lineno=function_definition.lineno,              # line number
            col_offset=function_definition.col_offset       # sign offset
        )
    )

    # represantation of the code in the tree
    code = compile(
        ast.Module(body=[function_definition], type_ignores=[]),
        filename="<ast>", 
        mode="exec"
    )

    # dict for functions, include func to exist somewhere
    scope = {}
    exec(code, func.__globals__, scope)

    return scope[func.__name__]


def make_generator_mem(function):
    self_recursive_function = _make_self_recursive(function)
    # @lru_cache(maxsize=None)
    @cache
    def new_function(n):
        return self_recursive_function(new_function, n)
    return make_generator(new_function)
