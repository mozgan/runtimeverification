#!/usr/bin/env python3

import sys
from tatsu import parse	# Used Version: 4.2.6

GRAMMAR = '''
	# ignore C style comments, i.e.
	# /* this is a comment and
	#    must be ignored!
	# */
	@@comments :: /\/\*(\*(?!\/)|[^*])*\*\//

	# ignore Python style comments
	@@eol_comments :: /#.*?$/

	# LTL+Past Grammar
	@@grammar :: LTL_Past

	start = expression $ ;

	expression =
		| expression 'or' expression
		| expression 'and' expression
		| expression 'implies' expression
		| expression 'since' expression
		| expression 'until' expression
		| formula
		;

	formula =
		| 'not' formula
		| 'w_prev' formula
		| 's_prev' formula
		| 'once' formula
		| 'w_next' formula
		| 's_next' formula
		| 'historically' formula
		| 'eventually' formula
		| 'always' formula
		| factor
		;

	factor =
		| '(' ~ @:expression ')'
		| atom
		;

	atom = /p\d+/ ;
'''

def ltl_parser(ltl_formula):
	try:
		return parse(GRAMMAR, ltl_formula, rule_name='start')
	except Exception as e:
		print("Syntax Error! - " + str(e))
		sys.exit(1)

