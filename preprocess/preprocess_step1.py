#!/usr/bin/env python3

import os
import re
from tqdm import tqdm
import glob


files = glob.glob("tornado/**/*.py", recursive=True)
changed = []
unchanged = []
print("{} files in path".format(len(files)))

print("PART 1 - REMOVE DOCSTRINGS AND COMMENTS")
for i, f in tqdm(enumerate(files)):
    opened_file = open(f, "r")
    data = opened_file.read()
    opened_file.close()
    orig_len = len(data)
    data = re.sub(r"'''[\w\W]*?'''", "''''''", data)
    data = re.sub(r"(\t''''''|    ''''''|'''''')", "", data)
    data = re.sub(r'"""[\w\W]*?"""', '""""""', data)
    data = re.sub(r'(\t""""""|    """""")', '', data)
    data = re.sub(r'""""""', '', data)
    data = re.sub(r'( |\n|\t)+# .*\n', '\n', data)  # inline comments
    data = re.sub(r' +#\n', '\n', data)  # empty inline comments
    data = re.sub(r'(?m)^ *#.*\n?', '\n', data)  # full line comments
    data = re.sub(r'\n\n+', '\n\n', data)  # multiple newlines

    if len(data) != orig_len:
        changed.append(f)
    else:
        unchanged.append(f)
    opened_file = open(f, "w+")
    opened_file.write(data)
    opened_file.close()

print("{} files changed".format(len(changed)))

ch = open("changed.txt", "w+")
for c in changed:
    ch.write(c)
    ch.write("\n")

print("{} files unchanged".format(len(unchanged)))
un = open("unchanged.txt", "w+")
for u in unchanged:
    un.write(u)
    un.write("\n")


print("PART 2 - TEST IF FILES CAN BE COMPILED")

codes = []
out = open('error_files.txt', "w+")  # change to errors_2 or errors_3

for i, f in tqdm(enumerate(files)):
    # change to python3 or python for different version compilation
    cmd = 'python3 -m py_compile ' + f

    code = os.system(cmd)
    if code is not 0:
        codes.append(code)
        out.write(f)
        out.write("\n")
print(len(codes))
out.close()

print("files that need to be fixed manually can be found in error_files.txt")
print("once the errors are fixed, you can run prepare_function.py")
