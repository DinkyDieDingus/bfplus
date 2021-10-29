#!/usr/bin/env python3
import argparse
from src.interpreter import Interpreter
import src.processor as processor

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Debug bf source code through the interpreter')
    parser.add_argument('bfname')
    parser.add_argument('-bi', dest='byte_input', action='store_true')
    parser.add_argument('-bo', dest='byte_output', action='store_true')

    args = parser.parse_args()

    instructions, debug_info = processor.load(args.bfname, True)

    executor = Interpreter(instructions, args.byte_input, args.byte_output, True, debug_info) 
 
    processor.process(instructions, executor)