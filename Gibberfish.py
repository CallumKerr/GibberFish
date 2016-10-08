import random

#Constants
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
c_nummap = {
    } #worthless until code page is at least partially done
c_charmap = {i : j for j, i in c_nummap.items()} #same as above
c_decodedict = {
    } #another useless empty dict for now


#Functions

class progrun:
    
    def __init__(self, code):
        self.v_code = code
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
        if self.v_stringmode != None and self.v_stringmode != cmd:
            self.f_push(c_nummap[cmd])
        
        elif cmd in c_string:
            if self.v_stringmode == None:
                self.v_stringmode = cmd
            else:
                self.v_stringmode = None
        
        elif cmd in c_numpush:
            self.f_push(c_nummap[cmd])

        elif cmd in c_directs:
            self.v_direct = c_directs[cmd]

        elif cmd in c_mirrors:
            self.v_direct = c_mirrors[cmd](*self.v_direct)

        elif cmd in c_miscmove:
            if cmd is 'x':
                self.v_direct = random.choice(list(c_directs.values()))

            elif cmd is '!':
                self.f_mov() #keep an eye on this

            elif cmd is '?':
                if self.v_stack.pop() == 0:
                    self.f_mov #same thing as above

            elif cmd is '.':
                self.v_pos[1], self.v_pos[0] = self.v_stack.pop(), self.v_stack.pop()

        elif cmd in c_arith:
            temp1, temp2 = self.v_stack.pop(), self.v_stack.pop()
            exec("self.f_push(temp2{}temp1)".format(cmd))

        elif cmd is ',':
            temp1, temp2 = self.v_stack.pop(), self.v_stack.pop()
            self.f_push(temp2/temp1)

        elif cmd in c_stackmanip:
            if cmd is ':':
                self.f_push(self.v_stack[-1])

            elif cmd is '~':
                self.v_stack.pop()

            elif cmd is '$':
                temp1, temp2 = self.v_stack.pop(), self.v_stack.pop()
                self.f_push(temp1)
                self.f_push(temp2)

            elif cmd is '@':
                temp1, temp2, temp3 = self.v_stack.pop(), self.v_stack.pop(), self.v_stack.pop()
                self.f_push(temp1)
                self.f_push(temp3)
                self.f_push(temp2)

            elif cmd is 'r':
                self.v_stack.reverse()

            elif cmd is 'l':
                self.f_push(len(self.v_stack))

            elif cmd is '}':
                self.f_rshift(self.v_stack)

            elif cmd is '{':
                self.f_lshift(self.v_stack)

            elif cmd is '[':
                temp1 = int(self.v_stack.pop())
                if temp1:
                    self.v_stackstack[-1], newstack = self.v_stack[:-temp1], self.v_stack[-temp1:]
                else:
                    self.v_stackstack[-1], newstack = self.v_stack, []
                self.v_stackstack.append(newstack)
                self.v_stack = newstack
                self.v_registers.append(None)

            elif cmd is ']':
                temp1 = self.v_stackstack.pop()
                self.v_stack = self.v_stackstack[-1] + temp1
                self.v_stackstack[-1] = self.v_stack
                self.v_registers.pop()

        elif cmd in c_comps:
            if cmd is '=':
                temp1, temp2 = self.v_stack.pop(), self.v_stack.pop()
                if temp1 == temp2:
                    self.f_push(1)
                else:
                    self.f_push(0)

            elif cmd is '(':
                temp1, temp2 = self.v_stack.pop(), self.v_stack.pop()
                if temp2 < temp1:
                    self.f_push(1)
                else:
                    self.f_push(0)

            elif cmd is ')':
                temp1, temp2 = self.v_stack.pop(), self.v_stack.pop()
                if temp2 > temp1:
                    self.f_push(1)
                else:
                    self.f_push(0)
                

        elif cmd in c_io:
            pass #unfinished

        elif cmd in c_misc:
            if cmd is '&':
                if self.v_registers[-1] is None:
                    self.v_registers[-1] = self.v_stack.pop()
                else:
                    self.f_push(self.v_registers.pop())
                    self.v_registers.append(None)

            elif cmd is 'g':
                pass #unfinished

            elif cmd is 'p':
                pass #unfinished

        elif cmd is ' ':
            pass

        else:
            raise Exception("Invalid Instruction", cmd)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("script", type=argparse.FileType("rb"))
    filetype = parser.add_mutually_exclusive_group(required=True)
    filetype.add_argument("-e","--e", action="store_true")
    filetype.add_argument("-d","--d", action="store_true",
                          help="specify whether file is encoded in UTF-8 (-d/--d) or Gibberfish code page (-e/--e)")
    

    opts = parser.add_argument_group("options")
    opts.add_argument("-s","--s", action="append", metavar="<string>", dest="stack")
    opts.add_argument("-n","--n", type=float, nargs="+", action="append",
                      metavar="<number>", dest="stack", help="initialize starting stack values")

    arguments = parser.parse_args()

    if arguments.e:
        filecode = arguments.script.read()
        code = []
        try:
            for i in filecode:
                code.append(c_decodedict[filecode[i]])
            code = ''.join(code)
        except KeyError:
            print("The hex value {} is not in the Gibberfish code page!".format(ord(filecode[i].decode())))
        
    else:
        code = arguments.script.read().decode()

    #execution to go here
    #branch test
