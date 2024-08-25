# Postscript Interpreter

### Outline
1. [Overview](#overview)
2. [How to use](#how-to-use)
3. [Unit Testing](#unit-testing)
4. [Supported commands](#supported-commands)  
    - [add](#add)
    - [begin](#begin)
    - [clear](#clear)
    - [copy](#copy)
    - [def](#def)
    - [dict](#dict)
    - [div](#div)
    - [dup](#dup)
    - [end](#end)
    - [eq](#eq)
    - [exch](#exch)
    - [for](#for)
    - [ge](#ge)
    - [get](#get)
    - [getinterval](#getinterval)
    - [gt](#gt)
    - [if](#if)
    - [ifelse](#ifelse)
    - [length](#length)
    - [le](#le)
    - [lt](#lt)
    - [mod](#mod)
    - [mul](#mul)
    - [pop](#pop)
    - [put](#put)
    - [roll](#roll)
    - [stack](#stack)
    - [sub](#sub)
    - [=](#)

## Overview
This project was made for CPT_S 355 at Washington State University (WSU) under proffessor Jeremy Thompson. 
The application was made in python, and aims to mimic [ghostscript](https://www.ghostscript.com/), a postscript interpreter. Not all commands from postscript, for a list of supported commands, please see [supported commands](#supported-commands).
<br>
<br>
This simplified PostScript language (SPS) interpreter operates as a stack-based language, where commands and operands are processed using a last-in, first-out (LIFO) stack structure. Users can input values or commands that manipulate the stack, such as arithmetic operations (e.g., add, sub), stack management (e.g., dup, pop), and conditional logic (e.g., if, ifelse). The interpreter processes each command by popping the required number of values from the stack, performing the operation, and then pushing the result back onto the stack. Additionally, it supports dictionary operations for defining and retrieving named values, making it versatile for various scripting tasks. 

## How to Use
To start the SPS interpreter, ensure you have a python environment set up, navigate to the location of `Interpreter.py`, and run the command `python .\Interpreter.py`.
<br>
<br>
To use the SPS interpreter, you start by entering values directly, which pushes them onto the stack. For example, entering 5 followed by 10 will place these values on the stack. You can then perform operations like add, which will pop the top two values, add them, and push the result back onto the stack.
<br>
<br>
You can define custom functions using the def command. First, push the procedure code onto the stack using curly braces {}, then define the function with a name. For example, { 5 add } /increment def creates a function called increment that adds 5 to the top stack value. You can call this function by simply entering increment after a value, such as 10 increment, which would result in 15 being pushed onto the stack.

## Unit Testing
In developing this SPS interpreter, extensive unit testing was implemented to ensure the reliability and correctness of the interpreter's core functionalities. The test suite, built using Python's [unittest](https://docs.python.org/3/library/unittest.html) framework, covers a wide range of scenarios, including basic stack operations, dictionary manipulations, arithmetic computations, and the execution of SPS commands. Each function and command is rigorously tested with various inputs to verify the expected outcomes. For example, functions like opPush, opPop, add, sub, mul, and div are tested with typical cases and edge cases to ensure they handle both valid and invalid inputs correctly. Additionally, the test cases also include more complex scenarios, such as defining and calling custom functions within the SPS language, and performing conditional operations using if and ifelse. The comprehensive coverage of unit tests provides confidence that the interpreter behaves as intended across all supported features.

## Supported Commands

### add
Pops the top two values off the stack, adds them together, and pushes the result of the addition back onto the stack.

### begin
Pushes a dictionary onto the dictionary stack, making it the top dictionary.

### clear
Clears the entire stack.

### copy
The copy command duplicates the top n values on the stack and pushes the copies back onto the stack in the same order. The number n is popped from the stack first.

### def
Defines a new name in the current dictionary with the value on the top of the stack.

### dict
Creates a new dictionary object and pushes it onto the stack.

### div
Pops the top two values off the stack, divides the first value by the second, and pushes the result back onto the stack.

### dup
Duplicates the top value on the stack.

### end
Removes the top dictionary from the dictionary stack.

### eq
Pops the top two values off the stack, compares them for equality, and pushes the result (true or false) back onto the stack.

### exch
Swaps the top two values on the stack.

### for
Pops the top four values off the stack: an initial value, an increment, a limit, and a procedure. The procedure is executed for each value from the initial value to the limit, incrementing by the increment value each time.

### ge
Pops the top two values off the stack, compares them to see if the first is greater than or equal to the second, and pushes the result (true or false) back onto the stack.

### get
Pops the top two values off the stack, which must be an index and an array (or string), and pushes the element at the specified index back onto the stack.

### getinterval
Pops the top three values off the stack: an array or string, an index, and a count. It pushes a subarray or substring starting at the given index and spanning the given count back onto the stack.

### gt
Pops the top two values off the stack, compares them to see if the first is greater than the second, and pushes the result (true or false) back onto the stack.

### if
Pops the top two values off the stack: a boolean and a procedure. If the boolean is true, the procedure is executed.

### ifelse
Pops the top three values off the stack: a boolean and two procedures. If the boolean is true, the first procedure is executed; if false, the second procedure is executed.

### length
Pops the top value off the stack, which must be an array or string, and pushes the length of that array or string back onto the stack.

### le
Pops the top two values off the stack, compares them to see if the first is less than or equal to the second, and pushes the result (true or false) back onto the stack.

### lt
Pops the top two values off the stack, compares them to see if the first is less than the second, and pushes the result (true or false) back onto the stack.

### mod
Pops the top two values off the stack, computes the remainder when the first value is divided by the second, and pushes the result back onto the stack.

### mul
Pops the top two values off the stack, multiplies them together, and pushes the result of the multiplication back onto the stack.

### pop
Pops the top value off the stack and discards it.

### put
Pops the top three values off the stack: an array or string, an index, and a new value. It replaces the element at the specified index with the new value.

### roll
Rolls the top n elements of the stack d times, where n and d are the top two elements on the stack.

### stack
Prints all the elements currently on the stack.

### sub
Pops the top two values off the stack, subtracts the second value from the first, and pushes the result back onto the stack.

### =
Prints the top value on the stack without removing it.
