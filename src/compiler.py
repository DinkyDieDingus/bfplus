import os
from src.executor import Executor

class CCompiler(Executor):
    def __init__(self, instructions, filename, compile_bin, binname):
        super().__init__(instructions)
        self.filename = filename
        self.file = open(filename, 'w')
        self.file.write('#include<stdio.h>\nint main(){\n    char array[30000] = {0};\n    char *ptr = array;\n')
        self.indent = 1
        self.compile = compile_bin
        self.binname = binname
    
    def _condense_repeats(self, i, instr, single_expr, multi_expr):
        count = 1
        while self.instructions[i + count] == instr:
            count += 1
        i += count - 1
        if count == 1:
            self.file.write(self.indent*'    ' + single_expr  + ';\n')
        else:
            self.file.write(self.indent*'    ' + multi_expr + str(count) + ';\n')
        return i

    def finish(self):
        self.file.write('    return 0;\n}\n')
        self.file.close()

        if self.compile:
            os.system(f'gcc {self.filename} -o {self.binname}')

    def incPtr(self, i):
        return self._condense_repeats(i, '>', '++ptr', 'ptr += ');

    def decPtr(self, i):
        return self._condense_repeats(i, '<', '--ptr', 'ptr -= ');

    def inc(self, i):
        return self._condense_repeats(i, '+', '++*ptr', '*ptr += ');

    def dec(self, i):
        return self._condense_repeats(i, '-', '--*ptr', '*ptr -= ');

    def print(self, i):
        self.file.write(self.indent*'    ' + 'putchar(*ptr);\n')
        return i

    def input(self, i):
        self.file.write(self.indent*'    ' + '*ptr = getchar();\n')
        return i

    def loopStart(self, i):
        self.file.write(self.indent*'    ' + 'while (*ptr) {\n')
        self.indent += 1
        return i

    def loopEnd(self, i):
        self.indent -= 1
        self.file.write(self.indent*'    ' + '}\n')
        return i


class AsmCompiler(Executor):
    def __init__(self, instructions, filename, compile_bin, binname):
        super().__init__(instructions)
        self.filename = filename
        self.file = open(filename, 'w')
        self.pad = '    '
        self.file.write('global _start\n\nsection .text\n_start:\n' + self.pad + "mov byte [rsp], 0x0\n")
        self.stack = []
        self.compile = compile_bin
        self.binname = binname

    def finish(self):
        self.file.write(self.pad + 'mov rax, 0x3c\n')
        self.file.write(self.pad + 'mov rdi, 0x1\n')
        self.file.write(self.pad + 'syscall\n')
        self.file.close()

        if self.compile:
            strn = f'nasm -f elf64 {self.filename} && ld ./{self.filename[:-4]}.o -o {self.binname}'
            os.system(strn)

    def incPtr(self, i):
        self.file.write(self.pad + 'dec rsp\n')
        return i

    def decPtr(self, i):
        self.file.write(self.pad + 'inc rsp\n')
        return i

    def inc(self, i):
        self.file.write(self.pad + 'inc byte [rsp]\n')
        return i

    def dec(self, i):
        self.file.write(self.pad + 'dec byte [rsp]\n')
        return i

    def print(self, i):
        self.file.write(self.pad + 'mov rax, 0x1\n')
        self.file.write(self.pad + 'mov rdi, 0x1\n')
        self.file.write(self.pad + 'mov rsi, rsp\n')
        self.file.write(self.pad + 'mov rdx, 0x1\n')
        self.file.write(self.pad + 'syscall\n')
        return i

    def input(self, i):
        self.file.write(self.pad + 'mov rax, 0x0\n')
        self.file.write(self.pad + 'mov rdi, 0x0\n')
        self.file.write(self.pad + 'mov rsi, rsp\n')
        self.file.write(self.pad + 'mov rdx, 0x1\n')
        self.file.write(self.pad + 'syscall\n')
        return i

    def loopStart(self, i):
        if len(self.stack) == 0:
            nxt = 'a'
        else:
            prev = self.stack[-1]
            lastchar = prev[-1]
            if lastchar == 'z':
                nxt = prev + 'a'
            else:
                nxt = prev[:-1] + chr(ord(lastchar) + 1)
        
        self.stack.append(nxt)
        self.file.write(self.pad + 'cmp byte [rsp], 0x0\n')
        self.file.write(self.pad + f'je {nxt}_end\n')
        self.file.write(nxt + ':\n')
        return i

    def loopEnd(self, i):
        prev = self.stack[-1]
        self.file.write(self.pad + 'cmp BYTE [rsp], 0x0\n')
        self.file.write(self.pad + f'jne {prev}\n')
        self.file.write(prev + '_end:\n')
        return i
