import os

def read_from_file(path: str) -> str:
    f = open(path,"r")
    content = f.read()
    f.close()
    return content

def write_to_file(path: str,content: str) -> None:
    f = open(path,"w")
    f.write(content)
    f.close()

def is_file(path):
    return os.path.isfile(path)

def is_dir(path):
    return os.path.isdir(path)

def make_dir(path):
    return os.mkdir(path)