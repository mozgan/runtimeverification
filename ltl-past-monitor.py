#!/usr/bin/env python3

import sys

import LTLPast
from spec import *
from sequence import sequence

def monitoring(formula, sequence):
	index = 0
	if isinstance(formula, str):
		# formula: an atomic proposition
		return sequence[formula][index]
	elif len(formula) == 2:
		# formula[0]: unary opereation
		f = getattr(LTLPast, formula[0].upper())
		return f(formula[1], sequence, index)
	else:
		# formula[0]: binary operation
		f = getattr(LTLPast, formula[0].upper())
		return f(formula[1], formula[2], sequence, index)

if __name__ == "__main__":

	if len(sys.argv) != 3:
		print("Usage: ltl-past-monitor.py specification.ltl inputs.csv")
		sys.exit(1)

	f = spec(sys.argv[1])
	#print(f)	# print formula in prefix form
	#print(pprefix(f))	# print formula in human readable format

	s = sequence(sys.argv[2])
	#print(s)	# sequence in dict format

	if monitoring(f, s) == True:
		print("Pass")
	else:
		print("Fail")

