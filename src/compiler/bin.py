import os
from src.executor import Executor

class BinCompiler(Executor):
    def __init__(self, instructions, binname):
        super().__init__(instructions)
        self.stack = []
        self.binname = binname

        self.text = b'\xc6\x04\x24\x00'

    def finish(self):
        self.text += b'\xb8\x3c\x00\x00\x00' # mov    $0x3c,%eax
        self.text += b'\xbf\x01\x00\x00\x00' # mov    $0x1,%edi
        self.text += b'\x0f\x05'             # syscall

        file = open(self.binname, 'wb')

        file.write(get_elf_header(len(self.text))) 
        file.write(self.text)
        
        file.close()

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
        self.stack.append(len(self.text))
        """
        self.file.write(self.pad + 'cmp byte [rsp], 0x0\n')
        self.file.write(self.pad + f'je {nxt}_end\n')
        self.file.write(nxt + ':\n')
        """
        return i

    def loopEnd(self, i):
        prev = self.stack[-1]
        """self.file.write(self.pad + 'cmp BYTE [rsp], 0x0\n')
        self.file.write(self.pad + f'jne {prev}\n')
        self.file.write(prev + '_end:\n')"""
        return i


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
    hdr += get_entry_point() # entry point address
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
    hdr += text_size.to_bytes(8, 'little') # size in bytes of file image
    hdr += text_size.to_bytes(8, 'little') # size in bytes of memory image
    hdr += (b'\x00'*4 + b'\x00\x00\x10\x00')[::-1] # alignment

    return hdr

def get_entry_point():
    # vmem address 0x400000 + size of elf header + size of program header
    return (0x400000 + 0x40 + 0x38).to_bytes(8, 'little')