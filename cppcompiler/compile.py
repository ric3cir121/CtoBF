import cppcompiler.tokenizer as tokenizer
import cppcompiler.process as process
import cppcompiler.transform as transform
import cppcompiler.inout as inout
from cppcompiler.objs import *

def solve(main: str):
    cppcode = inout.read_from_file(main)
    token_map = Tokens([Unparsed("#include \"bfcomp\"\n"),Unparsed(cppcode)],main)
    token_map.patch()
    tokenizer.solve(token_map)
    code_map = process.solve(token_map)
    semicode = transform.solve(code_map)
    return semicode