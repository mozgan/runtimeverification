#!/usr/bin/env python3

import sys

this = sys.modules[__name__]

'''
LTL+Past Grammar
================
psi ::= p | not psi | psi1 or psi2 | psi1 and psi2 | psi1 implies psi2 |
		w_prev psi | s_prev psi | once psi | w_next psi | s_next psi |
		historically psi | psi1 since psi2 | eventually psi | always psi |
		psi1 until psi2

LTL+Past Semantics
==================
*) P be a set of propositions and let p € P be a proposition.
*) A finite sequence can be defined as s: P x T -> B where T € [0, t] and
	B € {True, False}. s[i] is the i-th item of the sequence s.
*) Satisfaction Relation |=: Seq x PSI -> True where Seq is the sequence and
	PSI is the formula. We say "s satisfies psi" and write
	"s |= psi" iff "s[0] |= psi", i.e. "(s[0], psi) |= True". "s |/= psi"
	means that "s does not satisfy psi" and equivalent to "s |= not psi".

s[i] |= p <-> p € s[i]
s[i] |= psi <-> (s[i], psi) |= True
s[i] |= not psi <-> s[i] |/= psi
s[i] |= psi1 or psi2 <-> s[i] |= psi1 OR s[i] |= psi2
s[i] |= psi1 and psi2 <-> s[i] |= psi1 AND s[i] |= psi2
s[i] |= psi1 implies psi2 <-> s[i] |= not psi1 OR s[i] |= psi2
s[i] |= w_prev psi <-> if i = 0 then True, otherwise s[i-1] |= psi
s[i] |= s_prev psi <-> if i = 0 then False, otherwise s[i-1] |= psi
s[i] |= w_next psi <-> if i = |s| then True, otherwise s[i+1] |= psi
s[i] |= s_next psi <-> if i = |s| then False, otherwise s[i+1] |= psi
s[i] |= psi1 since psi2 <-> E j € [0, i]: s[j] |= psi2 AND A k € (j, i]: s[k] |= psi1
s[i] |= psi1 until psi2 <-> E j € [i, |s|]: s[j] |= psi2 AND A k € [i, j): s[k] |= psi1
s[i] |= eventually psi <-> E j € [i, |s|]: s[j] |= psi
s[i] |= always psi <-> A j € [i, |s|]: s[j] |= psi
s[i] |= once psi <-> E j € [0, i]: s[j] |= psi
s[i] |= historically psi <-> A j € [0, i]: s[j] |= psi

E .. There exists
A .. For all
|s| .. Lenth of sequence

Equivalences
============
psi1 implies psi2 = not psi1 or psi2
once psi = psi or s_prev (once psi)
historically psi = psi and w_prev (historically psi)
psi1 since psi2 = psi2 or (psi1 and s_prev (psi1 since psi2))
eventually psi = psi or s_next (eventually psi)
always psi = psi and w_next (always psi)
psi1 until psi2 = psi2 or (psi1 and s_next (psi1 until psi2))

References
==========
*) T. Latvala, A. Biere, K. Heljanko, T. Junttila - Simple is Better: Efficient Bounded Model Checking for Past LTL
	: http://fmv.jku.at/papers/latvalabiereheljankojunttila-vmcai05.pdf
	: http://tcs.legacy.ics.tkk.fi/users/tlatvala/vmcai2005/LBHJ-vmcai2005-slides.pdf

*) M. Benedetti, A. Cimatti - Bounded Model Checking for Past LTL
	: https://link.springer.com/content/pdf/10.1007%2F3-540-36577-X_3.pdf

*) K. Havelund, G. Rosu - Synthesizing Monitors for Safety Properties
	: https://ti.arc.nasa.gov/m/pub-archive/archive/0345.pdf
'''

UNARY = ['not', 'w_prev', 's_prev', 'once', 'w_next', 's_next',
		 'historically', 'eventually', 'always']
BINARY = ['or', 'and', 'implies', 'since', 'until']

def SplitPSI(psi1, psi2, s, i):
	'''
	Split the given formulas.
	'''
	if psi1[0] in UNARY:
		# the first element is an unary operation
		f1 = getattr(this, psi1[0].upper())
		r1 = f1(psi1[1], s, i)
	elif psi1[0] in BINARY:
		# the first element is an binary operation
		f1 = getattr(this, psi1[0].upper())
		r1 = f1(psi1[1], psi1[2], s, i)
	else:
		# formula is an atomic proposition
		r1 = s[psi1][i]

	if psi2 is not None:
		if psi2[0] in UNARY:
			# the first element is an unary operation
			f2 = getattr(this, psi2[0].upper())
			r2 = f2(psi2[1], s, i)
		elif psi2[0] in BINARY:
			# the first element is an binary operation
			f2 = getattr(this, psi2[0].upper())
			r2 = f2(psi2[1], psi2[2], s, i)
		else:
			# formula is an atomic proposition
			r2 = s[psi2][i]
	else:
		# if psi2 does not exist, then return None
		r2 = None

	return r1, r2

def NOT(psi, s, i):
	r1, _ = SplitPSI(psi, None, s, i)
	return (not r1)

def OR(psi1, psi2, s, i):
	r1, r2 = SplitPSI(psi1, psi2, s, i)
	return (r1 or r2)

def AND(psi1, psi2, s, i):
	r1, r2 = SplitPSI(psi1, psi2, s, i)
	return (r1 and r2)

def IMPLIES(psi1, psi2, s, i):
	'''
	psi1 IMPLIES psi2 = (NOT psi1) OR psi2
	'''
	r1, r2 = SplitPSI(psi1, psi2, s, i)
	return (not r1 or r2)

def W_PREV(psi, s, i):
	if i == 0:
		return True
	else:
		r1, _ = SplitPSI(psi, None, s, i-1)
		return r1

def S_PREV(psi, s, i):
	if i == 0:
		return False
	else:
		r1, _ = SplitPSI(psi, None, s, i-1)
		return r1

def W_NEXT(psi, s, i):
	l = len(list(s.values())[0])
	if i == l-1:
		return True
	else:
		r1, _ = SplitPSI(psi, None, s, i+1)
		return r1

def S_NEXT(psi, s, i):
	l = len(list(s.values())[0])
	if i == l-1:
		return False
	else:
		r1, _ = SplitPSI(psi, None, s, i+1)
		return r1

def SINCE(psi1, psi2, s, i):
	'''
	psi1 SINCE psi2 = psi2 OR (psi1 AND S_PREV (psi1 SINCE psi2))
	'''
	PSI = ['since', psi1, psi2]
	r1, r2 = SplitPSI(psi1, psi2, s, i)
	r3, _ = SplitPSI(['s_prev', PSI], None, s, i)
	return (r2 or (r1 and r3))

def UNTIL(psi1, psi2, s, i):
	'''
	psi1 UNTIL psi2 = psi2 OR (psi1 AND S_NEXT (psi1 UNTIL psi2))
	'''
	PSI = ['until', psi1, psi2]
	r1, r2 = SplitPSI(psi1, psi2, s, i)
	r3, _ = SplitPSI(['s_next', PSI], None, s, i)
	return (r2 or (r1 and r3))

def EVENTUALLY(psi, s, i):
	'''
	EVENTUALLY psi = psi OR S_NEXT (EVENTUALLY psi)
	'''
	PSI = ['eventually', psi]
	r1, r2 = SplitPSI(psi, ['s_next', PSI], s, i)
	return (r1 or r2)

def ALWAYS(psi, s, i):
	'''
	ALWAYS psi = psi AND W_NEXT (ALWAYS psi)
	'''
	PSI = ['always', psi]
	r1, r2 = SplitPSI(psi, ['w_next', PSI], s, i)
	return (r1 and r2)

def ONCE(psi, s, i):
	'''
	ONCE psi = psi OR S_PREV (ONCE psi)
	'''
	PSI = ['once', psi]
	r1, r2 = SplitPSI(psi, ['s_prev', PSI], s, i)
	return (r1 or r2)

def HISTORICALLY(psi, s, i):
	'''
	HISTORICALLY psi = psi AND W_PREV (HISTORICALLY psi)
	'''
	PSI = ['historically', psi]
	r1, r2 = SplitPSI(psi, ['w_prev', PSI], s, i)
	return (r1 and r2)

