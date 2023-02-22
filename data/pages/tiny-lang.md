---
title: "Tiny Lang"
date: "2021-12-22"
template:page
output:tiny-lang
menu: false
---

Tiny Lang is yet another one of my programming languages. Whereas my others have been primarily learning projects, this one is meant to fill a specific need (at least my need...). Tiny Lang is a minimalist programming language specification that is meant to be easily implemented and used either as a teaching tool or for experimentation. The latter purpose fills my need.

Why did I create this?

The most immediate reason to fulfill a personal need. When Christmas break started, I began working on several inter-related hardware projects. I had a programming language idea (a few actually), but I didn't have a compiler that would be a suitable starting point. The closest I had was Orka, but it contains a number of high-level constructs. Ida was another possibility, but it also contains some high-level constructs, and the expression parser is broken, to put it simply. In both cases, these compilers were meant as compiler learning projects, and not something I could take and use elsewhere, especially in low-level hardware environments.

The solution looked like it would be writing yet another compiler from scratch. I actually began doing that, but after implementing a basic lexer, I got stuck trying to figure out what language to implement. C is not something I want to deal with, so it began looking like I would end up doing another Orka- or Ida-like language. My Orka frontend is very good, but again because it implements high-level constructs, using Orka as a starting point meant at least a day of trimming out crap. And then probably another day designing a basic language.

This is when Tiny Lang was born. I decided to create a very simple, deliberately crippled yet still usable programming language that could be the base for future projects. Because Orka was a language I like, and because its compiler is working rather well and is still easy to fork, I decided to use that as the starting point. I first designed the spec of what the Tiny language should look like, and then I forked Orka and simplified the compiler to create a reference implementation.

The specification can be found [here](/tiny-lang-specification.html), and the source code can be found [here](https://github.com/pflynn157/tiny-lang).

## How Is It Different From C?

This is a fair question: is Tiny a different language from C? A simplified version? Or C with a different syntax?

The answer: all and neither.

In terms of what Tiny has in the language, it is very similar to C. It has basic functions, all the basic signed/unsigned integer types, the basic mathematical operations, variables, arrays, and structures. In fact, Tiny and C are largely compatible with each other when implemented as a systems programming language.

However, there are very important differences:

- _Not a compiled language_: Although Tiny certainly can be a compiled language (the reference implementation is an actual compiler), Tiny can be run as an interpreted language as well. C contains fine memory control, something you don't need or even want in an interpreted language. Tiny abstracts some key concepts away that C makes visible.
- _Limited Language_: Although Tiny is a complete language, I deliberately crippled it in some areas. It is complete in that it contains variables, arrays, conditionals, loops, functions, structures, and so forth. However, it is crippled in that the syntax is very rigid, and in some cases common constructs are missing. For instance, there is only a "while" loop in Tiny (you can do anything with a while loop that more advanced loops allow you to do).
- _Modern Language_: While it is a limited language, it does contains some modern features through abstraction (or more specifically, syntatic sugar). Because booleans are so widely used, I included a specific boolean type, something C lacks (a boolean is syntatic sugar around integers). I also included a string type and basic string handling support. Strings are nothing more than character arrays, or byte ("i8") arrays, making the implementation easy. There is also in-built support for string comparisons and string concatenation (in its compiled form, this is handled with the standard library).
- _Built-In Functions:_ The language contains a few built-in functions that make use easier. The most important is the "print/println" functions, which work like "printf."
- _Defined Standard Library:_ In addition to the language spec, there is also a defined standard library. This library contains the defined built-in functions along with additional functions that make Tiny more useful. The language also contains an "import" construct that can be interpreted based on your implementation.
- _Strings, Arrays, and Pointers:_ We already discussed the built-in string handling. As far as arrays and pointers go (ie, pointers to structure declarations), all pointers are allocated on the heap and passed by reference to functions. C allows manual control over this, which can make learning and use more difficult. Tiny abstracts this away, and calculates the proper malloc amount call.

## Does it Work?

Yes!

As mentioned, the reference implementation is a fork (a "downward fork"?) of Orka. Orka's compiler is a fully working, LLVM-based compiler, so forking the project to create the reference implementation was basically a matter of removing things.

In the project, there is an example directory with some small programs written in Tiny: a clone of the Unix "echo", a clone of the Unix "cat", a math practice program, and a simple Tic-Tac-Toe program.

## Example

Here's an example that can read and write files:

```
import std.io;
import std.fs;

func main() -> i32 is
    var fd : i32 := fs_open("../first.ok", 1);
    if fd = 0 then
        println("Unable to open.");
        return 1;
    end
    
    while fs_eof(fd) = false do
        var c : char := fs_get(fd);
        
        if fs_eof(fd) = false then
            print("%c", c);
        end
    end
    
    fs_close(fd);
    
    #
    # Now, write
    #
    fd := fs_open("/tmp/test.txt", 2);
    if fd = 0 then
        println("Unable to open for write.");
        return 1;
    end
    
    fs_writeln(fd, "Hello!");
    fs_writeln(fd, "How are you?");
    fs_close(fd);
    
    #
    # Try binary writing
    #
    fd := fs_open("/tmp/first.bin", 2);
    if fd = 0 then
        println("Unable to open test2.");
        return 1;
    end
    
    var bytes : u8\[5\];
    bytes[0] := 0xA1;
    bytes[1] := 0xA2;
    bytes[2] := 0xA3;
    bytes[3] := 0xA4;
    bytes[4] := 0xA5;
    
    fs_write(fd, bytes, 1, 5);
    fs_close(fd);
    
    return 0;
end
```


