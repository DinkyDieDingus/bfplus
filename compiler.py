import os

class CCompiler:
    def __init__(self, instructions, filename, compile_bin, binname):
        self.instructions = instructions
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

    def beforeInstr(self, i):
        return i

    def afterInstr(self, i):
        return i

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
