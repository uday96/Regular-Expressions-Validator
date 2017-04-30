import sys
sys.setrecursionlimit(100000)

def union(M1,M2):				#Constructs the union of given two automata
	n1=len(M1)
	n2=len(M2)
	n=n1+n2+2
	M=[]
	M.append([['#',1],['#',n1+1]])			#start state
	for i in range(n1):
		for x in M1[i]:
			#print x
			if len(x)!=0:
				x[1]+=1		
		M.append(M1[i])
	for i in range(n2):
		for x in M2[i]:
			#print x
			if len(x)!=0:
				x[1]+=1+n1
		M.append(M2[i])
	M[n1].pop()
	M[n1].append(['#',n1+n2+1])
	M[n1+n2].pop()
	M[n1+n2].append(['#',n1+n2+1])
	M.append([[]])					#final state
	return M

def concat(M1,M2):				#Constructs the concatenation of given two automata
	n1=n1=len(M1)
	n2=len(M2)
	n=n1+n2
	M=[]
	for i in range(n1):				#start state is that of M1
		M.append(M1[i])
	for i in range(n2):
		for x in M2[i]:
			if len(x)!=0:
				x[1]+=n1
		M.append(M2[i])				#final state is that of M2
	M[n1-1].pop()	
	M[n1-1].append(['#',n1])
	return M

def asterate(M1):				#Constructs the asterate of given automata
	n1=len(M1)
	n=n1+2
	M=[]
	M.append([['#',1],['#',n1+1]])			#start state
	for i in range(n1):
		for x in M1[i]:
			if len(x)!=0:
				x[1]+=1
		M.append(M1[i])
	M[n1].pop()	
	M[n1].append(['#',1])
	M[n1].append(['#',n1+1])
	M.append([[]])					#final state
	return M

def alph(a):					#Constructs the automaton for given alphabet
	M=[]
	if a=='#':
		return M
	else:
		M.append([[a,1]])
		M.append([[]])
		return M

def check(s,M,pntr):				#Checks for the membership of the given string wrt the automaton M
	str_len=len(s)				#Here, M is constructed from the input regular expression
	#print s, str_len, pntr
	if pntr==len(M)-1 and str_len==0:
		return True
	if len(s)!=0 and pntr==len(M)-1:
		return False
		
	arr=[]
	for y in M[pntr]:
		arr.append(y[0])
	#print arr	
	
	if str_len==0 and pntr!=len(M)-1:
		if '#' not in arr:
			return False
	
	if len(s)!=0 and s[0] not in arr and '#' not in arr:
		return False
	for x in M[pntr]:
		if x[0]=='#':
			pntr=x[1]			
			#check(s,M,pntr)
		elif x[0]==s[0]:
			pntr=x[1]
			s.pop(0)
			#check(s,M,pntr)
		if check(s,M,pntr):
			return True
	return False

def valid(exp):					#Checks if the input regular expression is valid or not
	
	"""
	Context Free Grammer for Regular Expressions:
		S=UX/UY/UZ
		X=SX1	Y=SY1	Z=SZ1
		X1=PX2	Y1=QX2	Z1=RV
		X2=SV
		P='+'  Q='.'  R='*'  U='('  V=')'
	"""

	St=[]
	for c in exp:
		St.append(c)
	n=len(St)											#input be a string St consisting of n characters: a1 ... an.
	n_non_terminals=13					
	r=n_non_terminals										#grammar contains r=13 nonterminal symbols R1 ... Rr.
	P=[[["False" for z in range(r)]for y in range(n)]for x in range(n)]				#P[n,n,r] array of booleans, Initialize all elements of P to false.
	NT=[]
	NT.append("S")	#0
	NT.append("X")	#1
	NT.append("Y")	#2
	NT.append("Z")	#3
	NT.append("X1")	#4
	NT.append("X2")	#5
	NT.append("Y1")	#6
	NT.append("Z1")	#7
	NT.append("P")	#8
	NT.append("Q")	#9
	NT.append("R")	#10
	NT.append("U")	#11
	NT.append("V")	#12
	prodcn=[[0,11,1],[0,11,2],[0,11,3],[1,0,4],[4,8,5],[5,0,12],[2,0,6],[6,9,5],[3,0,7],[7,10,12]]	#All productions of the form A=BC
	
	alphabets=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	#print P
	for i in range(n):
		if St[i] in alphabets:
			P[0][i][0]=True
		if St[i]=='(':
			P[0][i][11]=True
		if St[i]=='+':
			P[0][i][8]=True
		if St[i]==')':
			P[0][i][12]=True	
		if St[i]=='.':
			P[0][i][9]=True
		if St[i]=='*':
			P[0][i][10]=True
	#print P
	for i in range(1,n):										#Length of span
		for j in range(n-i):									#Start of span
			for k in range(i):								#Partition of span
				for pd in prodcn:
					if (P[k][j][pd[1]]==True and P[i-k-1][j+k+1][pd[2]]==True):
						P[i][j][pd[0]]=True
						#print i, j, k, pd[0], pd[1], pd[2]

	#print P
	if P[n-1][0][0]==True:
		return True										#S is member of language
	return False											#S is not member of language


def automaton(exp):				#Constructs and returns an automaton from the input regular expression
	alphabets=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	bracket_open=[]
	bracket_close=[]
	reg_exp_arr=[]
	reg_exp_cp=[]
	for c in exp:
		reg_exp_arr.append(c)
		reg_exp_cp.append(c)
	for i in range(len(exp)):
		if exp[i]=='(':
			bracket_open.append(i)
		if exp[i]==')':
			bracket_close.append([bracket_open.pop(),i])
	n_b=len(bracket_close)
	i=0
	while i<n_b:
		bracket_open=[]
		bracket_close=[]
		for j in range(len(reg_exp_cp)):
			if reg_exp_cp[j]=='(':
				bracket_open.append(j)
			if reg_exp_cp[j]==')':
				bracket_close.append([bracket_open.pop(),j])
		#print bracket_close
		new=reg_exp_cp[bracket_close[0][0]+1:bracket_close[0][1]]
		#print 'new', new
		if len(new)==2:								#asterate
			if new[0] in alphabets:							#(a*) case
				M_new=asterate(alph(new[0]))
			else:									#(M*) case
				M_new=asterate(new[0])
		elif new[1]=='+':							#union
			if new[0] in alphabets and new[2] in alphabets:				#(a+b) case
				M_new=union(alph(new[0]),alph(new[2]))
			if new[0] in alphabets and new[2] not in alphabets:			#(a+M) case
				M_new=union(alph(new[0]),new[2])
			if new[0] not in alphabets and new[2] in alphabets:			#(M+a) case
				M_new=union(new[0],alph(new[2]))
			if new[0] not in alphabets and new[2] not in alphabets:			#(M1+M2) case
				M_new=union(new[0],new[2])				
		else:									#concatenation
			if new[0] in alphabets and new[2] in alphabets:				#(a.b) case
				M_new=concat(alph(new[0]),alph(new[2]))
			if new[0] in alphabets and new[2] not in alphabets:			#(a.M) case
				M_new=concat(alph(new[0]),new[2])
			if new[0] not in alphabets and new[2] in alphabets:			#(M.a) case
				M_new=concat(new[0],alph(new[2]))
			if new[0] not in alphabets and new[2] not in alphabets:			#(M1.M2) case
				M_new=concat(new[0],new[2])
		#print reg_exp_cp
		exp_M=reg_exp_cp[:bracket_close[0][0]]
		#print exp_M		
		exp_M.append(M_new)
		#print exp_M
		exp_M=exp_M+reg_exp_cp[bracket_close[0][1]+1:]
		#print exp_M
		#print reg_exp_cp
		reg_exp_cp=exp_M
		i+=1
	#print reg_exp_cp[0]
	#print union(alph('a'),alph('b'))
	return reg_exp_cp[0]

reg_exp=raw_input("Enter the Regular Exp: ")

if valid(reg_exp)==False:
	print "Wrong Expression"
else:
	n_test_cases=int(raw_input("Number of test cases: "))
	test_cases_strings=[]
	for j in range(n_test_cases):
		test_cases_strings.append(raw_input())
	M=automaton(reg_exp)
	for s in test_cases_strings:
		string=[]
		for c in s:
			string.append(c)
		if check(string,M,0):
			print "Yes"
		else:
			print "No"
	

