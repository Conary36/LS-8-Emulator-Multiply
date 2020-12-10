#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
try:
    if len(sys.argv) < 2:
        print(f'Error from {sys.argv[0]}: missing filename argument')
        print(f'Usage: python3 {sys.argv[0]} <somefilename>')
        sys.exit(1)

    with open(sys.argv[1]) as f:

        cpu.load(sys.argv[1])
        cpu.run()


except FileNotFoundError:
    print(f'Your file {sys.argv[1]} was not found by {sys.argv[0]}')
