#!/usr/bin/env python3
import argparse
from src.compiler.bin import BinCompiler
from src.compiler.c import CCompiler
from src.compiler.asm import AsmCompiler
import src.processor as processor

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Compile bf source code into c code')
    parser.add_argument('bfname')
    parser.add_argument('-l', help='Language to compile to', dest='language', default='c', choices=['c', 'asm', 'bin'])
    parser.add_argument('-o', help='Name of compiled file', dest='cname', default=None)
    parser.add_argument('-c', help='Whether to use external compiler to compile to binary file', dest='binname', nargs='?', default=False)
    parser.add_argument('-d', help='Print compiler debugging information', dest='internal_debug', action='store_true')

    args = parser.parse_args()

    instructions, debug_info = processor.load(args.bfname, False)

    cname = args.cname
    if cname == None:
        rawname = args.bfname.split('/')[-1]
        if rawname.endswith('.bf'):
            rawname = rawname[:-3]
        cname = rawname + '.' + args.language

    binname = args.binname
    compile = binname != False
    if binname == None or binname == False:
        binname = 'a.out'
    
    if args.language == 'c':
        executor = CCompiler(instructions, cname, compile, binname)
    elif args.language == 'asm':
        executor = AsmCompiler(instructions, cname, compile, binname) 
    elif args.language == 'bin':
        executor = BinCompiler(instructions, binname, args.internal_debug)
 
    processor.process(instructions, executor)