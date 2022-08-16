#!/usr/bin/env python3

import sys
from parser import ltl_parser

def prefix(f):
	'''
	Convert an infix formula to prefix form

	Example:
		infix: ['always', ['p1', 'implies', ['eventually', 'p2']]]
		prefix: ['always', ['implies', 'p1', ['eventually', 'p2']]]
	'''
	if isinstance(f, list):
		if len(f) == 2:
			f[0], f[1] = prefix(f[0]), prefix(f[1])
			return f
		else:
			f[0], f[1], f[2] = prefix(f[1]), prefix(f[0]), prefix(f[2])
			return f
	else:
		return f

def pprefix(f):
	'''
	Convert prefix formula from list form to human readable string format

	Example:
		prefix formula: ['always', ['p1', 'implies', ['eventually', 'p2']]]
		human readable: always(implies(p1, eventually p2))
	'''
	if isinstance(f, list):
		if len(f) == 2:
			if isinstance(f[1], str):
				return pprefix(f[0]) + ' ' + pprefix(f[1])
			else:
				return pprefix(f[0]) + '(' + pprefix(f[1]) + ')'
		else:
			return pprefix(f[0]) + '(' + pprefix(f[1]) + ', ' + pprefix(f[2]) + ')'
	else:
		return f

def spec(file):
	try:
		f = open(file, "r")
		formula = f.read()
		f.close()

		infix = ltl_parser(formula)
		#print(infix)
		return prefix(infix)

	except Exception as e:
		print(e)
		sys.exit(1)

