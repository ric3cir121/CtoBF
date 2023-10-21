# Here are stored many of the objects used by the compiler

# Types

# TODO: all types should know where they are located in the
# original code, so that it is easier to find errors

class Unparsed:
    string: str = ""
    def __init__(self,value: str = ""):
        self.string = value

    def __str__(self):
        return f"Unparsed({self.string.__repr__()})"
    def __repr__(self):
        return str(self)
    
class String:
    string: str = ""
    delimiter: str = ""
    def __init__(self,string: str,delimiter: str):
        self.string = string
        self.delimiter = delimiter

    def __str__(self):
        return f"String({self.string.__repr__()})"
    def __repr__(self):
        return str(self)

class Operator:
    operator: str = ""
    def __init__(self,operator: str):
        self.operator = operator

    def __str__(self):
        return f"Operator({self.operator.__repr__()})"
    def __repr__(self):
        return str(self)

class Bracket:
    bracket: str = ""
    def __init__(self,bracket: str):
        self.bracket = bracket

    def __str__(self):
        return f"Bracket({self.bracket.__repr__()})"
    def __repr__(self):
        return str(self)

class Split:
    split: str = ""
    def __init__(self,split: str):
        self.split = split

    def __str__(self):
        return f"Split({self.split.__repr__()})"
    def __repr__(self):
        return str(self)

class Divider:
    def __init__(self):
        pass

    def __str__(self):
        return f"Divider()"
    def __repr__(self):
        return str(self)

class Name:
    name: str = ""
    def __init__(self,name: str|Unparsed):
        if isinstance(name,Unparsed):
            self.name = name.string
        else:
            self.name = name

    def __str__(self):
        return f"Name({self.name.__repr__()})"
    def __repr__(self):
        return str(self)

# Storages for other data

class BuiltIn:
    # TODO: incomplete builtin implementation
    def __init__(self):
        pass

    def __str__(self):
        return f"BuiltIn()"
    def __repr__(self):
        return str(self)
    
class Function:
    # TODO: incomplete function implementation
    def __init__(self):
        pass

    def __str__(self):
        return f"Function()"
    def __repr__(self):
        return str(self)

class Variable:
    # TODO: incomplete variable implementation
    def __init__(self):
        pass

    def __str__(self):
        return f"Variable()"
    def __repr__(self):
        return str(self)

class Default:
    # TODO: incomplete default implementation
    def __init__(self):
        pass

    def __str__(self):
        return f"Default()"
    def __repr__(self):
        return str(self)

# List Storages for other data

class Functions:
    builtins: list[BuiltIn] = []
    functions: list[Function] = []
    def __init__(self):
        pass

    def __str__(self):
        return f"Functions({self.builtins.__repr__()},{self.functions.__repr__()})"
    def __repr__(self):
        return str(self)
    
class Variables:
    variables: list[Variable] = []
    def __init__(self):
        pass

    def __str__(self):
        return f"Variables({self.variables.__repr__()})"
    def __repr__(self):
        return str(self)
    
class Defaults:
    defaults: list[Default] = []
    def __init__(self):
        pass

    def __str__(self):
        return f"Defaults({self.defaults.__repr__()})"
    def __repr__(self):
        return str(self)

# Tokens and Code

Token = Unparsed|String|Operator|Bracket|Split|Divider|Name

class Tokens:
    tokens: list[Token] = []
    dir: str = ""
    main_dir: str = ""

    def patch(self):
        # TODO: patch the content, a Divider should only exist between two Unparsed
        # and there should never be two Unparsed near each other
        i = 0
        while i != len(self.tokens):
            if isinstance(self.tokens[i],Unparsed):
                if i != len(self.tokens)-1:
                    if isinstance(self.tokens[i+1],Unparsed):
                        self.tokens[i].string = self.tokens[i].string + self.tokens[i+1].string
                        del self.tokens[i+1]
                        i -= 1
            elif isinstance(self.tokens[i],Divider):
                if i == 0 or i == len(self.tokens)-1:
                    del self.tokens[i]
                    i -= 1
                else:
                    if not (isinstance(self.tokens[i-1],Unparsed) and isinstance(self.tokens[i+1],Unparsed)):
                        del self.tokens[i]
                        i -= 2
            i += 1
        pass

    def __init__(self,tokens: list[Token] | Token, dir: str ="", main_dir: str =None):
        if isinstance(tokens,list):
            self.tokens = tokens
        else:
            self.tokens = [tokens]
        self.dir = dir
        if main_dir is None:
            self.main_dir = dir
        else:
            self.main_dir = main_dir


    def __str__(self):
        return f"Tokens({self.tokens.__repr__()})"
    def __repr__(self):
        return str(self)
    
class Code:
    tokens: Tokens|None = None
    functions: Functions|None = None
    variables: Variables|None = None
    defaults: Defaults|None = None
    def __init__(self,tokens: Tokens = Tokens([])):
        self.tokens = tokens
        self.functions = Functions()
        self.variables = Variables()
        self.defaults = Defaults()

    def __str__(self):
        return f"Code({self.tokens.__repr__()},{self.functions.__repr__()},{self.variables.__repr__()},{self.defaults.__repr__()})"
    def __repr__(self):
        return str(self)