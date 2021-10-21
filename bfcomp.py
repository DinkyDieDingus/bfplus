#!/usr/bin/env python3
import argparse
from compiler import CCompiler, AsmCompiler
import processor

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Compile bf source code into c code')
    parser.add_argument('bfname')
    parser.add_argument('-l', help='Language to compile to', dest='language', default='c', choices=['c', 'asm'])
    parser.add_argument('-o', help='Name of compiled file', dest='cname', default=None)
    parser.add_argument('-c', help='Whether to use external compiler to compile to binary file', dest='compile', action='store_true')

    args = parser.parse_args()

    instructions, debug_info = processor.load(args.bfname, False)

    cname = args.cname
    if cname == None:
        rawname = args.bfname.split('/')[-1]
        if rawname.endswith('.bf'):
            rawname = rawname[:-3]
        cname = rawname + '.' + args.language
    
    if args.language == 'c':
        executor = CCompiler(instructions, cname, args.compile, 'a.out')
    else:
        executor = AsmCompiler(instructions, cname, args.compile, 'a.out') 
 
    processor.process(instructions, executor)