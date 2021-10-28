import os
from src.executor import Executor

class BinCompiler(Executor):
    def __init__(self, instructions, binname):
        super().__init__(instructions)
        self.binname = binname

        self.loopStarts = []
        self.text = bytearray(b'\xc6\x04\x24\x00')

    def finish(self):
        self.text += b'\xb8\x3c\x00\x00\x00' # mov    $0x3c,%eax
        self.text += b'\xbf\x01\x00\x00\x00' # mov    $0x1,%edi
        self.text += b'\x0f\x05'             # syscall

        file = open(self.binname, 'wb')

        file.write(get_elf_header(len(self.text))) 
        file.write(self.text)
        
        file.close()
        os.system('chmod +x ' + self.binname)

    def incPtr(self, i):
        self.text += b'\x48\xff\xcc'
        return i

    def decPtr(self, i):
        self.text += b'\x48\xff\xc4'
        return i

    def inc(self, i):
        self.text += b'\xfe\x04\x24'
        return i

    def dec(self, i):
        self.text += b'\xfe\x0c\x24'
        return i

    def print(self, i):
        self.text += b'\xb8\x01\x00\x00\x00'
        self.text += b'\xbf\x01\x00\x00\x00'
        self.text += b'\x48\x89\xe6'
        self.text += b'\xba\x01\x00\x00\x00'
        self.text += b'\x0f\x05'
        return i

    def input(self, i): 
        self.text += b'\xb8\x00\x00\x00\x00'
        self.text += b'\xbf\x00\x00\x00\x00'
        self.text += b'\x48\x89\xe6'
        self.text += b'\xba\x01\x00\x00\x00'
        self.text += b'\x0f\x05'
        return i

    def loopStart(self, i):
        
        # check ptr is 0
        self.text += b'\x80\x3c\x24\x00'
        # jump to end of loop if so
        self.text += b'\x74\x00' # leave 0x00 at end to fill in later
        # bookmark beginning
        self.loopStarts.append(len(self.text))

        return i

    def loopEnd(self, i):
        
        # check ptr is 0
        self.text += b'\x80\x3c\x24\x00'

        # get the beginning of the loop
        start = self.loopStarts.pop()
        print(f'start = {hex(start)}')
        # get the number of instructions previous it was
        start_rel_pos = len(self.text) - start + 2
        print(f'diff  = {start_rel_pos}')
        print(f'dihex = {hex(start_rel_pos)}')
        # convert that number into negative signed 8-bit hex
        start_rel_pos_hex = twos_compliment(start_rel_pos)
        print(f'dineg = {hex(start_rel_pos_hex)}')
        print(f'bytes = {start_rel_pos_hex.to_bytes(1, "big")}')
        # write jne to that address
        self.text += b'\x75' + start_rel_pos_hex.to_bytes(1, 'big')
        
        end = len(self.text) 
        print(f'end   = {hex(end)}\n')
        self.text[start - 1] = end - start

        return i


def twos_compliment(num):
    print(bin(num)[2:].rjust(8,'0'))
    comp = num ^ 0b11111111
    print(bin(comp)[2:].rjust(8,'0'))
    res = comp + 1
    print(bin(res)[2:].rjust(8,'0'))
    return res

def get_elf_header(text_size):
    # ELF Header
    hdr = b'\x7fELF' # ELF magic number
    hdr += b'\x02' # 64 bit
    hdr += b'\x01' # little endian
    hdr += b'\x01' # ELF ver. 1
    hdr += b'\x00'*2 # ABI no.
    hdr += b'\x00'*7 # padding
    hdr += b'\x02\x00' # exec file type
    hdr += b'\x3e\x00' # x86-64 architecture
    hdr += b'\x01\x00\x00\x00' # ELF ver. 1
    hdr += dword(get_entry_point()) # entry point address
    hdr += b'\x40' + b'\x00' * 7 # start of program header table
    hdr += b'\x00'*8 # start of section header (none)
    hdr += b'\x00'*4 # flags (none)
    hdr += b'\x40\x00' # size of header
    hdr += b'\x38\x00' # size of program header
    hdr += b'\x01\x00' # number of sections
    hdr += b'\x00\x00' # size of section header (none)
    hdr += b'\x00\x00' # number of entries in section header
    hdr += b'\x00\x00' # index of section header that has section names

    # program header (text segment)
    hdr += b'\x01\x00\x00\x00' # loadable segment
    hdr += b'\x05\x00\x00\x00' # flags (0x05 is 00000101 (x-r permissions))
    hdr += b'\x00' * 8 # offset
    hdr += (b'\x00'*4 + b'\x00\x40\x00\x00')[::-1] # virtual address
    hdr += (b'\x00'*4 + b'\x00\x40\x00\x00')[::-1] # physical address (fake)
    hdr += dword(text_size) # size in bytes of file image
    hdr += dword(text_size)# size in bytes of memory image
    hdr += (b'\x00'*4 + b'\x00\x00\x10\x00')[::-1] # alignment

    return hdr

def dword(num):
    return num.to_bytes(8, 'little')

def get_entry_point():
    # vmem address 0x400000 + size of elf header + size of program header
    return 0x400000 + 0x40 + 0x38