---
title: "Espresso Language"
date: "2021-07-27"
template: page
output: espresso-language
menu: false
---

While the Espresso language is stable enough for me to be producing this initial documentation, it isn't stable, and things could change and break. As I said in the introduction, the language is a fork of Orka designed to run on the Java Virtual Machine, so the two are very similar. This page gives an overview of the language, and will be updated as the project progresses.

### The Class File

This is important to note. If you've programmed in Java before, you're probably used to declaring a class like this:

```
public class HelloWorld {

    // Code here...
}
```

This is not necessary in Espresso. A class named after the input file is implicitly created. All functions and member variables are part of this class.

### Methods

There are two types of methods in Espresso: Functions and Routines.

Functions are members of the class. They are non-static, meaning the class has to be created before they can be called. Functions can be public, protected, or private, with the visibility following the same rules as Java. Here are examples of functions:

```
public func sayHello is
    println("Hello!");
    this.sayHello2();
    this.sayHello3();
end

protected func sayHello2 is
    println("Protected: Hello!!!");
end

private func sayHello3 is
    println("Private: Hello!!!");
end
```

Routines are static methods. Like functions, they can be public, protected, or private, but unlike functions, they can be called without the class being instantiated. The main routine of your function could look like this:

```
routine main(args : str\[\]) is
    println("Hello, World!");
end
```

### Strings and Println

Later, you'll begin to notice the string type, but in the meantime, have you noticed all the "println"s in our example?

"Println" is a wrapper around the Java "System.out.println" function. The built-in string type is a wrapper around Java's String object. The reason for this is because these functions are used so much that it's easier to provide these convenience facilities. For the println, currently only printing strings and integers are supported. Concatenation, however, isn't supported.

Later on, I'll provide an improved method for loading external libraries, but for right now, keep this in mind.

### Variables

Espresso supports the same primitive types as Orka, but for now, only integers, strings, and some objects are supported. The syntax roughly follows this format:

```
var <name> : <type> := <optional expression>
```

"int" and "str" can be used to represent integers and strings respectively. For example, an integer expression could look like this:

```
var x : int := y \* 22 + 3;
```

If you wish to initialize an object, you can do so as in the example below:

```
public func sayHello is
    println("Hello!");
end

routine main(args : str\[\]) is
    var clazz : Inner;
    clazz.sayHello();
end
```

### Operators

Currently, operators are only supported on integers right now. The following arithmetic operators are supported:

- +
- \-
- \*
- /
- %

And the following logical/bitwise operators are supported:

- & (AND)
- | (OR)
- ^ (XOR)
- << (shift left)
- >> (shift right)


