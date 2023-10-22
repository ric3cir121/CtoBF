import cppcompiler.precompile as precompile
from cppcompiler.objs import *

# Variables

# operators must be sorted by increasing length of tokens
operators = [
    # length of 1
    ",",".","+","-","*","/","%","&","|","^","!","=",">","<",":",
    # length of 2
    "++","+=","-=","--","->","*=","/=","%=","&=","&&","|=","||","^=","!=","==",">=",">>","<=","<<","::",
    # length of 3
    "<=>",">>=","<<="
]

empties = [" ","\n"]
brackets = ["(",")","[","]","{","}"]
action_split = ";"

builtin_value_types = {
    "void":"__builtin_bf_void",
    "signed char":"__builtin_bf_signed_char",
    "unsigned char":"__builtin_bf_unsigned_char",
    "char":"__builtin_bf_char",
    "char8_t":"__builtin_bf_char8_t",
    "signed short int":"__builtin_bf_signed_short_int",
    "unsigned short int":"__builtin_bf_unsigned_short_int",
    "char16_t":"__builtin_bf_char16_t",
    "signed int":"__builtin_bf_signed_int",
    "unsigned int":"__builtin_bf_unsigned_int",
    "char32_t":"__builtin_bf_char32_t",
    "wchar_t":"__builtin_bf_wchar_t",
    "signed long int":"__builtin_bf_signed_long_int",
    "unsigned long int":"__builtin_bf_unsigned_long_int",
    "signed long long int":"__builtin_bf_signed_long_long_int",
    "unsigned long long int":"__builtin_bf_unsigned_long_long_int",
    "bool":"__builtin_bf_bool",
    "float":"__builtin_bf_float",
    "double":"__builtin_bf_double",
    "long double":"__builtin_bf_long_double"
}
solve_value_types = {
    "short":"signed short int",
    "short int":"signed short int",
    "signed short":"signed short int",
    "unsigned short":"unsigned short int",
    "int":"signed int",
    "signed":"signed int",
    "unsigned":"unsigned int",
    "long":"signed long int",
    "long int":"signed long int",
    "signed long":"signed long int",
    "unsigned long":"unsigned long int",
    "long long":"signed long long int",
    "long long int":"signed long long int",
    "signed long long":"signed long long int",
    "unsigned long long":"unsigned long long int",
}
# value_types must be sorted by increasing number of words
value_types = [
    # 1 word
    "void","char","char8_t","short","char16_t","int","signed","unsigned","char32_t","wchar_t","long","bool",
    "float","double",
    # 2 words
    "signed char","unsigned char","short int","signed short","unsigned short","signed int","unsigned int",
    "long int","signed long","unsigned long","long long","long double",
    # 3 words
    "signed short int","unsigned short int","signed long int","unsigned long int","long long int",
    "signed long long","unsigned long long",
    # 4 words
    "signed long long int","unsigned long long int"
]

# Utils Functions

def split_str(string: list[str]|str,criteria: list[str]|str):
    if isinstance(criteria,list):
        res = string
        for i in criteria:
            res = split_str(res,i)
        return res
    else:
        res = []
        for i in string:
            string_split = i.split(criteria)
            split = []
            for i in range(len(string_split)):
                if i != 0 and criteria != "": split.append(criteria)
                if string_split[i] != "": split.append(string_split[i])
            res += split
        return res

def split_token(string: list[Token],criteria: list[str]|str,replace: list[Token]|Token):
    if isinstance(criteria,list) and isinstance(replace,list):
        res = string
        for i in range(len(criteria)):
            res = split_token(res,criteria[i],replace[i])
        return res
    elif not (isinstance(criteria,list) or isinstance(replace,list)):
        res = []
        for i in string:
            if isinstance(i,Unparsed):
                string_split = i.string.split(criteria)
                for j in range(len(string_split)):
                    string_split[j] = Unparsed(string_split[j])

                split = []
                for i in range(len(string_split)):
                    if i != 0 and replace != "": split.append(replace)
                    if string_split[i].string != "": split.append(string_split[i])
                
                res += split
            else:
                res.append(i)
        return res
    else:
        # TODO: proper internal error message
        raise Exception("Error: Internal error: split_token() provived with invalid arguments")

# Functions

def uncomment(token_map: Tokens):
    tokens = token_map.tokens
    res = []
    is_long_comment,is_short_comment = False,False
    for token in tokens:
        if isinstance(token,Unparsed):
            string = token.string
            split = split_str([string],["/*","*/","//","\n"])
            read = ""
            for i in split:
                if is_short_comment:
                    if i == "\n":
                        is_short_comment = False
                        res.append(Unparsed(read))
                        res.append(Divider())
                        read = ""
                elif is_long_comment:
                    if i == "*/":
                        is_long_comment = False
                        res.append(Unparsed(read))
                        res.append(Divider())
                        read = ""
                else:
                    if i == "//": is_short_comment = True
                    elif i == "/*": is_long_comment = True
                    else:
                        read += i
            if read != "":
                res.append(Unparsed(read))
    token_map.tokens = res
    token_map.patch()

def unstring(token_map: Tokens):
    tokens = token_map.tokens
    res = []
    for token in tokens:
        if isinstance(token,Unparsed):
            string = token.string
            in_string,in_single_escape,is_include_str = False,False,False
            delimiters = "\"'"
            delimiter,escape = "",""
            read = ""
            for char in string:
                if not in_string:
                    if char in delimiters:
                        in_string = True
                        delimiter = char
                        is_include_str = read.rstrip(" ").split("\n")[-1] == "#include"
                        res.append(Unparsed(read))
                        read = ""
                    else:
                        read += char
                else:
                    # TODO: missing all escaping rules for a string
                    if char == delimiter and not in_single_escape:
                        in_string = False
                        res.append(String(read,delimiter))
                        read = ""
                    else:
                        if char in "\\\n" and is_include_str:
                            # TODO: proper error message
                            raise Exception("Error: Include errors detected")
                        if not in_single_escape:
                            if char == "\\":
                                in_single_escape = True
                        else:
                            in_single_escape = False
                        read += char

            if not in_string:
                res.append(Unparsed(read))
                read = ""
            else:
                # TODO: proper error message
                raise Exception("Error: String reached end of file")
    token_map.tokens = res
    token_map.patch()

def tokenize(token_map: Tokens):
    # split different tokens
    tokens = token_map.tokens
    res = []
    for token in tokens:
        # TODO: join together unparsed only if they match position
        # position means that only two originally adjacent pieces
        # can be joined, such as in "unsigned long", we split it
        # into Unparsed("unsigned")+Divider(" ")+Unparsed("long")
        # and can then be joined back into Name("unsigned long").
        # 
        # We may have the same exact syntax but with the "unsigned"
        # coming from a different file in an include, in such case
        # it wont be compatible and the string will be kept separated
        if isinstance(token,Unparsed):
            split: list[Token] = [token]
            for operator in operators[::-1]:
                split = split_token(split,operator,Operator(operator))

            for bracket in brackets:
                split = split_token(split,bracket,Bracket(bracket))

            split = split_token(split,action_split,Split(action_split))

            for operator in empties:
                split = split_token(split,operator,Divider())
                
            res += split
        elif isinstance(token,String):
            res.append(token)
    token_map.tokens = res
    token_map.patch()

    # connect tokens made of multiple words

    tokens = token_map.tokens
    i = 0
    while i != len(tokens):
        # TODO: join together unparsed only if they match position
        # position means that only two originally adjacent pieces
        # can be joined, such as in "unsigned long", we split it
        # into Unparsed("unsigned")+Divider(" ")+Unparsed("long")
        # and can then be joined back into Name("unsigned long").
        # 
        # We may have the same exact syntax but with the "unsigned"
        # coming from a different file in an include, in such case
        # it wont be compatible and the string will be kept separated
        if len(tokens)-i >= 7:
            if (isinstance(tokens[i  ],Unparsed) and isinstance(tokens[i+1],Divider) and isinstance(tokens[i+2],Unparsed) and isinstance(tokens[i+3],Divider) and 
                isinstance(tokens[i+4],Unparsed) and isinstance(tokens[i+5],Divider) and isinstance(tokens[i+6],Unparsed)):
                for j in value_types:
                    key_words = j.split(" ")
                    if len(key_words) == 4:
                        if tokens[i].string == key_words[0] and tokens[i+2].string == key_words[1] and tokens[i+4].string == key_words[2] and tokens[i+6].string == key_words[3]:
                            tokens[i] = Name(j)
                            del tokens[i+1:i+7]
                            break
        if len(tokens)-i >= 5:
            if (isinstance(tokens[i  ],Unparsed) and isinstance(tokens[i+1],Divider) and isinstance(tokens[i+2],Unparsed) and isinstance(tokens[i+3],Divider) and 
                isinstance(tokens[i+4],Unparsed)):
                for j in value_types:
                    key_words = j.split(" ")
                    if len(key_words) == 3:
                        if tokens[i].string == key_words[0] and tokens[i+2].string == key_words[1] and tokens[i+4].string == key_words[2]:
                            tokens[i] = Name(j)
                            del tokens[i+1:i+5]
                            break
        if len(tokens)-i >= 3:
            if (isinstance(tokens[i],Unparsed) and isinstance(tokens[i+1],Divider) and isinstance(tokens[i+2],Unparsed)):
                for j in value_types:
                    key_words = j.split(" ")
                    if len(key_words) == 2:
                        if tokens[i].string == key_words[0] and tokens[i+2].string == key_words[1]:
                            tokens[i] = Name(j)
                            del tokens[i+1:i+3]
                            break
        i += 1
    
    for i in range(len(tokens)):
        if isinstance(tokens[i],Unparsed):
            tokens[i] = Name(tokens[i])

    token_map.tokens = tokens
    token_map.patch()

# Main functions

def purify(token_map: Tokens):
    # Function purify does unstringing and uncommenting
    # It will divide strings from the rest of the code
    # and will remove comments from it
    uncomment(token_map)
    unstring(token_map)

def solve(token_map: Tokens):
    purify(token_map)
    precompile.solve(token_map)
    tokenize(token_map)
    print()
    print(token_map)