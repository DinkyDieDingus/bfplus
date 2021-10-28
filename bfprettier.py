#!/usr/bin/env python3

import argparse
import sys

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Prettify bf source code')

	parser.add_argument('bfname')
	parser.add_argument('-o', dest='outname')

	args = parser.parse_args()

	indent = 0
	streak = 0
	out = ''
	prev = ''
	prevprev = ''
	with open(args.bfname, 'r') as file:
		for line in file:
			for char in line:
				if char == prev:
					streak += 1
				else:
					streak = 0

				if streak == 4:
					out += ' '
					streak = 0

				if char == '[':
					out += '\n\n' + indent * '    '
					indent += 1
				elif char == ']':
					indent -= 1
					out += '\n' + indent * '    '
				elif char in '<>':
					if prev != char:
						out += '\n' + indent * '    '
				elif char in '.,':
					if prev not in '<>' and prev != char:
						out += '\n' + indent * '    '
				else:
					if prev in '<>':
						out += ' '
					elif prev in '.,':
						out += '\n' + indent * '    '

				out += char

				if char == '[':
					out += '\n' + indent * '    '
				elif char == ']':
					out += '\n\n' + indent * '    '
				
				prevprev = prev
				prev = char

	file = sys.stdout
	if args.outname != None:
		file = open(args.outname, 'w')

	file.write(out)

	if args.outname != None:
		file.close()
