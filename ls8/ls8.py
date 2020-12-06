#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

try:
    if len(sys.argv) < 2:
        print(f'Error from {sys.argv[0]}: missing filename argument')
        print(f'Usage: python3 {sys.argv[0]} <somefilename>')
        sys.exit(1)

    with open(sys.argv[1]) as f:
        for line in f:
            split_line = line.split("#")[0]
            stripped_split_line = split_line.strip()

            if stripped_split_line != "":
               command = int(stripped_split_line, 2)

                print(command)

except FileNotFoundError:
    print(f'Your file {sys.argv[1]} was not found by {sys.argv[0]}')

# except Exception:
#     print(f.closed)

# print(sys.argv)


cpu = CPU()

cpu.load()
cpu.run()