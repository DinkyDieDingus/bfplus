#!/usr/bin/env python3

import sys
import re
import os
from bfdebug import Debugger

debug = False

if __name__ == '__main__':

    if len(sys.argv) > 2:
        if sys.argv[2] == 'true':
            debug = True

    data = [0]
    ptr = 0
    stack = []
    debug_info = []
    instructions = []
    with open(sys.argv[1]) as f:
        #instructions = f.read()
        #instructions = re.sub(r'[^\>\<\+\-|.\,\[\]]','',instructions)
        line = 1
        col = 1
        while True:
            char = f.read(1)
            if not char:
                break
            if char in ['>', '<', '+', '-', '.', ',', '[', ']']:
                instructions.append(char)
                if debug:
                    debug_info.append((line, col))
            if debug:
                col += 1
                if char == '\n':
                    line += 1
                    col = 1

    if debug:
        debugger = Debugger(instructions, debug_info)
    
    i = 0
    while i < len(instructions):

        instruction = instructions[i]
        
        if debug:
            debugger.run(ptr, data, i)        

        if instruction == '>':
            ptr += 1
        elif instruction == '<':
            ptr -= 1
        elif instruction == '+':
            data[ptr] += 1
        elif instruction == '-':
            data[ptr] -= 1
        elif instruction == '.':
            if debug:
                os.system('clear')
                print('program output:')
            print(chr(data[ptr]), end='')
            if debug:
                input()
        elif instruction == ',':
            if debug:
                os.system('clear')
                print('program input:')
            data[ptr] = ord(input()[0])
        elif instruction == '[':
            if data[ptr] == 0:
                while instructions[i] != ']':
                    i += 1
            else:
                stack.append(i)
        elif instruction == ']':
            if data[ptr] != 0:
                i = stack[len(stack) - 1]
            else:
                stack.pop(len(stack) - 1)
        while (ptr >= len(data)):
            data.append(0)

        i += 1
