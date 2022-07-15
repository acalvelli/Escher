import random
import copy
import numpy
from inspect import signature
import time
import matplotlib.pyplot as plt

# *************************************************
# ****  Types that can be called in test **********
# *************************************************
NUM = "NUM"
VAR = "VAR"
PLUS = "PLUS"
TIMES = "TIMES"
LT = "LT"
ITE = "ITE"
ZERO = "ZERO"
FALSE_exp = "FALSE"
TRUE_exp = "TRUE"
NONNEG = "NONNEG"
NEG = "NEG"
INC = "INC"
DEC = "DEC"
FIB = "FIB"
FACT = "FACT"
# list ops
LIST = "LIST"
CONS = "CONS"
HEAD = "HEAD"
LENGTH = "LENGTH"
TAIL = "TAIL"
EMPTY = "EMPTY"
CONCAT = "CONCAT"
FACT = "FACT"
REVERSE = "REVERSE"
NIL = "NIL"
SELF = "SELF"

# used to store the comps that can be used
COMPS = []

class Error(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


# *************************************************
# ***********  AST node definitions ***************
# *************************************************
    
class Node:
    arity = 0
    def __str__(self):
        raise Error("Unimplemented method: str()")

    def interpret(self):
        raise Error("Unimplemented method: interpret()")
  

# THIS IS THE RECURSIVE COMPONENT
class Self(Node):
    # right now hardcode to compile
    arity = 0
    def __init__(self, comp, arity):
        self.type = SELF
        self.comp = comp
        self.c_type = strToType(comp)
        self.arity = arity
    
    def __str__(self):
        return str(self.comp)
        
    # interprets the recursive call, need to redefine evaluate
    def interpret(self, envt):
        # know that terminates
        print("self interpret...")

        

class FalseExp(Node):
    arity = 0
    def __init__(self):
        self.type = FALSE_exp

    def __str__(self):
        return "false"

    def interpret(self, envt):
        return False

class TrueExp(Node):
    arity = 0
    def __init__(self):
        self.type = TRUE_exp

    def __str__(self):
        return "true"

    def interpret(self, envt):
        return True

class Neg(Node):
    arity = 1
    def __init__(self, inner):
        self.type = NEG
        self.inner = inner

    def __str__(self):
        return "-" + str(self.inner)

    def interpret(self, envt):
        return self.inner.interpret(envt) * -1  
        
class NonNeg(Node):
    arity = 1
    def __init__(self, inner):
        self.type = NONNEG
        self.inner = inner

    def __str__(self):
        return str(self.inner) + " >= 0"

    def interpret(self, envt):
        val = self.inner.interpret(envt)
        return val >= 0
              
# list functions
class List(Node):
    arity = 1
    def __init__(self, vals):
        self.type = LIST
        self.vals = vals
    
    def __str__(self):
        s = ""
        s = str(self.vals)
        return '[' + s + ']'
        
    def interpret(self, envt):
        v1 = copy.deepcopy(self.vals.interpret(envt))
        if(type(v1) != list):
            res = []
            res.append(v1)
            v1 = res
        return v1
        

class Zero():
    arity = 0
    def __init__(self):
        self.type = ZERO
        
    def __str__(self):
        return str(0)
        
    def interpret(self, envt):
        return 0
        
class Nil():
    arity = 0
    def __init__(self):
        self.type = NIL
        
    def __str__(self):
        return str("[]")
        
    def interpret(self, envt):
        return []
     
# this should be recursive component synthesizing       
class Length(Node):
    arity = 1
    def __init__(self, inner):
        self.type = LENGTH
        self.inner = inner
        
    def __str__(self):
        return "|" + str(self.inner) + "|"
    
    def interpret(self, envt):
        v1 = copy.deepcopy(self.inner.interpret(envt))
        if(type(v1) != list):
            res = []
            res.append(v1)
            v1 = res
        if("err" in v1):
            return "err"
        return len(v1)


class Tail(Node):
    arity = 1
    def __init__(self, inner):
        self.type = TAIL
        self.inner = inner
        
    def __str__(self):  
        return "Tail(" + str(self.inner) + ")"
        
    def interpret(self, envt):
        v1 = copy.deepcopy(self.inner.interpret(envt))
        if(type(v1) != list):
            res = []
            res.append(v1)
            v1 = res
        if(len(v1) == 0 or "err" in v1):
            return "err"
        else:
            return v1[1:]
            
        
class Empty(Node):
    arity = 1
    def __init__(self, inner):
        self.type = EMPTY
        self.inner = inner
        
    def __str__(self):
        return "Empty(" + str(self.inner) + ")"
    
    def interpret(self, envt):
        v1 = copy.deepcopy(self.inner.interpret(envt))
        if(type(v1) != list):
            res = []
            res.append(v1)
            v1 = res
        return len(v1) == 0

# deep copy list values then append, works for (List, concat, tail)
class Concat(Node):
    arity = 2
    def __init__(self,left,right):
        self.type = CONCAT
        self.left = left
        self.right = right
              
    def __str__(self):
        return "Concat(" + str(self.left) + "," + str(self.right) + ")"
        
    def interpret(self,envt):
        v1 = copy.deepcopy(self.left.interpret(envt))
        if(type(v1) != list):
            res = []
            res.append(v1)
            v1 = res
        v2 = copy.deepcopy(self.right.interpret(envt))
        if(type(v2) != list):
            res = []
            res.append(v2)
            v2 = res
        v1.extend(v2)
        return v1
 
class Inc(Node):
    arity = 1
    # must increment the value of any type
    def __init__(self, inner):
        self.type = INC
        self.inner = inner
    
    def __str__(self):
        return str(self.inner) + " + 1"
        
    def interpret(self, envt):
        val = self.inner.interpret(envt)
        if val == "err":
            return 'err'
        return self.inner.interpret(envt) + 1

class Dec(Node):
    arity = 1
    # must increment the value of any type
    def __init__(self, inner):
        self.type = Dec
        self.inner = inner
    
    def __str__(self):
        return str(self.inner) + " - 1"
        
    def interpret(self, envt):
        val = self.inner.interpret(envt)
        if val == "err":
            return 'err'
        return self.inner.interpret(envt) - 1

class Var(Node):
    arity = 1
    def __init__(self, name):
        self.type = VAR
        self.name = name

    def __str__(self):
        return self.name

    def interpret(self, envt):
        return envt[self.name]


class Num(Node):
    arity = 1
    def __init__(self, val):
        self.type = NUM
        self.val = val

    def __str__(self):
        return str(self.val)

    def interpret(self, envt):
        return self.val


class Plus(Node):
    arity = 2
    def __init__(self, left, right):
        self.type = PLUS
        self.inner = left
        self.right = right

    def __str__(self):
        return "(" + str(self.inner) + "+" + str(self.right) +")"

    def interpret(self, envt):
        return self.inner.interpret(envt) + self.right.interpret(envt)

class Times(Node):
    arity = 2
    def __init__(self, left, right):
        self.type = TIMES
        self.left = left
        self.right = right

    def __str__(self):
        return "(" + str(self.left) + "*" + str(self.right) + ")"

    def interpret(self, envt):
        return self.left.interpret(envt) * self.right.interpret(envt)

class Lt(Node):
    arity = 2
    def __init__(self, left, right):
        self.type = LT
        self.left = left
        self.right = right

    def __str__(self):
        return "(" + str(self.left) + "<" + str(self.right) + ")"

    def interpret(self, envt):
        return self.left.interpret(envt) < self.right.interpret(envt)

class Fib(Node):
    arity = 1
    def __init__(self, inner):
        self.type = FIB
        self.inner = inner

    def __str__(self):
        return "Fib(" + str(self.inner) + ")"

    def interpret(self, envt):

        n = self.inner.interpret(envt)
        return fib(n)
    
# function for fib   
def fib(n):
    if (n <= 1):
        return 1
    return fib(n-1) + fib(n-2)


class Fact(Node):
    arity = 1
    def __init__(self, inner):
        self.type = FACT
        self.inner = inner
        
    def __str__(self):
        return "(" + str(self.inner) + ")!"
        
    def interpret(self, envt):
        n = self.inner.interpret(envt)
        if(n <= 1):
            return 1
        
        return fact(n)

def fact(n):
    if(n <= 1):
        return 1
    return n * fact(n-1)
    
class Head(Node):
    arity = 1
    def __init__(self, inner):
        self.type = HEAD
        self.inner = inner
        
    def __str__(self):
        return "[" + str(self.inner) + "]"
        
    def interpret(self, envt):
        v = copy.deepcopy(self.inner.interpret(envt))
        if(type(v) != list):
            res = []
            res.append(v)
            v = res
        if len(v) == 0 or v[0] == 'err':
            return 'err'
        
        return v[0]
        
        
class Cons(Node):
    arity = 2
    def __init__(self, left, right):
        self.type = CONS
        self.left = left
        self.right = right
        
    def __str__(self):
        return  "[" + str(self.left) + ":" + str(self.right) + "]"
        
    def interpret(self, envt):
        v = copy.deepcopy(self.left.interpret(envt))
        
        if(type(v) != list):
            res = []
            res.append(v)
            v = res
        v2 = copy.deepcopy(self.right.interpret(envt))
        
        if(type(v2) != list):
            res2 = []
            res2.append(v2)
            v2 = res2
            
        if len(v) == 0 or 'err' in v:
            if len(v2) == 0 or 'err' in v2:
                return []
            return v2
        
        v.extend(v2)
        return v


class Reverse(Node):
    arity = 1
    def __init__(self, inner):
        self.type = REVERSE
        self.inner = inner
        
    def __str__(self):
        return  str(self.inner)
        
    def interpret(self, envt):
        v = copy.deepcopy(self.inner.interpret(envt))
        
        if(type(v) != list):
            res = []
            res.append(v)
            v = res
        
        if v == 'err':
            return 'err'
            
        v.reverse()
        return v

class Ite(Node):
    arity = 3
    def __init__(self, c, t, f):
        self.type = ITE
        self.cond = c
        self.tcase = t
        self.inner = f

    def __str__(self):
        return "(if " + str(self.cond) + " then " + str(self.tcase) + " else " + str(self.inner) + ")"

    def interpret(self, envt):
        if (self.cond.interpret(envt)):
            return self.tcase.interpret(envt)
        else:
            return self.inner.interpret(envt)


# ************************************************
# *************** Helper Functions **************
# **********************************************

def strToType(term):
	if term == "VAR":
		return Var
	elif term == "NUM":
		return Num
	elif term == "LT":
		return Lt
	elif term == "ITE":
		return Ite
	elif term == "PLUS":
		return Plus
	elif term == "TIMES":
		return Times
	elif term == "LIST":
		return List
	elif term == "LENGTH":
		return Length
	elif term == "EMPTY": 
		return Empty
	elif term == "TAIL":
		return Tail
	elif term == "CONCAT":
		return Concat
	elif term == "FALSE":
		return FalseExp
	elif term == "TRUE":
		return TrueExp
	elif term == "ZERO":
		return Zero
	elif term == "SELF":
		return Self
	elif term == "INC":
		return Inc
	elif term == "DEC":
		return Dec	
	elif term == "FIB":
		return Fib	
	elif term == "FACT":
		return Fact	
	elif term == "HEAD":
		return Head
	elif term == "CONS":
		return Cons
	elif term == "REVERSE":
		return Reverse
	elif term == "NIL":
		return Nil
		            
# *************************************************
# ***********  ESCHER Functions ***************
# *************************************************

# initializes the goal graph, etc.
# set syn to be the list of input variables and goalGraph to be inputoutputs
def initialize(Comps, vars, Ex):

	global var 
	var = vars
	global h_map	
	h_map = {}
	global COMPS
	COMPS = Comps
	global self
	self = Self(Comps[-1], len(vars))

	syn = []
	goalGraph = ()
	
	# add the terminals to plist
	# initialize the h_map	(key = program, val = num nodes)
	for v in vars:
		syn.append(Var(v))
		p = Var(v)
		h_map[p] = p.arity
		
	root = []
	
	
	# get the outputs of the i/o examples
	for ex in Ex:
		root.append(ex["_out"])
		
	# initialized so G = [root], R = [], E = [], root = [outputs]
	goalGraph = ([root],[],[],root)
	
	
	return escherAlgo(syn, goalGraph, Ex)



# has the rule scheduling of the algorithm
def escherAlgo(syn, goalGraph, Ex):
	global h_map
	# stores the saturated to check termination
	exp = []
	saturated =[]
	
	# tracks the iteration to search the heuristic 
	iteration = 1

	while True:
		
		print("ITERATION:", iteration)
		# only grow to programs of iteration # size
		grownList = forwardSearch(syn, Ex, iteration)	
		syn.extend(grownList)
			
		# every time a program synthesized
		for s in syn:
			#print("current program:", s, eval(s, Ex))
			
			# check if SATURATE
			# reboots the progam if recursive and solves the goal
			if type(s) == self.c_type and terminates(s, Ex, goalGraph[3]):
				exp = saturate(s, Ex, goalGraph[3])
				if exp and exp not in Ex:
					Ex.extend(exp)
					return initialize(COMPS,var, Ex)
						
			# check if TERMINATES and if works on SATURATED LIST
			if (terminates(s, Ex, goalGraph[3])):
				print("SAT program:", s)
				return s
			# if not, apply RESOLVE to close as many open goals possible
			syn, pr = resolve(goalGraph, syn, Ex)
			
			# checks if the resolver will satisfy
			if(pr and terminates(pr, Ex, goalGraph[3])):
				print("SAT program: after resolving", pr)
				return pr

			# apply SPLITGOAL if p matches some positions of an open goal
			split_bool, cond, g, Ex = shouldSplit(s, goalGraph[0], Ex)
			#print("should split:",split_bool)
			if split_bool:
				goalGraph = splitGoal(cond, goalGraph, g, syn, Ex)
			
		iteration += 1
				
		

# apply a component to syn programs
# updates the heuristics and returns the sorted list
def forwardSearch(syn, Ex, iteration):
	global h_map
	global self
	global exp
	res = []
	
	# get the list of boolean and number programs 
	bool_programs = []
	num_programs = []
	list_programs = []
		
	# add the programs to the correct lists
	for s in syn:
		if(type(s) in (List, Concat, Tail) or type(s.interpret(Ex[0])) == list):
			list_programs.append(s)
		elif(type(s) in (Var, Num, Length, Plus, Times, Ite, Inc, Dec, Zero, Neg, Fib, Fact)):
			num_programs.append(s)
		# empty should be in here
		elif(type(s) != Self):
			bool_programs.append(s)
	# only synthesize programs of size iteration
	for c in COMPS:

		# apply appropriate type programs to the nonterminals in the program rules 
		if(c in ("PLUS","TIMES","LT")):
			# go through and propogate with all the programs in numlist
			for np in num_programs:
				for np2 in num_programs:
					progs = [np, np2]
					if c == "PLUS":
						prop = Plus(np, np2)
						
					elif c == "LT":
						prop = Lt(np, np2)
					elif c == "TIMES":
						prop = Times(np, np2)
						
					if not equiv(syn, res, prop, Ex):
						h = heuristic(progs, prop)
						
						if(h == iteration):
							res.append(prop)
							h_map[str(prop)] = h 
		
		#add inc
		if(c in ("ZERO", "FALSE", "TRUE", "NIL")):
			if c == "ZERO":
				prop = Zero()
			elif c == "FALSE":
				prop = FalseExp()
			elif c == "NIL":
				prop = Nil()
			else:
				prop = TrueExp()
				
			if not equiv(syn, res, prop, Ex):
				h = heuristic([], prop)
				if(h + 1 == iteration):
					res.append(prop)
					h_map[str(prop)] = h + 1
		
		if (c in ("INC", "DEC", "NEG", "NONNEG")):
			for np in num_programs:
				if(c == "INC"):
					prop = Inc(np)
				elif(c == "DEC"):
					prop = Dec(np)					
				elif(c == "NONNEG"):
					prop = NonNeg(np)
				else:
					prop = Neg(np)
					
				if not equiv(syn, res, prop, Ex):
					h = heuristic([np], prop)
					
					if(h == iteration):
						res.append(prop)
						h_map[str(prop)] = h
					
		if(c == "LIST"):
			for np in num_programs:
				prop = List(np)
				if not equiv(syn, res, prop, Ex):
					h = heuristic([np], prop)
					if(h == iteration):
						res.append(prop)
						h_map[str(prop)] = h
					
			for bp in bool_programs:
				prop = List(bp)
				if not equiv(syn, res, prop, Ex):
					h = heuristic([bp], prop)
					if(h == iteration):
						res.append(prop)
						h_map[str(prop)] = h
	
							
		elif(c in ("CONCAT","CONS")):
			for l1 in list_programs:
				for l2 in list_programs:
					progs = [l1,l2]
					if c == "CONCAT":
						prop = Concat(l1, l2)
					else:
						prop = Cons(l1,l2)
					if not equiv(syn, res, prop, Ex):
						h = heuristic(progs, prop)
						if(h == iteration):
							res.append(prop)
							h_map[str(prop)] = h
		
		elif(c in ("TAIL", "EMPTY","HEAD")):
			for l in list_programs:
				if c == "TAIL":
					prop = Tail(l)
				elif c == "HEAD":
					prop = Head(l)
				else:
					prop = Empty(l)
					
				if not equiv(syn, res, prop, Ex):
					h = heuristic([l], prop)
					if(h == iteration):
						res.append(prop)
						h_map[str(prop)] = h
					
		elif(c == "LENGTH"):	
			for l in list_programs:
				prop = Length(l)
				if (termination_argument(prop, Ex)):
					# checks if equivalent with the REAL function?
					if not equiv(syn, res, prop, Ex):
						h = heuristic([l], prop)
						if(h == iteration):
							# check if passes the termination argument
							if(c == self.comp):
								res.append(prop)
								h_map[str(prop)] = h
		elif(c == "FACT"):	
			for np in num_programs:
				prop = Fact(np)
				if(max(eval(np, Ex)) > 10):
					continue
				if (termination_argument(prop, Ex)):
					# checks if equivalent with the REAL function?
					if not equiv(syn, res, prop, Ex):
						h = heuristic([np], prop)
						if(h == iteration):
							# check if passes the termination argument
							if(c == self.comp):
								res.append(prop)
								h_map[str(prop)] = h

		elif(c == "FIB"):
			for np in num_programs:
	
				prop = Fib(np)
				if (termination_argument(prop, Ex)):
					if not equiv(syn, res, prop, Ex):
						h = heuristic([np], prop)
						
						if(h == iteration):
							# check if passes the termination argument
							if(c == self.comp):
								#print("recursive type", c, prop)
								res.append(prop)
								h_map[str(prop)] = h
		
		elif(c == "REVERSE"):
			for l in list_programs:
	
				prop = Reverse(l)
				if (termination_argument(prop, Ex)):
					if not equiv(syn, res, prop, Ex):
						h = heuristic([l], prop)
						if(h == iteration):
							# check if passes the termination argument
							if(c == self.comp):
								#print("recursive type", c, prop)
								res.append(prop)
								h_map[str(prop)] = h
					
	
	return res

# look for current p to get old value, otherwise make new
def heuristic(plist, prog):
	global h_map

	penalize = 0
	h_val = 0
	params = 0
	
	# get the value of the old term
	for p in plist:
		
		# penalize the program by multiply current size by 
		if(type(p) == type(prog)):
			penalize = prog.arity
		
		# stupid fix
		if(type(p) == Var):
			params += 1
		
		# add the new value to the map, penalize if repeates
		if(str(p) in h_map):
			params += prog.arity + h_map[str(p)] + (penalize * h_map[str(p)])	
		
		else:
			params += prog.arity
			
		# reset the penalty
		penalize = 0
		
	h_val = params
	return h_val
	
# returns a value vector of applying the terms 
def eval(term, Ex):
	val = []
	for ex in Ex:
		val.append(term.interpret(ex))
	
	return val	
	
# compute the value vectors and see if observational equivalence
def equiv(syn, res, prop, Ex):
	# returns a value vector of applying the terms 
	val = eval(prop, Ex)
	
	# check if same as a term added
	for s in syn:
		r1 = eval(s, Ex)
		if (val == r1):
			return True
	# check if same as term just added		
	for r in res:
		r2 = eval(r, Ex)
		if(r2 == r1):
			return True
	
	return False
		
# checks if passes termination argument	
def termination_argument(prop, Ex):
	#print("checking if ", prop, " terminates")
	res = []
	# get the first iteration
	og = eval(self.c_type(Var(var[0])), Ex)
	res.append(og)

	if(type(prop) == Var or prop.inner.arity == 0):
		return False
	# compute the next iteration
	next = eval(prop,Ex)
	#print("next:", next)
	#print(eval(type(prop)(prop.inner),Ex))
	
	val = []
	# check 

	if type(next[0]) == list:
		for i in range(len(next)):
			# if greater or an 'err' mark as error
			if('err' in next[i] or len(next[i]) >= len(og[i])):
				val.append('err')
			# otherwise mark as the evaluation
			else:
				val.append(next[i])
		
	else:
		for i in range(len(next)):
			# if greater or an 'err' mark as error
			if(next[i] == 'err' or next[i] >= og[i]):
				val.append('err')
			# otherwise mark as the evaluation
			else:
				val.append(next[i])

	# if all are errors then bad
	if val.count('err') == len(val):
		#print("NO TERMINATION")
		return False
	else:
		return True

# takes in a recursive program, current io list, root goal
def saturate(prop, Ex, root):
	# new i/o pair must have all the variables
	var_adding = var[0]

	res = []
	og_inputs = []
	exp = []
	# get the original inputs
	for ex in Ex:
		og_inputs.append(ex[var[0]])

	# get the first iteration
	og = eval(self.c_type(Var(var[0])), Ex)
	res.append(og)
	
	new_inputs = []
	new_outputs = []

	# get the innermost term
	if(type(prop) != Var):
		if(type(prop) == Ite):
			prop = prop.inner
		# if plus need to saturate left and right
		if(type(prop) in (Plus,Concat,Cons)):
			new_inputs.extend(eval(prop.right.inner, Ex))
			new_outputs.extend(eval(self.c_type(prop.right.inner), Ex))
			
		while (type(prop.inner) not in (Var,Plus,Cons,Concat)):
			prop = prop.inner
			
	# prop = the next iterations	
	new_inputs.extend(eval(prop, Ex))
	new_outputs.extend(eval(self.c_type(prop), Ex))
	

	
	# add a pair that is not in the original inputs
	for n in range(len(new_inputs)):
		if (new_inputs[n] != 'err' and new_inputs[n] not in og_inputs):
			pair = {}
			pair[var[0]] = new_inputs[n]
			pair['_out'] = new_outputs[n]
			if pair not in exp:
				exp.append(pair)
			
	print("Adding the saturated examples:")
	print(exp)
	
	return exp


# determines from inputoutputs if program is SAT
# terminate the algo when a program matchng the root goal has been synthesized
def terminates(program, Ex, root):

	v = eval(program, Ex)
		
	return match(v, root)	
	
# returns true iff value vector matches the goal
# find a program P such that interpret(P) matches root
def match(v, g):

	# v matches g
	for i in range(0, len(v)):
		if g[i] != '?' and v[i] != g[i]:
			return False;
	return True
	
# s is a program, G is a goal, Ex
# returns true if the current program s matches some elements of a certain goal
def shouldSplit(s, G, Ex):

	cond = []
	
	# compute the value vector for each input
	v = eval(s, Ex)
	
	# for each goal (g in G is size v)
	for g in G:
		for i in range(len(g)):
			# splits the case because 0, 1 evaluate to true and false
			if(g[i] == 0 or g[i] == 1):
				cond.append(g[i] is v[i])
			else:
				cond.append(g[i] == v[i])

		# if returns true, then split on this with the value cond
		return True in cond, cond, g, Ex
		

# split goal is called if the current program works for some outputs of one of the goals
# passes in the arbitrary boolean vector and associated goal
# takes in boolean vector, goalGraph, current goal, list programs, io examples
def splitGoal(cond, goalGraph, g, syn, Ex):
	#print("splitting:", cond)

	G = goalGraph[0]
	R = goalGraph[1]
	E = goalGraph[2]
	root = goalGraph[3]
	
	# number of output examples need
	length = len(g)	

	bthen = []
	belse = []
	
	# from cond and g, compute then and else goals which agree with G on positions
	for c in range(0,length):
		if cond[c]:
			bthen.append(g[c])
			belse.append("?")
		else:
			bthen.append("?")
			belse.append(g[c])
	
	# updates the goal graph as in inference rules
	G.extend([cond, bthen, belse])
	E.extend([g,cond,bthen,belse]) 
	# R is a list storing lists of conditions to sat
	R.append([cond,bthen,belse])

	
	# may need to remake this instead of update
	return goalGraph
	
	
# pass in [cond,bthen,belse] return an ITE resolver with programs from syn satisfying
def resolve(goalGraph, syn, Ex):
	
	# for each resolver (a list of cond, bthen, belse
	for resolver in goalGraph[1]:
		resolved = []
		#print("current resolver:", resolver)
		# for each subgoal trying to resolve
		for r in resolver:

			# look for a program which matches
			for s in syn:
				
				# gets the value vector of the program
				v = eval(s, Ex)	
				
				skip = False
				# type checks for efficiency purposes
				for i in range(len(v)):
					if(type(v[i]) != type(r[i]) and r[i] != '?'):
						skip = True
						
				if skip:
					continue
				
				# if find the goal should remove from the resolver?
				if(match(v, r)):
					#print("this program resolves ", r, ":", s)
					resolved.append((r,s))

					break

		
		pr = []
		if(len(resolved) == 3):
			pr = Ite(resolved[0][1], resolved[1][1], resolved[2][1])
			#print("resolves the goal:", pr)
			# should add pr to the synthesized program list
			syn.append(pr)
			# found the root goal
			if(eval(pr,Ex) == goalGraph[3]):
				return syn,pr
			

	# if not changed return syn
	return syn, None
	
#####################################################################################

# *************************************************
# *****************  TESTS ********************
# *************************************************

# fibonacci- THIS TEST DOES NOT WORK WELL, the correct programs are added to syn and the map, however the heuristic value of the recursive step is so large it take sa long time to physically get there
def fibTest():
    print ("####### ESCHER Algo (Test 1)#######")
    initialize(
        [ZERO, NONNEG, NEG, DEC, INC, PLUS, SELF, FIB],
        ["x"], [
		{"x":-3, "_out":1},
		{"x":0, "_out":1},
		{"x":1, "_out":1},
		{"x":2, "_out":2},
		{"x":3, "_out":3},
		{"x":4, "_out":5},
		{"x":5, "_out":8},
		{"x":6, "_out":13}]
    )

# length of a list
def lengthTest():
    print ("####### ESCHER Algo (Test 2)#######")
    initialize(
        [INC, EMPTY, TAIL, ZERO, SELF, LENGTH],
        ["l1"], [
		{"l1":[], "_out":0},
		{"l1":[1,2], "_out":2}]
    )

def reverseTest():
    print ("####### ESCHER Algo (Test 3)#######")
    initialize(
        [EMPTY, LIST, CONCAT, TAIL, HEAD, CONS, NIL, SELF, REVERSE],
        ["l1"], [
		{"l1":[], "_out":[]},
		{"l1":[1,2], "_out":[2,1]},
		{"l1":[1,2,3], "_out":[3,2,1]}]
    )


# length of a list
def factTest():
    print ("####### ESCHER Algo (Test 3)#######")
    initialize(
        [NONNEG, DEC, INC, ZERO, TIMES, SELF, FACT],
        ["x"], [
		{"x":3, "_out":6},
		{"x":-1, "_out":1},
		{"x":5, "_out":120},
		{"x":0, "_out":1}]
    )


# function to plot the time results for changing heuristic function
def time_trials(trials):
	
	plist = numpy.arange(0, trials,1.0).tolist()
	result = []
	
	for i in range(len(plist)):
		curr_trial = i
		# starts the time for the trial
		start = time.time()
		factTest()
		end = time.time()
		total_time = end - start
		result.append(total_time)

	# computes the average line
	avg = [numpy.mean(result)] * len(plist)
	# plot the data
	x_axis = plist
	y_axis = result
	plt.xlabel("Trials")
	plt.ylabel("Time to Run")
	
	
	plt.title("Time to Run over 10 Trials")
	plt.plot(x_axis, y_axis, label='Data')
	plt.xticks(numpy.arange(0,trials,1.0))
	avg_line = plt.plot(x_axis, avg, label = "Average =" + str(avg[0]), linestyle='--')
	
	legend = plt.legend(loc='upper right')
	plt.show()



if __name__ == '__main__':
    #fibTest()
    #factTest()
    #lengthTest()
    reverseTest()
    #time_trials(9)
					
			
