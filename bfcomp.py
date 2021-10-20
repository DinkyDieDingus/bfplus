#!/usr/bin/env python3

import sys
import re
import os
from bfdebug import Debugger

filename = 'a'

def countRepeats(i, instructions, instr):

    count = 1
    while instructions[i + count] == instr:
        count += 1
    return count

if __name__ == '__main__':

    if len(sys.argv) > 2:
        filename = sys.argv[2]

    with open(sys.argv[1]) as f:
        instructions = f.read()
        instructions = re.sub(r'[^\>\<\+\-|.\,\[\]]','',instructions)

    with open(filename + '.c', 'w') as f:

        f.write('#include<stdio.h>\nint main(){\n    char array[30000] = {0};\n    char *ptr = array;\n')
        
        indent = 1

        i = 0
        while i < len(instructions): 
            instruction = instructions[i]

            if instruction == '>':
                count = countRepeats(i, instructions, '>')
                i += count - 1
                if count == 1:
                    f.write(indent*'    ' + '++ptr;\n')
                else:
                    f.write(indent*'    ' + f'ptr += {count};\n')
                
            elif instruction == '<':
                count = countRepeats(i, instructions, '<')
                i += count - 1
                if count == 1:
                    f.write(indent*'    ' + '--ptr;\n')
                else:
                    f.write(indent*'    ' + f'ptr -= {count};\n')
            elif instruction == '+':
                count = countRepeats(i, instructions, '+')
                i += count - 1
                if count == 1:
                    f.write(indent*'    ' + '++*ptr;\n')
                else:
                    f.write(indent*'    ' + f'*ptr += {count};\n')
            elif instruction == '-':
                count = countRepeats(i, instructions, '-')
                i += count - 1
                if count == 1:
                    f.write(indent*'    ' + '--*ptr;\n')
                else:
                    f.write(indent*'    ' + f'*ptr -= {count};\n')
            elif instruction == '.':
                f.write(indent*'    ' + 'putchar(*ptr);\n')
            elif instruction == ',':
                f.write(indent*'    ' + '*ptr = getchar();\n')
            elif instruction == '[':
                f.write(indent*'    ' + 'while (*ptr) {\n')
                indent += 1
            elif instruction == ']':
                indent -= 1
                f.write(indent*'    ' + '}\n')
            
            i += 1
        f.write('    return 0;\n}\n')

    os.system('gcc ' + filename + '.c -o ' + filename + '.out')
