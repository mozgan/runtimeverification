#!/usr/bin/env python3

import sys

def sequence(file):
	'''
	Read the sequence from file and return it in dictionary structure

	Example:
		In file:
			p1, p2, p3
			1,  0,  0
			0,  1,  0
			0,  0,  1

		In dictionary form:
			{
                'p1': [True, False, False],
                'p2': [False, True, False],
                'p3': [False, False, True]
            }
	'''
	try:
		f = open(file, "r")
		contents = f.readlines()
		f.close()

		contents = [c.strip().split(',') for c in contents]
		contents[0] = [c.replace(' ', '') for c in contents[0]]
		return {i[0]: [int(x) == 1 for x in i[1:]] for i in zip(*contents)}

	except Exception as e:
		print(e)
		sys.exit(1)

