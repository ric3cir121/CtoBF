import cppcompiler.includes as includes

def solve(tokens):
    # We give priority to includes as we want to obtain the full
    # sheet of code before running any other pre compilation step
    # as they may not run in order then
    tokens = includes.solve(tokens)

    # TODO: pre compilation operations

    return tokens