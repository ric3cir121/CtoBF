import cppcompiler.compile as compile

def solve(main):
    # TODO: Full strict type support
    semicode = compile.solve(main)
    return semicode