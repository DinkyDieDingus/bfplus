#!/usr/bin/env python3
import argparse
from src.interpreter import Interpreter
import src.processor as processor

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Interpret bf source code')
    parser.add_argument('bfname')
    parser.add_argument('-d', dest='debug', nargs='?', default=False, const=True)
    parser.add_argument('-bi', dest='byte_input', action='store_true')
    parser.add_argument('-bo', dest='byte_output', action='store_true')

    args = parser.parse_args()

    instructions, debug_info = processor.load(args.bfname, args.debug)

    executor = Interpreter(instructions, args.byte_input, args.byte_output, args.debug, debug_info)   
 
    processor.process(instructions, executor)