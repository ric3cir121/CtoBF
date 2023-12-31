from cppcompiler.objs import *

# Variables

reserved_keywords = [
    "bool","char","char8_t","char16_t","char32_t","double","float","int","long","short","signed","unsigned","void","wchar_t",

    "alignas","alignof","and","and_eq","asm","atomic_cancel","atomic_commit","atomic_noexcept","auto","bitand","bitor","break","case","catch",
    "class","compl","concept","const","consteval","constexpr","constinit","const_cast","continue","co_await","co_return","co_yield","decltype",
    "default","delete","do","dynamic_cast","else","enum","explicit","export","extern","false","for","friend","goto","if","inline","mutable",
    "namespace","new","noexcept","not","not_eq","nullptr","operator","or","or_eq","private","protected","public","reflexpr","register",
    "reinterpret_cast","requires","return","sizeof","static","static_assert","static_cast","struct","switch","synchronized","template","this",
    "thread_local","throw","true","try","typedef","typeid","typename","union","using","virtual","volatile","while","xor","xor_eq"
]

# Utils Functions

# Functions

def direct_compiler(code: Code,token_map: Tokens):
    tokens = token_map.tokens
    i = 0
    read = []
    state = "read"
    brackets = []
    while i != len(tokens):
        if state == "read":
            read.append(tokens)
        i += 1

# Main Functions

def solve(token_map):
    # TODO: Processing code
    code = Code()
    direct_compiler(code,token_map)
    print(code)
    return code