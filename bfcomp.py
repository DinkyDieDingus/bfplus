#!/usr/bin/env python3
import argparse
from compiler import CCompiler
import processor

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Compile bf source code into c code')
    parser.add_argument('bfname')
    parser.add_argument('cname', nargs='?', default='a.c')
    parser.add_argument('-c', dest='compile', nargs='?', default=False, const=True)
    parser.add_argument('-o', dest='binname', nargs='?', default='a.out')

    args = parser.parse_args()

    instructions, debug_info = processor.load(args.bfname, False)

    executor = CCompiler(instructions, args.cname, args.compile, args.binname) 
 
    processor.process(instructions, executor)