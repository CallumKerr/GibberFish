a,b,c,d,e,f = 10,11,12,13,14,15

codepage = []
for i in range(16):
	codepage.append([])
	for i2 in range(16):
		codepage[i].append('N/A')
		
for i in range(32,127):
	codepage[i//16][i%16] = chr(i)
	
#-----------------------------------------------------------------------

def s(loc, symb):
	codepage[eval(loc[0])][eval(loc[1])] = symb

quoteadd = lambda x: "'{}'".format(x)
tablerows = lambda y, z: list(map(quoteadd, y)) + [str(z)]
tablecols = '\t'.join(list(map(lambda x: str(x),range(16))))
comp = lambda: print(tablecols + '\n\n' + '\n\n'.join(['\t'.join(sublist) for sublist in list(map(tablerows, codepage, range(16)))]))