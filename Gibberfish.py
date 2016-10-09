import random

#Constants, currently defunct for 5-bit GibberFish
c_numpush = "0123456789abcdef"
c_stackmanip = ":~$@{}rl[]"
c_string = '"\''
c_io = "ion"
c_directs = { ">" : (1,0), "<" : (-1,0), "v" : (0,1), "^" : (0,-1)}
c_arith = "+-*%"
c_comps = "=()"
c_miscmove = "x!?."
c_misc = "&gp"
c_mirrors = {
    "|" : lambda x,y:(-x, y),
    "_" : lambda x,y:(x, -y),
    "#" : lambda x,y:(-x,-y),
    "/" : lambda x,y:(-y,-x),
    "\\": lambda x,y:( y, x)
    }
c_decodedict = {
    } #Currently empty dictionary for decoding symbolic GibberFish into binary format for execution. Will be done when codepage is complete
c_valuedict = {i : j, for j, i in c_decodedict.items()} #Reversed version of above dictionary for getting symbolic code representations from binaries


#Functions

class progrun:
    
    def __init__(self, code):
        self.v_code = code
		self.v_map = 0
        self.v_stack = []
        self.v_stackstack = [self.v_stack]
        self.v_registers = [None]
        self.v_stringmode = None
        self.v_pos = [-1, 0]
        self.v_direct = (1, 0)
        
        self.v_dictx = 0
        self.v_dicty = 0
        self.v_codefield = {}
        for i in self.v_code:
            if i != '\n':
                self.v_codefield[(self.v_dictx,self.v_dicty)] = i
                self.v_dictx += 1
            else:
                self.v_dictx = 0
                self.v_dicty += 1

    def f_mov(self):
        try:
            self.v_pos[0] += self.v_direct[0]
            self.v_pos[1] += self.v_direct[1]
            self.v_codefield[tuple(self.v_pos)]
        except KeyError:
            pass #needs work
        
    def f_push(self, value):
        self.v_stack.append(value)

    def f_pop(self):
        self.v_stack.pop()
        return

    def f_rshift(self, l):
        l.insert(0, l.pop())

    def f_lshift(self, l):
        l.append(l.pop(0))

    def f_exe(self, cmd):
        if cmd is 29:
			self.v_map = 0
			
		elif cmd is 28:
			self.v_map = 1
		
		elif cmd is 27:
			self.v_map = 2
			
		elif map == 0:
			pass #map 0 cmds here
		
		elif map == 1:
			pass #map 1 cmds here
			
		elif map == 2:
			pass #map 2 cmds here

        else:
            raise Exception("Invalid Instruction", cmd)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("script", type=argparse.FileType("rb"))
    filetype = parser.add_mutually_exclusive_group(required=True)
    filetype.add_argument("-e","--e", action="store_true")
    filetype.add_argument("-d","--d", action="store_true",
                          help="specify whether file is encoded in GibberFish symbolic form (-d/--d) or binary form (-e/--e)")
    

    opts = parser.add_argument_group("options")
    opts.add_argument("-s","--s", action="append", metavar="<string>", dest="stack")
    opts.add_argument("-n","--n", type=float, nargs="+", action="append",
                      metavar="<number>", dest="stack", help="initialize starting stack values")

    arguments = parser.parse_args()

    if arguments.e:
        codenum = int.from_bytes(arguments.script.read(), byteorder = 'big')
        code = [codenum >> i & 31 for i in range(0, len(bin(codenum)) - 2, 5)]
        
    else:
        filecode = arguments.script.read()
        try:
            code = []
            for i in filecode:
                code.append(decodedict[i])
        except KeyError:
            print('{} is not valid in symbolic GibberFish!'.format(i))

    #execution to go here
