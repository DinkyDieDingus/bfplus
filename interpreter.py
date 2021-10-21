
from debug import Debugger
import os

class Interpreter:
    def __init__(self, instructions, debug=False, debug_info=None):
        self.data = [0]
        self.ptr = 0
        self.stack = []
        self.debug_info = debug_info
        self.instructions = instructions
        self.debug = debug
        if (self.debug):
            self.debugger = Debugger(self.instructions, self.debug_info)

    def finish(self):
        pass

    def beforeInstr(self, i):
        if self.debug:
            self.debugger.run(self.ptr, self.data, i)

    def afterInstr(self, i):
        while self.ptr >= len(self.data):
            self.data.append(0)

    def incPtr(self, i):
        self.ptr += 1
        return i

    def decPtr(self, i):
        self.ptr -= 1
        return i

    def inc(self, i):
        self.data[self.ptr] += 1
        return i

    def dec(self, i):
        self.data[self.ptr] -= 1
        return i

    def print(self, i):
        if self.debug:
            os.system('clear')
            print('program output:')
        print(chr(self.data[self.ptr]), end='')
        if self.debug:
            input()
        return i

    def input(self, i):
        if self.debug:
            os.system('clear')
            print('program input:')
        self.data[self.ptr] = ord(input()[0])
        return i

    def loopStart(self, i):
        if self.data[self.ptr] == 0:
            while self.instructions[i] != ']':
                i += 1
        else:
            self.stack.append(i)
        return i

    def loopEnd(self, i):
        if self.data[self.ptr] != 0:
            i = self.stack[len(self.stack) - 1]
        else:
            self.stack.pop(len(self.stack) - 1)
        return i
