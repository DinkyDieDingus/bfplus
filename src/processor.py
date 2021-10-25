
def load(filename, debug):
    instructions = []
    debug_info = []
    with open(filename) as f:
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
    return (instructions, debug_info)

def process(instructions, executor):
    i = 0
    while i < len(instructions):

        instruction = instructions[i]
        
        executor.beforeInstr(i)

        if instruction == '>':
            i = executor.incPtr(i)
        elif instruction == '<':
            i = executor.decPtr(i)
        elif instruction == '+':
            i = executor.inc(i)
        elif instruction == '-':
            i = executor.dec(i)
        elif instruction == '.':
            i = executor.print(i)
        elif instruction == ',':
            i = executor.input(i)
        elif instruction == '[':
            i = executor.loopStart(i)
        elif instruction == ']':
            i = executor.loopEnd(i)

        executor.afterInstr(i)

        i += 1
    executor.finish()