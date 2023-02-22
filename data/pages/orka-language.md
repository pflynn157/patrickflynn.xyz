---
title: "Orka Language"
date: "2021-07-21"
template: page
output: orka-language
menu: false
---

Welcome to the documenation for the Orka language!

This is meant to give an overview, not to go deep into any complexities. I do this partly in case I decide to change anything. That being said though, I don't plan on changing any of the syntax. I'm largely happy with how everything is, and I hate breaking things, so you can mostly count on this staying this same.

### Functions

In general, functions have this structure:

```
func main is
    println("Hello, world!");
end
```

The "is" keyword specifies the start of a function, while "end" specifies where it stops. A return type can be specified like this:

```
func main -> int is
    println("Hello, world!");
    return 0;
end
```

If no return type is specified, the function is assumed to be void. Returns are automatically inserted by the compiler.

Arguments and function calls are much like in other languages. If a function is being used that is located in a different library or file, the "func" keyword can be replaced with "extern".

```
extern printf(line:str, x:int);

func getNumber(x:int, y:int) -> int is
    return 20 + x + y;
end

func main -> int is
    var x : int := getNumber(23, 10);
    printf("X: %d\\n", x);
    
    return 0;
end
```

### Datatypes and Variables

Orka has the following datatypes:

- byte / ubyte -> byte values
- short / ushort -> word (usually 16-bit) values
- int / uint -> dword (usually 32-bit) values
- int64 / uint64 -> qword (usually 64-bit) values
- char -> char literals
- str -> string literals
- bool -> true/false values

Variables are built using this syntax: var <name> : <type> := <expression>;

```
var x : int := 20;
```

Notice the assignment operator. We do not use the "=" operator for assignments; that is reserved for equality comparisons. Rather, we use the ":=" operator, like in Go or Ada.

### Arrays

Arrays are similar to variables. When you declare an array, arrays are dynamically and automatically allocated on the heap. They have this syntax: var <name> : <type>\[<size expression>\];

```
var numbers : int[5];
```

Array sets and accesses are similar to that of other languages. Below is a full example of a program with array use:

```
func main -> int is
    var numbers : int\[5\];
    numbers\[2\] := 242;
    
    var x : int := numbers\[2\];
    printf("%d\\n", x);
    return 0;
end
```

### Enumerations

Enumerations are similar to those in C; they are little more than named integer values. While you can specify the type you want the enumeration to represent, this is not implemented yet. Enumerations are fully handled at compile time.

An enum declaration is done outside a function, and looks like this:

```
enum Vals is
    A,
    B,
    C
end
```

Enumeration values can be assigned to variables like this:

```
var x : int = Vals::B;
```

### Structures

Structures look similar to those of other languages, but they have what I consider an important feature: you can specify initial values. Structure declarations require that you specify an inital value, which is set at compile time.

A structure declaration looks like this:

```
struct S1 is
    x : int := 10;
    y : int := 20;
end
```

Inside a function, a structure variable is declared like this:

```
struct s : S1;
```

And the members can be set and accessed like this:

```
var v1 : int := s.x;
s.x := 25;
```

### Conditionals

Conditionals are very similar to other languages:

```
if x > 20 then
    println("X greater than 20.");
elif x > 10 then
    println("X greater than 10.");
elif x > 5 then
    println("X greater than 5.");
else
    println("IDK");
end
```

Like in other languages, it is completely valid to omit an elif or else statement. Also, note the presence of the "then" keyword in the "if" and "elif" blocks. These are required before the conditional body.

Conditionals can also be constructed with a single argument, as below. The value compared to in these cases will either be "1" or "true", depending on the type.

```
var x : bool := true;
    
if x then
    println("True");
else
    println("False");
end
```

The following are the valid conditional operators:

- \= (Equal to)
- != (Not equal to)
- \> (Greater than)
- < (Less than)
- \>= (Greater than or equal to)
- <= (Less than or equal to)


### Loops

There are four kinds of loops in Orka: the while loop, the repeat loop, the for loop, and the for-all loop. All loops have the "break" and "continue" keywords, which function in the same way as other languages.

A while loop looks like this:

```
while x < 10 do 
    printf("X: %d\n", x);
    x := x + 1;
end
```

A repeat loop is basically an infinite loop. You are responsible for making sure it breaks out at some point; otherwise, it will run forever. A repeat loop looks like this:

```
var i : int := 0;
    
repeat
    printf("%d|", i);
    i := i + 2;

    if i = 22 then break; end
end
```

For loops are probably closest in looks to Ada. For loops can have the optional "step" keyword, which specifies the increment amount. Finally, the ranges can be either variables or constants. For loops look like this:

```
for i in 0 .. 10 do
    numbers\[i\] := 0;
end
    
for i in 0 .. 10 step 2 do
    numbers\[i\] := 100;
end
```

For-all loops are range loops; they are used for iterating over arrays. The index variable is the current array element, while the second value is the array to be iterated over. They look like this:

```
forall i in numbers do
    printf("%d\n", i);
end
```


