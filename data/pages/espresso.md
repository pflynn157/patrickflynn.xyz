---
title: "Espresso"
date: "2021-07-27"
template: page
output: espresso
menu: false
---

Espresso is my sixth significant programming language/compiler project. However, it is one of my most unique. All my compilers so far have taken the source language and have gone down to assembly code- they have been compiled languages. Espresso is semi-compiled: It runs on the Java Virtual Machine.

The purpose of this project was largely to learn more about Java, while providing a unique, interesting challenge. The project is completely written in C++, and because I am great believe in making things as difficult as possible, I wrote the library for generating the Java class files myself. The frontend is a fork of Orka's. However, the language is not Orka. The JVM is designed to represent an object oriented programming environment, not the linear environment you would find on a regular machine. As a result, Espresso has programming constructs to open these features.

You can find the source here: [https://github.com/pflynn157/espresso](https://github.com/pflynn157/espresso)

### The Language

You can find documentation on the current progress of the language [here](/espresso-language.html).

### How Does One Generate Java?

Generating Java is actually not that difficult. It is not for the faint of heart however; you need to make sure you know how to write binary, especially structures, and you need to be ready to read some documentation.

In my first Java code generator, I was stupidly generating all the binary manually, and needless to say, this was very buggy. In this generator, I use structures to write everything. However, in C and C++ at least, you can't write deep trees to a file. In other words, if your structure has pointers to other sub-structures, you will need to have separate routines to write them in the proper order to a file. C++ allows member functions in structures, so the most efficient method is to override and call these functions.

These links provide good information on the Java class file and Java bytecode. They were the starting point for this project and previous projects:

- [https://medium.com/@davethomas_9528/writing-hello-world-in-java-byte-code-34f75428e0ad](https://medium.com/@davethomas_9528/writing-hello-world-in-java-byte-code-34f75428e0ad)
- [https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html)
- [https://en.wikipedia.org/wiki/Java_bytecode_instruction_listings](https://en.wikipedia.org/wiki/Java_bytecode_instruction_listings)

### Building and Running

Building is super easy. Simple create a build directory, run CMake (no arguments needed), and run make. The only dependency to build is a C++ compiler, and the only dependency to run is Java. I would recommend the JDK so you have access to JavaP, but this is not essential.

To run, simply feed an input file to the compiler. The class file will be generated with the class named after the file. There are two handy command line options:

- \--ast -> Allows you to visualize the abstract syntax tree (AST)
- \--javap -> Calls JavaP to disassemble the class file.


