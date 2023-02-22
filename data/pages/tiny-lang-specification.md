---
title: "Tiny Lang Specification"
date: "2021-12-22"
template:page
output:tiny-lang-specification
menu: false
---

Welcome! This page describes the specification of a Tiny Lang implementation.

Please keep in mind that this specification is meant to be a starting point for other languages. If you are forking Tiny, you are free to keep or discard whatever you like. However, if you are intending to create an implementation of the Tiny Programming Language, you must follow the specifications here, and be able to pass all the tests and the examples in the reference implementation.

The implementation source code can be found [here](https://github.com/pflynn157/tiny-lang).

## Semantics

The grammar is largely a "what you see is what it does". For example, if I assign an integer value to an integer variable, that's what happens. Some incorrect semantics should go without saying: assigning a string to an integer variable obviously doesn't make sense. However, there are a few semantics that need consideration.

### Arrays, Structures, and Pointers

Arrays, structures, and pointer inputs (ie, as function parameters) are all treated as heap-allocated objects. Many languages such as C give you the option (or automatically just do it) to allocate arrays and structures on the stack, and then pass by copy or pass by reference. In Tiny, all arrays and structures are heap allocated, and when they are passed or returned from functions, they are passed and returned as pointers.

Of course, if the implementation is as an interpreted language, the interpreter is free to decide the semantics under the hood. However, from the perspective of the language, the syntax and behavior should remain the same.

### Strings

Strings are treated as null-terminated arrays of "char" values. A "char" is a wrapper around the "i8" (byte) type. A string literal can only be assigned to a string type, but in practice byte arrays and strings can be operated on in the same way.

The language contains the following operators on strings:

- <string> = <string> / <string> != <string> -> String comparison. This works the same way under the hood as the C "strcmp" function.
- <string> + <string> -> String to string concatenation.
- <string> + <char> -> String to character concatenation.

These functions are not something a computer can inherently do. As such, runtime functions are required to implement this.

### Casting

All casting is implicit, and requires the end-user programmer to know what they are doing. Casting checks are optional. In some cases, it is probably wise to check for signed casting, but otherwise variables can be assigned interchangebly.

As long as no special syntax is added for casting, an implementation is free to interpret this however the programmer wishes. If you want casting checks, all the better, but if you're just experimenting, its fine to leave them out.

### The "extern" keyword

This is an optional construct, and as such is not included in the grammar. The reference implementation has this so linking can be easily accomplished.

If you are creating a Tiny Lang implementation, at the very least support should be added to ignore this construct much as you would a comment. If you are forking the language, then of course it is up to you.

### Command Line Arguments

Command line arguments follow the syntax of <argument list> <argument count>:

```
func main(args:string[], argc:i32) -> i32 is
    var i : i32 := 0;
    while i < argc do
        println(args[i]);
        i := i + 1;
    end

    return 0;
end
```

### Built-In Functions / Standard Library

In order to make the language portable, there are a limited subset of core library functions that must be provided by the implementation. A standard library specification is below after the grammar.

## Grammar

Below is the grammar for Tiny:

```
data_type:
      i8 | u8
    | i16 | u16
    | i32 | u32
    | i64 | u64
    | char
    | bool
    | string
    ;
    
expression_list:
      expression
    | expression_list ',' expression
    ;
    
const_expr:
      INTEGER
    | HEX_L
    | TRUE | FALSE
    | STRING_L
    | CHAR_L
    ;
    
primary_expr:
      ID
    | const_expr
    ;
    
conditional_expr:
      expression '=' expression
    | expression '>' expression
    | expression '<' expression
    | expression '!=' expression
    | expression '>=' expression
    | expression '<=' expression
    ;
    
logical_expr:
      expression AND expression
    | expression OR expression
    ;
    
assign_expr: expression ':=' expression
    ;
    
binary_expr:
      assign_expr
    | expression '+' expression
    | expression '-' expression
    | expression '*' expression
    | expression '/' expression
    | expression '%' expression
    | expression '&' expression
    | expression '|' expression
    | expression '^' expression
    ;
    
function_expr:
      ID '(' ')'
    | ID '(' expression_list ')'
    ;
    
array_expr: ID '[' expression ']'
    ;
    
struct_expr: ID '.' ID
    ;
    
expression:
      primary_expr
    | conditional_expr
    | logical_expr
    | binary_expr
    | function_expr
    | array_expr
    | struct_expr
    ;
    
id_list:
      ID
    | id_list ',' ID
    ;
    
var_declaration:
      VAR id_list ':' data_type ASSIGN expression ';'
    | VAR id_list ':' data_type '[' expression ']' ';'
    ;
    
struct_declaration: STRUCT ID : ID ';'
    ;
    
constant_declaration: CONST ID ':' data_type ASSIGN const_expr ';'
    ;
    
function_call:
      ID '(' ')' ';'
    | ID '(' expression_list ')' ';'
    ;
    
conditional:
      IF conditional_expr THEN block END
    | IF conditional_expr THEN block elif_block
    ;
    
elif_block:
      ELIF conditional_expr THEN block END
    | ELIF conditional_expr THEN block elif_block
    | ELSE block END
    ;
    
loop: WHILE conditional_expr DO block END
    ;

import_list:
      ID
    | import_list '.' ID
    ;
    
import: IMPORT import_list ';'
    ;
    
expr_statement: assign_expr ';'
    ;
    
return:
      RETURN ';'
    | RETURN expression ';'
    ;
    
statement:
      var_declaration
    | struct_declaration
    | constant_declaration
    | function_call
    | conditional
    | loop
    | import
    | expr_statement
    | return
    ;
    
statement_list:
      statement
    | statement_list statement
    ;
    
block: statement_list;
    
arg:
      ID ':' data_type
    | ID ':' data_type '[' ']'
    ;
    
arg_list:
      arg
    | arg_list ',' arg
    ;

function:
      FUNC ID IS block END
    | FUNC ID '(' ')' IS block END
    | FUNC ID ARROW data_type IS block END
    | FUNC ID '(' ')' ARROW data_type IS block END
    | FUNC ID '(' arg_list ')' IS block END
    | FUNC ID '(' arg_list ')' ARROW data_type IS BLOCK END
    ;
    
struct_item: ID ':' data_type ASSIGN const_expr ';'
    ;
    
struct_block:
      struct_item
    | struct_block struct_item
    ;
    
struct: STRUCT ID IS struct_block END
    ;

global_statement:
      constant
    | struct
    | function
    ;

global_statement_list:
      global_statement
    | global_statement_list global_statement
    ;

translation_unit : global_statement_list;
```

## Standard Library

Because Tiny is portable across implementations, it requires a runtime to be truly useful. A few core functions are required for the language to work at all. If you are implementing Tiny, these functions are absolutely required. If you are creating your own fork, then of course it is up to you, though I hope you will consider the logic behind having some of these functions.

The method of implementation is up to you. It is perfectly possible to implement all these library functions in C without the C library using only Linux system calls. (If you add a "syscall" construct to Tiny, you could probably implement them in Tiny itself). The reference implementation standard library is written in C++ with C linkages.

In the list below, functions essential to the language itself are starred (*). This is considered part of the corelib, which should be statically linked. The other functions can be dynamically linked. Note for simplicity, the reference implementation dynamically links everything.

Note for the print/println function, the following format specifiers must be supported: %d, %s, %c, %x (decimal, string, character, hex respectively).

core (NOTE: These functions are unneccessary if the implementation is interpreted)
- malloc(i32)
- free(ptr)

std.io
- print(string, ...)
- println(string, ...)
- readline() -> string
- readint() -> i32

std.fs
- fs\_open(string, i32) -> i32
- fs\_eof(i32) -> bool
- fs\_get(i32) -> i32
- fs\_writeln(i32, string)
- fs\_write(i32, u8[], i32, i32)
- fs\_close(i32)

std.string
- stringcmp(string, string) -> i32
- strcat\_str(string, string) -> string
- strcat\_char(string, char) -> string

std.num
- rand\_init()
- rand\_int(i32, i32) -> i32


