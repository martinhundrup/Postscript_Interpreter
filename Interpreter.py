# CptS 355 - Spring 2024 Assignment 5
# Martin Hundrup

from collections import deque
import re
def tokenize(s):
    return re.findall("/?[a-zA-Z()][a-zA-Z0-9_()]*|[-]?[0-9]+|}|{|%.*|[^ \t\n]", s)

opstack = []  #assuming top of the stack is the end of the list

def opPop():
    # opPop should return the popped value.
    # The pop() function should call opPop to pop the top value from the opstack, but it will ignore the popped value.
    if len(opstack) == 0: # can't pop when nothing in stack
        return None; 
    return opstack.pop();

def groupArray():
    # ensure a '[' is in the stack
    if not '[' in opstack:
        return False
    # traverse opstack until the '['
    i = opPop()
    L = [']']
    while (i != '['):
        L.append(i)
        i = opPop()
    # return the accumulated array WITH '[' ']' appended
    L.append('[')
    return L[::-1]
    
def opPush(value):
    if value == None:
        return
    n = None
    if value == '[': # start of an array, add stuff like normal
        opstack.append(value)
        return
    elif value == ']': # end of array; we need to check that a '[' is present in the stack, and group all of the items together
        L = groupArray()
        if L == False: # improper stack state
            print('no matching [ found')
        else:
            opstack.append(L)
        return                    
    elif isinstance(value, str) and value[0] != '/':
        if value[0] == '(' and value[-1] == ')': # push strings without any further lookup
            opstack.append(value)
            return
        n = lookup(value)
        if isinstance(n, list): # a var or function was called
            if n[0] == '[': # regular array
                opstack.append(n)
                return
            else: # code array
                for it in n:
                    opPush(it)   
                return         
        if n == None:
            if value == 'add':
                add()
                return
            elif value == 'sub':
                sub()
                return
            elif value == 'mul':
                mul()
                return
            elif value == 'div':
                div()
                return
            elif value == 'mod':
                mod()
                return
            elif value == 'roll':
                roll()
                return
            elif value == 'pop':
                pop()
                return
            elif value == '=':
                print(opPop())
                return        
            elif value == 'stack':
                stack()
                return
            elif value == 'def':
                psDef()
                return
            elif value == 'dict':
                psDict()
                return
            elif value == 'end':
                end()
                return
            elif value == 'eq':
                eq()
                return
            elif value == 'lt':
                lt()
                return  
            elif value == 'ge':
                ge()
                return
            elif value == 'le':
                le()
                return
            elif value == 'gt':
                gt()
                return
            elif value == 'length':
                length()
                return
            elif value == 'get':
                get()
                return
            elif value == 'getinterval':
                getinterval()
                return
            elif value == 'put':
                put()
                return
            elif value == 'dup':
                dup()
                return
            elif value == 'copy':
                copy()
                return
            elif value == 'clear':
                clear()
                return
            elif value == 'exch':
                exch()
                return
            elif value == 'begin':
                begin()
                return    
            elif value == 'if':
                psIf()
                return         
            elif value == 'ifelse':
                psIfelse()
                return 
            elif value == 'for':
                psFor()
                return
            elif value[0] != '(' or value[-1] != ')': # make sure its a valid ps string
                print(value + ': name not recognized')
                return     
    if n == None:
        opstack.append(value)
    else: # we found a variable, append the value to the stack
        opstack.append(n)

dictstack = []  #assuming top of the stack is the end of the list

# now define functions to push and pop dictionaries on the dictstack, to
# define name, and to lookup a name

def dictPop():
    # dictPop pops the top dictionary from the dictionary stack.
    if len(dictstack) == 0:
        return None;
    return dictstack.pop();

def dictPush(d):
    if d == None:
        return
    dictstack.append(d);

def define(name, value):
    #add name:value pair to the top dictionary in the dictionary stack.
    #Keep the '/' in the name constant.
    d = dictPop()
    #print(d)
    if d == None: # nothing in dictstack yet
        d = {name:value}
    else:
        d[name] = value
    dictPush(d)

# used to recursively find the inner most definition of a value in the current dict
def lookupHelper(name, count, d):
    for it in d:
        if it == name:
            return lookupHelper(d[name], count + 1, d)
    if count == 0:
        return None
    else:
        return name

def lookup(name):
    # return the value associated with name
    # What is your design decision about what to do when there is no definition for “name”? If “name” is not defined, your program should not break, but should give an appropriate error message.
    # loop through each dictionary starting with the topmost
    i = len(dictstack) - 1
    if i < 0: # nothing in dictstack, don't bother looking
        return None
    x = 0
    if isinstance(name, str):
        name = '/' + name # append slash to beginning
    while (i >= 0):
        x = lookupHelper(name, 0, dictstack[i])
        if x != None:
            if isinstance(x, str):
                x = '/' + x
            else:
                return x
            name = x        
        i -= 1 # decrement i
    if isinstance(x, str):
        x = x[1:]
    return x

def add():
    y = opPop()
    x = opPop()
    try:
        if isinstance(x, str) and isinstance(y, str):
            raise Exception()  # ps does not support string concatenation
        result = x + y
        opPush(result)
    except: # put popped items back on stack
        opPush(x)
        opPush(y)
        print('add: invalid stack operands')

def sub():
    y = opPop()
    x = opPop()
    try:
        result = x - y
        opPush(result)
    except: # put popped items back on stack
        opPush(x)
        opPush(y)
        print('sub: invalid stack operands')

def mul():
    y = opPop()
    x = opPop()
    try:
        if isinstance(x, str) or isinstance(y, str):
            raise Exception()  # ps does not support string multiplication
        result = x * y
        opPush(result)
    except: # put popped items back on stack
        opPush(x)
        opPush(y)
        print('mul: invalid stack operands')

def div():
    y = opPop()
    x = opPop()
    try:
        result = x / y
        opPush(result)
    except: # put popped items back on stack
        opPush(x)
        opPush(y)
        print('div: invalid stack operands')

def mod(): # why can python do modulus with floating points??????
    y = opPop()
    x = opPop()
    if not isinstance(y, int) or not isinstance(x, int): # put popped items back on stack
        opPush(x)
        opPush(y)
        print('mod: invalid stack operands')
    else:
        result = x % y
        opPush(result)
                
def eq():
    y = opPop()
    x = opPop()
    if x == None or y == None: # eq doesn't work when one item DNE
        opPush(x)
        opPush(y)
        print('eq: invalid stack operands')
        return
    else:
        opPush(x == y)

def lt():
    x = opPop()
    y = opPop()
    try:
        result = y < x
        opPush(result)
    except:
        opPush(x)
        opPush(y)
        print('lt: invalid stack operands')

def le():
    x = opPop()
    y = opPop()
    try:
        result = y <= x
        opPush(result)
    except:
        opPush(x)
        opPush(y)
        print('le: invalid stack operands')

def gt():
    x = opPop()
    y = opPop()
    try:
        result = y > x
        opPush(result)
    except:
        opPush(x)
        opPush(y)
        print('gt: invalid stack operands')

def ge():
    x = opPop()
    y = opPop()
    try:
        result = y >= x
        opPush(result)
    except:
        opPush(x)
        opPush(y)
        print('ge: invalid stack operands')

def length():
    s = opPop()
    if isinstance(s, str): # only push if s is a string
        opPush(len(s) - 2) # -2 ignores the ()
    elif isinstance(s, list):
        opPush(len(s))
    else:
        opPush(s)
        print('length: invalid stack operands')

def get():
    index = opPop()
    s = opPop()
    if (not isinstance(s, list) and not isinstance(s, str)) or not isinstance(index, int):
        opPush(s)
        opPush(index)
        print('get: invalid stack operands')
    else: 
        if isinstance(s, str):
            if (index + 2 >= len(s)):
                opPush(s)
                opPush(index)
                print('get: invalid stack operands')
            else:
                opPush(ord(s[index + 1])) # +1 ignores the starting (
        elif isinstance(s, list) and s[0] == '[':
            if (index + 2 >= len(s)):
                opPush(s)
                opPush(index)
                print('get: invalid stack operands')
            else:
                opPush(s[index + 1])
        else:
            if (index >= len(s)):
                opPush(s)
                opPush(index)
                print('get: invalid stack operands')
            else:
                opPush(s[index])

def getinterval():
    length = opPop()
    index = opPop()
    s = opPop()
    if (not isinstance(s, str) and not isinstance(s, list)) or not isinstance(index, int) or not isinstance(length, int):
        # one of types don't match
        opPush(s)
        opPush(index)
        opPush(length)
        print('getinterval: invalid stack operands')
    else:
        if isinstance(s, str):
            if length + index > len(s) - 2: # trying to read out of bounds, -2 ignores ()
                opPush(s)
                opPush(index)
                opPush(length)
                print('invalid stack operands')
            else:
                opPush('(' + s[index + 1:length + index + 1] + ')')
        else:
            if length + index > len(s):
                opPush(s)
                opPush(index)
                opPush(length)
                print('invalid stack operands')
            else:
                opPush(s[index:length + index])

def put():
    asciival = opPop()
    index = opPop()
    s = opPop() # the string check
    org = s
    success = False
    
    if isinstance(s, str) and isinstance(asciival, int) and isinstance(index, int) and index < len(s) - 2:
        s = s[0:index + 1] + chr(asciival) + s[index + 2:]
        success = True
    elif isinstance(s, list) and isinstance(index, int) and index < len(s):
        s = s[0:index] + [asciival] + s[index + 1:]
        success = True
    else:
        opPush(s) # invalid stack for put
        opPush(index)
        opPush(asciival)
        print('put: invalid stack operands')        
        return
    if success:
        for i in range(len(opstack)):
            if id(org) == id(opstack[i]):
                opstack[i] = s
        for i in range(len(dictstack)):
            for it in dictstack[i]:
                if id(dictstack[i][it]) == id(org):
                    dictstack[i][it] = s

def dup():
    x = opPop()
    opPush(x)
    opPush(x)

def copy():
    x = opPop()
    if not isinstance(x, int) or x > len(opstack):
        opPush(x) # top was not an integer or too large
        print('copy: invalid stack operands')
    else:
        queue = [None] * (x * 2) # create empty list with 2x items
        i = 0
        while (i < x):
            queue[i] = opPop()
            queue[i + x] = queue[i]
            i += 1
        i = 0
        while (i < x * 2):
            opPush(queue.pop())
            i += 1

def pop():
    opPop()

def clear():
    x = opPop()
    while not x == None:
        x = opPop()

def exch():
    x = opPop()
    y = opPop()
    if x == None or y == None: # not enough items for exchange
        opPush(y)
        opPush(x)
        print('exch: invalid stack operands')
    else:
        opPush(x)
        opPush(y)

def roll():
    i = opPop()
    n = opPop()
    # if either value aren't integers or n is negative or too large put back on stack
    if not isinstance(i, int) or not isinstance(n, int) or n < 0 or n > len(opstack):
        opPush(n)
        opPush(i)
        print('roll: invalid stack operands')
    else: # see if i is negative to determine course of action
        if i < 0:
            i *= -1
            while i > 0:
                i -= 1
                index = len(opstack) - n
                x = opstack[index]
                del opstack[index]
                opPush(x)
        else:
            while i > 0:
                i -= 1
                index = len(opstack) - n
                opstack.insert(index, opPop())
        
def stack():
    i = len(opstack)
    while (i > 0):
        i -= 1
        if isinstance(opstack[i], list): # change print depending on whether it's code or reg array
            s = printHelper(opstack[i])
            if s[0] == ' ':
                s = s[1:]
            else:
                print(s)       
        else:
            print(opstack[i])
    
def printHelper(item):
    s = ''
    if isinstance(item, list):
        if item[0] != '[':
            s += '{'
        for it in item:
            if isinstance(it, list):
                s += printHelper(it)
            else:
                if str(it) == '[':
                    s += '['
                elif str(it) == ']':
                    if s[-1] == ' ':
                        s = s[:-1]
                    s += ']'
                elif s[-1] == ']':
                    s += ' ' + str(it) + ' '
                else:
                    s += str(it) + ' '
        if item[0] != '[':
            if s[-1] == ' ':
                s = s[:-1]
            s += '} '
        return s
    else:
        return str(item) + ' '

def psDict():
    # step 1: pop an integer off the stack
    x = opPop()
    if not isinstance(x, int): # case: not an integer
        opPush(x)
        print('dict: invalid stack operands')
    else: # step 2: push an emtpy dictionary onto operator stack
        opPush({})

def begin():
    # step 1: pop a dictionary off the stack
    x = opPop()
    if not isinstance(x, dict): # case: not a dict
        opPush(x)
        print('begin: invalid stack operands')
    else: # step 2: push the dict onto the dict stack
        dictPush(x)

def end():
    x = dictPop()
    if x == None:
        print('end: invalid stack operands')

def psDef():
    #Your psDef function should pop the name and value from operand stack and
    #call the “define” function.
    value = opPop()
    name = opPop()
    if not isinstance(name, str) or name[0] != '/': # case: not a valid name, put back onto op stack
        opPush(name)
        opPush(value)
        print('def: invalid stack operands')
    else: # call define
        define(name, value)

def psIf():
    codeArr = opPop()
    con = opPop()
    if not isinstance(con, bool) or not isinstance(codeArr, list): # improper stack
        opPush(con)
        opPush(codeArr)
        print("if: invalid stack operands")
    elif con == True: # execute code array
        for it in codeArr:
            opPush(it) # recursive statement: psIf was called by opPush
            
def psIfelse():
    codeFalse = opPop()
    codeTrue = opPop()
    con = opPop()
    if not isinstance(con, bool) or not isinstance(codeTrue, list) or not isinstance(codeFalse, list): # improper stack
        opPush(con)
        opPush(codeTrue)
        opPush(codeFalse)
        print("ifelse: invalid stack operands")
    elif con == True: # execute code array
        for it in codeTrue:
            opPush(it) # recursive statement: psIfelse was called by opPush
    else:
        for it in codeFalse:
            opPush(it) # recursive statement: psIfelse was called by opPush
            
def psFor():
    code = opPop()
    final = opPop()
    incr = opPop()
    init = opPop()
    
    if not isinstance(code, list) or not isinstance(final, int) or not isinstance(incr, int) or not isinstance(init, int):
        # invalid stack, put everything back
        opPush(init)
        opPush(incr)
        opPush(final)
        opPush(code)
        print("for: invalid stack operands")
    else:
        # decrement array
        if incr < 0:
            while (init >= final):
                opPush(init)
                for it in code:
                    opPush(it) # recursive statement: psFor was called by opPush
                init += incr
        # increment array
        elif incr > 0:
            while (init <= final):
                opPush(init)
                for it in code:
                    opPush(it) # recursive statement: psFor was called by opPush
                init += incr
  
def groupMatching2(it):
    res = []
    for c in it:
        if c == '}':
            return res
        elif c =='{':
            # Note how we use a recursive call to group the tokens inside the
            # inner matching parenthesis.
            # Once the recursive call returns the code array for the inner
            # paranthesis, it will be appended to the list we are constructing
            # as a whole.
            res.append(groupMatching2(it))
        else:
            try:
                c = int(c)
            except:
                if c == 'true':
                    c = True
                elif c == 'false':
                    c = False
            res.append(c)
    return False

def groupMatchingArray(it):
    res = []
    for c in it:
        if c == ']':
            return res
        elif c =='[':
            res.append(groupMatchingArray(it))
        else:
            try:
                c = int(c)
            except:
                if c == 'true':
                    c = True
                elif c == 'false':
                    c = False
            res.append(c)
    return False

# Properly nested parentheses are arranged into a list of properly nested lists.
def parse(L):
    res = []
    it = iter(L)
    for c in it:
        if c=='}':  #non matching closing paranthesis; return false since there is
                    # a syntax error in the Postscript code.
            print("no matching { found")
            return False
        elif c=='{':
            n = groupMatching2(it)
            if not n == False:
                res.append(n)
            else:
                print('no matching } found')
        else:
            try:
                c = int(c)
            except:
                if c == 'true':
                    c = True
                elif c == 'false':
                    c = False
            res.append(c)
    return res    

def interpretSPS(code): # code is a code array ex [1, 1, add]
    for it in code:
        val = lookup(it)
        if isinstance(val, list): # psDef lead to an array
            if val[0] == '[': # case 1: regular array
                for it2 in val:
                    opPush(it2)
            else: # case 2: code array
                for it2 in val:
                    # note: nested code arrays are not ran
                    opPush(it2)
        elif not val == None:
            opPush(val)
        else:
            opPush(it)

def interpreter(s): # s is a string
    n = parse(tokenize(s))
    if n == False:
        print('error: invalid input')
    else:
        interpretSPS(n)
        
#clear opstack and dictstack
def clearAll():
    del opstack[:]
    del dictstack[:]
    
# runs a terminal similar to ghostscript
def runInterpreter():
    while True:
        s = input("SPS<" + str(len(opstack)) + '>')
        if s == 'quit': # reserved name
            return
        interpreter(s)
        
if __name__=="__main__": 
    runInterpreter() 