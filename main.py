import cppcompiler.main as cppcompiler
import semicompiler.main as semicompiler
import bfcompiler.main as bfcompiler
import sys

def read_from_file(path):
    f = open(path,"r")
    content = f.read()
    f.close()
    return content

def write_to_file(path,content):
    f = open(path,"w")
    f.write(content)
    f.close()

semicode = cppcompiler.solve(str(sys.argv[1]))

write_to_file("generated/code.semi",semicode)

bfcode = semicompiler.solve(semicode)

write_to_file("generated/code.bf",bfcode)

compiledcode = bfcompiler.solve(bfcode)

write_to_file("generated/code.c++",compiledcode)