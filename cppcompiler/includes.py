import cppcompiler.io as io
import cppcompiler.tokenizer as tokenizer
from cppcompiler.objs import *

# Functions

def include_files(token_map: Tokens):
    tokens = token_map.tokens
    res = []
    read: list[Token] = []
    for token in tokens:
        if isinstance(token,Unparsed):
            string = token.string
            read.append(Unparsed())
            for char in string:
                if char == "\n":
                    include_check = Tokens(read)
                    include_check.patch()
                    if include_check.tokens[0].string[:8] == "#include":
                        # A File will be included
                        is_valid = True
                        if len(include_check.tokens) == 3:
                            if (include_check.tokens[0].string.rstrip(" ") == "#include" and isinstance(include_check.tokens[1],String) and
                                isinstance(include_check.tokens[2],Unparsed)):
                                if include_check.tokens[2].string.strip(" ") == "":
                                    is_valid = True
                                else: is_valid = False
                            else: is_valid = False
                        else: is_valid = False
                            
                        if not is_valid:
                            # TODO: proper error message
                            raise Exception("Error: Invalid include syntax")
                        
                        path = include_check.tokens[1].string

                        working_path = None

                        if len(path) > 0:
                            if path[0] == "/":
                                if io.is_file(path):
                                    working_path = path
                            else:
                                if "/" in path:
                                    test_path = "/".join(token_map.main_dir.split("/")[:-1])+"/"+path
                                    if io.is_file(test_path):
                                        working_path = test_path
                                    elif io.is_file(path):
                                        working_path = path
                                else:
                                    if io.is_file(path):
                                        working_path = path

                        if working_path == None:
                            # TODO: proper error message
                            raise Exception("Error: Include file not found: "+str(path))

                        cppcode = io.read_from_file(path)
                        sub_token_map = Tokens(Unparsed(cppcode),path)
                        tokenizer.purify(sub_token_map)
                        solve(sub_token_map)

                        res += [Divider()]+sub_token_map.tokens+[Divider()]
                        read = [Unparsed()]
                    else:
                        read[-1].string += char
                        res += read
                        read = [Unparsed()]
                else:
                    read[-1].string += char
        elif isinstance(token,String):
            read.append(token)

    res += read

    token_map.tokens = res
    token_map.patch()

# Main Functions

def solve(token_map):
    include_files(token_map)
    return token_map