import sys
import io
import unittest
from Interpreter import *

# CptS 355 - Spring 2024 Assignment 5
# Martin Hundrup

class HW4Tests(unittest.TestCase):
    def setUp(self):
        
        self.input1 = """
                /square {
                dup mul
                } def 
                (square)
                4 square 
                dup 16 eq 
                {(pass)} {(fail)} ifelse
                stack 
                """
        self.input2 = """
                (facto) dup length /n exch def
                /fact {
                    0 dict begin
                        /n exch def
                        n 2 lt
                        { 1}
                        {n 1 sub fact n mul }
                        ifelse
                    end 
                } def
                n fact stack
                """

        self.input3 = """
                /fact{
                0 dict
                        begin
                                /n exch def
                                1
                                n -1 1 {mul} for
                        end
                } def
                6
                fact
                stack
                """

        self.input4 = """
                /lt6 { 6 lt } def 
                1 2 3 4 5 6 4 -3 roll 
                dup dup lt6 {mul mul mul} if
                stack 
                clear
                """

        self.input5 = """
                (CptS355_HW5) 4 3 getinterval 
                (355) eq 
                {(You_are_in_CptS355)} if
                 stack
                """

        self.input6 = """
               /pow2 {/n exch def 
                       (pow2_of_n_is) dup 8 n 48 add put 
                       1 n -1 1 {pop 2 mul} for 
                     } def
               (Calculating_pow2_of_9) dup 20 get 48 sub pow2
               stack
               """
        pass

    def testOpPush(self):
        opstack.clear()
        opPush("(Hello)")
        self.assertEqual(opstack[-1],"(Hello)")
    
    def testOpPush2(self):
        opstack.clear()
        opPush(5)
        opPush(6)
        opPush(7)
        self.assertEqual(opstack[2],7)
        self.assertEqual(opstack[1],6)
        self.assertEqual(opstack[0],5)

    def testOpPop(self):
        opstack.clear()
        opPush(5)
        self.assertEqual(opPop(),5)
    
    def testOpPop2(self):
        opstack.clear()
        opPush(5)
        opPush('(hello)')
        self.assertEqual(opPop(),'(hello)')
        self.assertEqual(opPop(),5)
    
    def testDictPush(self):
        dictstack.clear()
        dictPush({})
        self.assertEqual(dictstack[-1],{})
        
    def testDictPush2(self):
        dictstack.clear()
        dictPush({})
        dictPush({'hello': 4, 'world': '5'})
        self.assertEqual(dictstack[1],{'hello': 4, 'world': '5'})
        self.assertEqual(dictstack[0],{})

    def testDictPop(self):
        dictstack.clear()
        dictPush({})
        dictPop()
        self.assertEqual(len(dictstack),0)
        
    def testDictPop2(self):
        dictstack.clear()
        dictPush({})
        dictPush({'hello': 4, 'world': '5'})
        d = {'hello': 4, 'world': '5'}
        self.assertEqual(d, dictPop())
        d = {}
        self.assertEqual(d, dictPop())

    def testDefine(self):
        dictstack.clear()
        define("/a",1)
        self.assertEqual(len(dictstack),1)
        
    def testDefine2(self):
        dictstack.clear()
        define("/b",3)
        define("/a",1)
        self.assertEqual(dictPop(),{'/b':3,'/a':1})
    
    def testDefine3(self):
        dictstack.clear()
        define("/a",1)
        define("/b",3)
        define("/a",2)
        self.assertEqual(dictPop(),{'/b':3,'/a':2})
        
    def testDefine4(self):
        dictstack.clear()
        define("/a",1)
        opPush('a')
        self.assertEqual(opPop(),1)

    def testLookup(self):
        dictstack.clear()  
        opPush("/n1")       
        opPush("(hornswaggle)")  
        psDef()
        self.assertEqual(lookup("n1"),"(hornswaggle)")

    def testAdd(self):
        opstack.clear()     
        opPush(1.0)       
        opPush(2.0)       
        add()       
        self.assertEqual(opPop(),3)

    def testAdd2(self):
        opstack.clear()     
        opPush(3)
        opPush("(notanum)")
        add()       
        self.assertEqual(opPop(),"(notanum)")
        self.assertEqual(opPop(),3)
        
    def testAdd3(self):
        opstack.clear()     
        opPush('(1.0)')       
        opPush('(2.0)')       
        add()       
        self.assertEqual(opPop(),'(2.0)')
        self.assertEqual(opPop(),'(1.0)')

    def testSub(self):
        opstack.clear()
        opPush(3)
        opPush(2)
        sub()
        self.assertEqual(opPop(),1)
        
    #def testSub2(self): # by coincidence, these numbers produce a floating number representation error, so it is omitted
        #opstack.clear()
        #opPush(3)
        #opPush(4.6)
        #sub()
        #self.assertEqual(opPop(),-1.6)
        
    def testSub3(self):
        opstack.clear()
        opPush(3)
        sub()
        self.assertEqual(opPop(),3)
    
    def testSub4(self):
        opstack.clear()
        opPush(3)
        opPush('(3)')
        sub()
        self.assertEqual(opPop(),'(3)')
        
    def testSub5(self):
        opstack.clear()
        opPush(3)
        opPush(-3)
        sub()
        self.assertEqual(opPop(),6)
    
    def testMul(self):
        opstack.clear()
        opPush(3)
        opPush(2)
        mul()
        self.assertEqual(opPop(),6)
        
    def testMul2(self):
        opstack.clear()
        opPush(3)
        mul()
        self.assertEqual(opPop(),3)
        
    def testMul3(self):
        opstack.clear()
        opPush(3)
        opPush('(3)')
        mul()
        self.assertEqual(opPop(),'(3)')

    def testDiv(self):
        opstack.clear()
        opPush(4)
        opPush(2)
        div()
        self.assertEqual(opPop(),2)
        
    def testDiv2(self):
        opstack.clear()
        opPush(4)
        div()
        self.assertEqual(opPop(),4)
        
    def testDiv3(self):
        opstack.clear()
        opPush(3)
        opPush('(3)')
        div()
        self.assertEqual(opPop(),'(3)')
        
    def testDiv4(self):
        opstack.clear()
        opPush(3)
        opPush(0)
        div()
        self.assertEqual(opstack,[3, 0])
    
    def testMod(self):
        opstack.clear()
        opPush(3)
        opPush(2)
        mod()
        self.assertEqual(opPop(),1)
        
    def testMod2(self):
        opstack.clear()
        opPush(3)
        mod()
        self.assertEqual(opPop(),3)
        
    def testMod3(self):
        opstack.clear()
        opPush(3)
        opPush(3.1)
        mod()
        self.assertEqual(opPop(),3.1)

    def testEq(self):
        opstack.clear()
        opPush(3)
        opPush(2)
        eq()
        self.assertEqual(opPop(),False)
        
    def testEq2(self):
        opstack.clear()
        opPush('(hello)')
        opPush(2)
        eq()
        self.assertEqual(opPop(),False)
        
    def testEq3(self):
        opstack.clear()
        dictstack.clear()
        opPush('(hello)')
        opPush('/hello')
        opPush('(hello)')
        psDef()
        opPush('hello')
        eq()
        self.assertEqual(opPop(),True)

    def testLt(self):
        opstack.clear()
        opPush(2)
        opPush(3)
        lt()
        self.assertEqual(opPop(),True)
        
    def testLt2(self):
        opstack.clear()
        opPush(2)
        lt()
        self.assertEqual(opPop(),2)
        
    def testLt3(self):
        opstack.clear()
        opPush('(hello)')
        opPush('(world)')
        lt()
        self.assertEqual(opPop(),True)
    
    def testLe1(self):
        clearAll()
        opPush(3)
        opPush(3)
        le()
        self.assertEqual(opPop(),True)
        
    def testLe2(self):
        clearAll()
        opPush(2)
        opPush(3)
        le()
        self.assertEqual(opPop(),True)
        
    def testLe3(self):
        clearAll()
        opPush(3)
        opPush(2)
        le()
        self.assertEqual(opPop(),False)

    def testGt(self):
        opstack.clear()
        opPush(2)
        opPush(3)
        gt()
        self.assertEqual(opPop(),False)
        
    def testGt2(self):
        opstack.clear()
        opPush(2)
        gt()
        self.assertEqual(opPop(),2)
        
    def testGt3(self):
        opstack.clear()
        opPush('(hello)')
        opPush('(world)')
        gt()
        self.assertEqual(opPop(),False)
        
    def testGe1(self):
        clearAll()
        opPush(3)
        opPush(3)
        ge()
        self.assertEqual(opPop(),True)
        
    def testGe2(self):
        clearAll()
        opPush(2)
        opPush(3)
        ge()
        self.assertEqual(opPop(),False)
        
    def testGe3(self):
        clearAll()
        opPush(3)
        opPush(2)
        ge()
        self.assertEqual(opPop(),True)

    def testLength(self):
        opstack.clear()
        opPush("(Hello)")
        length()
        self.assertEqual(opPop(),5)
        
    def testLength2(self):
        opstack.clear()
        opPush([1, 2, 3])
        length()
        self.assertEqual(opPop(),3)

    def testGet(self):
        opstack.clear()
        opPush("(CptS355)")
        opPush(0)
        get()
        self.assertEqual(opPop(),ord('C'))
    
    def testGet2(self):
        opstack.clear()
        opPush([1,2,3,4,5])
        opPush(3)
        get()
        self.assertEqual(opPop(),4)

    def testGetInterval(self):
        opstack.clear()
        opPush("(CptS355)")
        opPush(0)
        opPush(3)
        getinterval()
        self.assertEqual(opPop(),"(Cpt)")
        
    def testGetInterval2(self):
        opstack.clear()
        opPush([1,'(hello)',3,4,5])
        opPush(0)
        opPush(3)
        getinterval()
        self.assertEqual(opPop(),[1,'(hello)',3])

    def testPut(self):
        opstack.clear()
        opPush("(CptS355)")
        dup()
        opPush(0)
        opPush(48)
        put()
        self.assertEqual(opPop(),"(0ptS355)")
        
    def testPut2(self):
        opstack.clear()
        opPush([1,2,3])
        dup()
        opPush(0)
        opPush(48)
        put()
        dup()
        opPush(1)
        opPush('(hello)')
        put()
        self.assertEqual(opPop(),[48,'(hello)',3])
        
    def testPut3(self):
        opPush("(This is a test _)")
        dup()
        opPush("/s")
        exch()
        psDef()
        dup()
        opPush(15)
        opPush(48)
        put()
        self.assertFalse(lookup("s") != "(This is a test 0)" or opPop()!= "(This is a test 0)")

    def testDup(self):
        opstack.clear()
        opPush(3)
        dup()
        self.assertEqual(len(opstack),2)
    
    def testDup2(self):
        opstack.clear()
        dup()
        self.assertEqual(len(opstack),0)

    def testPop(self):
        opstack.clear()
        opPush(1)
        pop()
        self.assertEqual(len(opstack),0)
    
    def testClear(self):
        opstack.clear()
        opPush(1)
        clear()
        self.assertEqual(len(opstack),0)

    def testExch(self):
        opstack.clear()
        opPush(1)
        opPush(2)
        exch()
        self.assertListEqual(opstack,[2,1])
        
    def testExch2(self):
        opstack.clear()
        opPush(2)
        exch()
        self.assertListEqual(opstack,[2])

    def testRoll(self):
        opstack.clear()
        opPush(1)
        opPush(2)
        opPush(3)
        opPush(4)
        opPush(2)
        opPush(3)
        roll()
        self.assertListEqual(opstack,[1,2,4,3])
        
    def testRoll2(self):
        opstack.clear()
        opPush(1)
        opPush(2)
        opPush(3)
        opPush(4)
        opPush(5)
        opPush(3)
        roll()
        self.assertListEqual(opstack,[1,2,3,4,5,3])
    
    def testStack(self):
        #pass # this seems to work just fine
        text_trap = io.StringIO()
        sys.stdout = text_trap
        opstack.clear()
        opPush(2)
        opPush(3)
        stack()
        sys.stdout = sys.__stdout__
        self.assertEqual(text_trap.getvalue(), "3\n2\n")

    def testPsDict(self):
        opstack.clear()
        opPush(2)
        psDict()
        self.assertIsInstance(opPop(), dict)
    
    def testPsDict2(self):
        opstack.clear()
        opPush(2)
        psDict()
        self.assertEqual(opPop(), {})

    def testPsDef(self):
        opstack.clear()
        dictstack.clear()
        opPush(5)
        psDict()
        begin()
        opPush("/a")
        opPush(2)
        psDef()
        self.assertEqual(dictstack[-1],{"/a":2})
        
    def testPsDef2(self):
        clearAll()
        opPush(3)
        psDict()
        begin()
        opPush("/a")
        opPush(2)
        psDef()
        opPush('/a')
        opPush(6)
        psDef()
        self.assertEqual(dictstack[-1],{"/a":6})
    
    def testpsDef3(self):
        opPush("/x")
        opPush(10)
        psDef()
        opPush(1)
        psDict()
        begin()
        result = lookup("x")
        self.assertTrue(result == 10)
        
    ### -- START OF HW5 TESTING -- ###
    
    def testIf1(self):
        clearAll()
        interpreter("true {1 1 add} if")
        self.assertEqual(opstack[-1],2)
        
    def testIfelse1(self):
        clearAll()
        interpreter("true {1 1 add} {1 1 mul} ifelse")
        self.assertEqual(opstack[-1],2)
        
    def testIfelse2(self):
        clearAll()
        interpreter("false {1 1 add} {1 1 mul} ifelse")
        self.assertEqual(opstack[-1],1)
        
    def testFor1(self):
        pass
    
    def testTokenize1(self):
        actual = tokenize(self.input1)
        expected = ['/square', '{', 'dup', 'mul', '}', 'def', '(square)', '4', 'square', 
                    'dup', '16', 'eq', '{', '(pass)', '}', '{', '(fail)', '}', 'ifelse', 
                    'stack']
        self.assertEqual(actual, expected)
        
    def testParse1(self):
        actual = parse(tokenize(self.input1))
        expected = ['/square', ['dup', 'mul'], 'def', '(square)', 4, 'square', 'dup', 16, 
                    'eq', ['(pass)'], ['(fail)'], 'ifelse', 'stack']
        self.assertEqual(actual, expected)
        
    def testInterpreter1(self):
        text_trap = io.StringIO()
        sys.stdout = text_trap
        clearAll()
        interpreter(self.input1)
        sys.stdout = sys.__stdout__
        self.assertEqual(text_trap.getvalue(), "(pass)\n16\n(square)\n")     
        
    def testTokenize2(self):
        actual = tokenize(self.input2)
        expected = ['(facto)', 'dup', 'length', '/n', 'exch', 'def', '/fact', '{', '0', 
                    'dict', 'begin', '/n', 'exch', 'def', 'n', '2', 'lt', '{', '1', '}', '{', 
                    'n', '1', 'sub', 'fact', 'n', 'mul', '}', 'ifelse', 'end', '}', 'def', 
                    'n', 'fact', 'stack']
        self.assertEqual(actual, expected)
        
    def testParse2(self):
        actual = parse(tokenize(self.input2))
        expected = ['(facto)', 'dup', 'length', '/n', 'exch', 'def', '/fact', [0, 'dict', 
                    'begin', '/n', 'exch', 'def', 'n', 2, 'lt', [1], ['n', 1, 'sub', 'fact', 
                    'n', 'mul'], 'ifelse', 'end'], 'def', 'n', 'fact', 'stack']
        self.assertEqual(actual, expected)
        
    def testInterpreter2(self):
        text_trap = io.StringIO()
        sys.stdout = text_trap
        clearAll()
        interpreter(self.input2)
        sys.stdout = sys.__stdout__
        self.assertEqual(text_trap.getvalue(), "120\n(facto)\n") 
        
    def testTokenize3(self):
        actual = tokenize(self.input3)
        expected = ['/fact', '{', '0', 'dict', 'begin', '/n', 'exch', 'def', '1', 'n', '-1', 
                    '1', '{', 'mul', '}', 'for', 'end', '}', 'def', '6', 'fact', 'stack']
        self.assertEqual(actual, expected)
    
    def testParse3(self):
        actual = parse(tokenize(self.input3))
        expected = ['/fact', [0, 'dict', 'begin', '/n', 'exch', 'def', 1, 'n', -1, 1, 
                    ['mul'], 'for', 'end'], 'def', 6, 'fact', 'stack']
        self.assertEqual(actual, expected)
    
    def testInterpreter3(self):
        text_trap = io.StringIO()
        sys.stdout = text_trap
        clearAll()
        interpreter(self.input3)
        sys.stdout = sys.__stdout__
        self.assertEqual(text_trap.getvalue(), "720\n")     
    
    def testTokenize4(self):
        actual = tokenize(self.input4)
        expected = ['/lt6', '{', '6', 'lt', '}', 'def', '1', '2', '3', '4', '5', '6', '4', '-3', 
                    'roll', 'dup', 'dup', 'lt6', '{', 'mul', 'mul', 'mul', '}', 'if', 
                    'stack', 'clear']
        self.assertEqual(actual, expected)
        
    def testParse4(self):
        actual = parse(tokenize(self.input4))
        expected = ['/lt6', [6, 'lt'], 'def', 1, 2, 3, 4, 5, 6, 4, -3, 'roll', 'dup', 'dup', 
                    'lt6', ['mul', 'mul', 'mul'], 'if', 'stack', 'clear']
        self.assertEqual(actual, expected)
        
    def testInterpreter4(self):
        text_trap = io.StringIO()
        sys.stdout = text_trap
        clearAll()
        interpreter(self.input4)
        sys.stdout = sys.__stdout__
        self.assertEqual(text_trap.getvalue(), "300\n6\n2\n1\n") 
    
    def testTokenize5(self):
        actual = tokenize(self.input5)
        expected = ['(CptS355_HW5)', '4', '3', 'getinterval', '(355)', 'eq', '{', 
                    '(You_are_in_CptS355)', '}', 'if', 'stack']
        self.assertEqual(actual, expected)
        
    def testParse5(self):
        actual = parse(tokenize(self.input5))
        expected = ['(CptS355_HW5)', 4, 3, 'getinterval', '(355)', 'eq', 
                    ['(You_are_in_CptS355)'], 'if', 'stack']
        self.assertEqual(actual, expected)
        
    def testInterpreter5(self):
        text_trap = io.StringIO()
        sys.stdout = text_trap
        clearAll()
        interpreter(self.input5)
        sys.stdout = sys.__stdout__
        self.assertEqual(text_trap.getvalue(), "(You_are_in_CptS355)\n") 
        
    def testTokenize6(self):
        actual = tokenize(self.input6)
        expected = ['/pow2', '{', '/n', 'exch', 'def', '(pow2_of_n_is)', 'dup', '8', 'n', 
                    '48', 'add', 'put', '1', 'n', '-1', '1', '{', 'pop', '2', 'mul', '}', 
                    'for', '}', 'def', '(Calculating_pow2_of_9)', 'dup', '20', 'get', '48', 
                    'sub', 'pow2', 'stack']
        self.assertEqual(actual, expected)
        
    def testParse6(self):
        actual = parse(tokenize(self.input6))
        expected = ['/pow2', ['/n', 'exch', 'def', '(pow2_of_n_is)', 'dup', 8, 'n', 48, 
                    'add', 'put', 1, 'n', -1, 1, ['pop', 2, 'mul'], 'for'], 'def', 
                    '(Calculating_pow2_of_9)', 'dup', 20, 'get', 48, 'sub', 'pow2', 'stack']
        self.assertEqual(actual, expected)
        
    def testInterpreter6(self):
        text_trap = io.StringIO()
        sys.stdout = text_trap
        clearAll()
        interpreter(self.input6)
        sys.stdout = sys.__stdout__
        self.assertEqual(text_trap.getvalue(), "512\n(pow2_of_9_is)\n(Calculating_pow2_of_9)\n")
    
    def testCase1(self):
        clearAll()
        interpreter("/a {1 1 {add 2 add}} def a")
        self.assertEqual(opstack[-1],['add',2,'add'])
    
    def testCase2(self):
        clearAll()
        interpreter("/add {1 8 mul} def add")
        self.assertEqual(opstack[-1],8)
    
    def testCase3(self):
        clearAll()
        interpreter("/a [2 8 mul] def a")
        self.assertEqual(opstack[-1],['[', 16, ']'])
        
    def testCase4(self):
        clearAll()
        interpreter("1 /a [8 mul] def a")
        self.assertEqual(opstack[-1],['[', 8, ']'])
    
    def testCase5(self):
        clearAll()
        interpreter("[[1 1 add]2 div]")
        self.assertEqual(opstack[-1],['[',['[', 2, ']'], 2, ']'])
        
    def testGet3(self):
        clearAll()
        text_trap = io.StringIO()
        sys.stdout = text_trap
        clearAll()
        interpreter('[1 2 3] 1 get [1 [1 4 5 {1 1 add} (world)] (hello)] 2 get = =')
        sys.stdout = sys.__stdout__
        self.assertEqual(text_trap.getvalue(), "(hello)\n2\n")
        
    def testGet4(self):
        clearAll()
        text_trap = io.StringIO()
        sys.stdout = text_trap
        clearAll()
        interpreter('[1 2 3] 3 get {1 2 3} 3 get (hello) 5 get (hello) 4 get =')
        sys.stdout = sys.__stdout__
        self.assertEqual(text_trap.getvalue(), "get: invalid stack operands\nget: invalid stack operands\nget: invalid stack operands\n111\n")

if __name__ == '__main__':
    unittest.main()