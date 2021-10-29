
import os
from src.debug import Debugger
from src.executor import Executor

class Interpreter(Executor):
    def __init__(self, instructions, byte_input=False, byte_output=False, debug=False, debug_info=None):
        super().__init__(instructions)
        self.data = [0]
        self.ptr = 0
        self.stack = []
        self.byte_input = byte_input
        self.byte_output = byte_output
        self.debug_info = debug_info
        self.debug = debug
        if (self.debug):
            self.debugger = Debugger(self.instructions, self.debug_info, self.stack)

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
        if not self.byte_output:
            print(chr(self.data[self.ptr]), end='')
        else:
            print(self.data[self.ptr], end='')
        if self.debug:
            input()
        return i

    def input(self, i):
        if self.debug:
            os.system('clear')
            print('program input:')
        if not self.byte_input:
            self.data[self.ptr] = ord(input()[0])
        else:
            self.data[self.ptr] = int(input())
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
            i = self.stack[-1]
        else:
            self.stack.pop()
        return i
