#!/usr/bin/env python3

import argparse
import sys

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Prettify bf source code')

	parser.add_argument('bfname')
	parser.add_argument('-o', dest='outname')
	parser.add_argument('-c', dest='compress', action='store_true')

	args = parser.parse_args()

	dataset = '<>[]+-.,'

	indent = 0
	streak = 0
	out = ''
	prev = '\0'
	word = False
	with open(args.bfname, 'r') as file:
		inp = ''.join(file.readlines())
	for idx, char in enumerate(inp):
		if args.compress:
			if char in dataset:
				out += char
				continue

		if char in dataset:
			word = False
			if char == prev:
				streak += 1
			else:
				streak = 0
			if streak == 4:
				out += ' '
				streak = 0

			if char in '<>':
				if char != prev:
					out += '\n' + indent * '  '
				out += char
			elif char in '[]':
				if char == '[':
					out += '\n'
				else:
					indent -= 1
				out += '\n' + indent * '  ' + char
				if char == '[':
					indent += 1
				else:
					out += '\n'
			elif char in ',.':
				if prev in '[]':
					out += '\n' + indent * '  '
				elif prev in '<>':
					out += ' '
				out += char
			else:
				if prev in '[]':
					out += '\n' + indent * '  '
				if prev in '<>':
					out += ' '
				out += char

			prev = char
		elif char not in '\n\r':
			if word or char != ' ':
				if not word and prev in dataset:
					startIdx = len(out) - 1
					while startIdx >= 0 and out[startIdx] != '\n':
						startIdx -= 1 
					linelen = len(out) - startIdx
					if linelen != 1:
						print(f'linelen: {linelen}')
						remainder = 4 - (linelen - 1) % 4
						print(f'remainder {char}: {remainder}')
						out += ' ' * remainder
				out += char
				word = True
		else:
			nxt = ''
			i = 1
			while nxt in ' \n\r' and idx + i != len(inp):
				nxt = inp[idx + i]
				i += 1
			if nxt not in dataset:
				out += '\n'
				

	file = sys.stdout
	if args.outname != None:
		file = open(args.outname, 'w')

	file.write(out)

	if args.outname != None:
		file.close()
