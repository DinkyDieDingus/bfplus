import os

class Debugger:
    def __init__(self, instructions, debug_info, show_line_nums=True, clearMode=True, data_window_size=10, instr_window_size=10, show_instr_per_line=4):
        self.instructions = instructions
        self.info = debug_info
        self.clearMode = clearMode
        self.prev_instr = ''
        self.breakpoints = [0]
        self.data_window_size = data_window_size
        self.instr_window_size = instr_window_size
        self.show_instr_per_line = show_instr_per_line
        self.show_line_nums = show_line_nums

    def run(self, ptr, data, i):
        if i not in self.breakpoints:
            return
        else:
            self.breakpoints.pop(self.breakpoints.index(i))
        if self.clearMode:
            #pass
            os.system('clear')
        d_snip_start = max(0, ptr - self.data_window_size)
        d_snip_end = min(len(data), ptr + self.data_window_size)
        d_snip = data[d_snip_start : d_snip_end + 1]
        print(str(d_snip))
        if (ptr == 0):
            print(' ^')
        else:
            print(' '*(len(str(data[d_snip_start : ptr]))+1) + '^')

        i_snip_start = max(0, i - self.instr_window_size)
        i_snip_end = min(len(self.instructions), i_snip_start + (2 * self.instr_window_size))
        i_snip = self.instructions[i_snip_start : i_snip_end + 1]
        
        for idx, instr in enumerate(i_snip):
            num = idx + i_snip_start
            cur = ' '
            if num == i:
                cur = '>'
            line_str = ''
            if self.show_line_nums:
                line_str = f'line {self.info[num][0]}, col {self.info[num][1]}'
            print(f'{num:<4} {cur} ({instr})    {line_str}')
        
        debug_inst = ''    
        while not (debug_inst == 'n' or debug_inst == 'c'):    
            debug_inst = input('>')
            if debug_inst == '':
                debug_inst = self.prev_instr
            while not (debug_inst != '' and debug_inst[0] in ['n', 's', 'q', 'c', 'b']):
                print('Invalid debugger command')
                debug_inst = input('>')
            split = debug_inst.split(' ')
            cmd = split[0]
            args = split[1:]
            if cmd == 'n':
                self.breakpoints.append(i + 1)
            elif cmd == 's':
                start = 0
                if len(args) >= 1:
                    start = int(args[0])
                end = len(self.instructions)
                if len(args) >= 2:
                    end = min(len(self.instructions), int(args[1]))
                for idx, instr in enumerate(self.instructions[start:end]):
                    if idx % self.show_instr_per_line == 0:
                        print(f'{idx + start:<4} ', end='')
                    print(f'({instr}) ', end='')
                    if idx % self.show_instr_per_line == self.show_instr_per_line - 1:
                        print()
                print()
            elif cmd == 'q':
                confirm = input('Are you sure you want to quit? (Y/n) ')
                if confirm == 'y' or confirm == '':
                    exit()
                else:
                    print('Quit aborted')
            elif cmd == 'b':
                self.breakpointCmd(args)
            self.prev_instr = debug_inst


    def breakpointCmd(self, args):
        if len(args) < 1:
            print('Please specify breakpoint location')
        else:
            if ',' in args[0]:
                line, col = args[0].split(',')
                brkpntIdx = -1               
                for idx, info in enumerate(self.info):
                    if int(line) == info[0] and int(col) == info[1]:
                        brkpntIdx = idx
                        break
                if brkpntIdx == -1:
                    print('Invalid line and column')
                    return
                else:
                    brkpnt = brkpntIdx
            else:
                brkpnt = int(args[0])
            self.breakpoints.append(brkpnt)
