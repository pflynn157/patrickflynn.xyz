---
title: "Creating a Simple VM: Adding Variables"
date: "2022-06-12"
categories: 
  - "compilers"
  - "programming-languages"
---

Welcome back! You probably remember a few weeks ago that we created a simple application-level virtual machine that could read a binary file, load numbers, add them, and print them. Today, we're going to extend that machine, and add variables. I don't think I need to tell you how important variables are to a programming language. Therefore, this is the logical next step. Before we dive into the implementation, let us briefly consider this conceptually.

You will remember that registers on a real machine and the stack on our virtual machine are used to do operations. The data on these structures is operated upon and changed very quickly, making them unsuitable for storing data long-term. This is where memory comes in. On a real computer, this would be the volatile memory- the DRAM. When we want to save a variable, we save the data to a location in memory, and when we need that data, we load from that location. Variables are useful in programming languages because they are named values. The compiler takes care of determining the location, but you as the programmer only have to worry about the variables by their name.

So how do we do this on a virtual machine? The answer: the exact same way. We are still utilizing the computer's DRAM, but because this is a virtual machine, we use an array. So now, the machine will have two data structures: an array for variables, and a stack for operations.

This program will build off the original code we wrote a few weeks ago, so if you haven't read it, I encourage you to go back and do so. I will still post the code, but I'm only going over the parts we're adding.

Let's dive into this!

### The Program

This is the program we'll be writing:

```
iconst 50
istore 1
iconst 10
istore 2

iload 1
iload 2
imul
istore 3

iload 1
iload 2
idiv
istore 4

iload 3
iprint
ipop

iload 4
iprint
ipop

exit
```

The program would roughly correspond to this in C:

```
int x = 50;        // Location 1
int y = 10;        // Location 2
int mulResult;     // Location 3
int divResult;     // Location 4

mulResult = x * y;
printf("%d\\n", mulResult);

divResult = x / y;
printf("%d\\n", divResult);
```

You'll notice some changes and additions to our instructions. First, notice the "iconst" and the "iload" instructions. Originally, "iload" was used to load a number to the stack. Now, the "iconst" does that. The "iload" still follows the same syntax, but that number represents a location in memory. The number corresponds to an index in the array, and loads the value at that index to the stack.

The "istore" does the inverse of the "iload" instruction. It pops from the top of the stack, and saves that value to a location represented by that number.

Finally, notice the "ipop" instruction. All "ipop" does is pop a value from the top of the stack and discards it. Why? You'll remember that "iprint" doesn't pop from the stack; it only peeps. Therefore, we have to pop the loaded value before we can print the next one.

### Changing the Opcodes

When you look at the source, you'll notice we included an additional file:

```
#pragma once

enum Opcode
{
    I_CONST = 0xA1,
    I_LOAD = 0xA2,
    I_STORE = 0xA3,
    I_POP = 0xA4,
    
    I_ADD = 0xA5,
    I_SUB = 0xA6,
    I_MUL = 0xA7,
    I_DIV = 0xA8,
    
    I_PRINT = 0xA9,
    
    EXIT = 0x73
};

```
This header contains our opcode enumeration for both the reader and the writer, which is handy so we don't have to keep two copies up to date.

In addition to the new opcodes, notice how some of the numbers changed for the existing ones. This is the beauty of enumerations. If we had hard-coded the numbers, we would have had to either A) leave the existing ones alone and deal with a less-than-logical numbering sequence, or B) change everything. Because we are using enumerations, we can change the numbers, and the writer and VM will still work perfectly.

In the real world, however, you want to be careful about doing things like this on production products. Of course, there's times you just have to, but this will break the ABI- the application binary interface, meaning that any older programs will not be compatible with newer versions of the VM. Breaking the ABI was a good idea in this case because we were changing the meaning of one of the instructions (the "iload").

### Updating the Writer

I originally was going to skip this section, but I'll make a quick note.

The writer (writer.c) will be basically the same. We do have to re-arrange the "WriteOpcode" function calls to create our own program, but that is the main difference.

The one other thing we have to do is write an extra field to our binary file. Just after the version field, we need to write an integer indicating how many variables we have. I'll cover this more in a second, but in the meantime, see the source.

### Updating the VM

This is where the fun really begins. First, scroll down to the main function, and look at the new fread call we make before calling the "run" function:

```
// Get the variable size
int varSize = 0;
fread(&varSize, sizeof(int), 1, file);
```

This integer tells the VM how many variables we have in the program so we can allocate our memory accordingly. Now, it is not strictly necessary that you have this, especially in today's world where memory is cheap. We could use a C++ container like the vector or map, or we could just create a huge array of 100 or so elements. However, using a C++ container incurs overhead, and allocating one big array wastes memory. By using this field, you only allocate what you need. This was inspired by Java, which has a similar field for each method.

Okay, now let's go to the "run" function. The variables are all stored in this unimpressive array:

```
int vars[varSize];
```

Now we can start adding our new instructions. As you remember, "iconst" does the exact same thing as "iload" used to do, so we can just change the case statement:

```
case I_CONST: {
    int arg = 0;
    fread(&arg, sizeof(int), 1, file);
    stack.push(arg);
} break;
```

Next, we'll create the new "iload". A load has an argument, so we must read that from the binary file. That argument will be the index of the array. We retrieve the value from that array index, and push it to the stack:

```
case I_LOAD: {
    int arg = 0;
    fread(&arg, sizeof(int), 1, file);
    int val = vars[arg];
    stack.push(val);
} break;
```

The "istore" instruction is similar; it just works the opposite direction:

```
case I_STORE: {
    int arg = 0;
    fread(&arg, sizeof(int), 1, file);

    int val = stack.top();
    stack.pop();
    vars[arg] = val;
} break;
```

Finally, we have the "ipop" instruction, which is really simple:

```
case I_POP: {
    stack.pop();
} break;
```

You'll also notice that we have the two new "imul" and "idiv" instructions. These are simply add-ons to the two existing math instructions (add and subtract), so I'm not going to go over it here. See the source code if you're interested.

### Build and Run

The writer is written in C (although you can use it as C++ if you want), and the VM is written in C++. You can use these commands to compile and run:

```
gcc writer.c -o writer && ./writer
g++ reader.cpp -o reader && ./reader
```

One implementation idea for the VM if you're looking to extend it is to add command line argument support for input files. Currently, the input is hard-coded into the VM's main function, which is obviously wrong. Doing something similar with the writer would eventually be nice as well, but that will require you to write an assembler so you have something to read.

### Conclusion

As you can see, adding variables was a straightforward process. Our VM is now a little more useful, and we can more easily do complicated math operations, or even several math operations. The variables themselves aside, you can see that adding instructions is a pretty easy process itself.

Despite having variables, our VM is still not an accurate representation of a computer; if anything, it is more of a calculator. In order to make it a computer, we need compare and branch instructions, which allows us to make decisions and control the course of the program. That will be our next step, which we will return to in a future post.

Thanks for reading!

### The Source

Below is our source code, which is now three files. This source is in the public domain; use to your heart's content.

opcodes.h

```
#pragma once

enum Opcode
{
    I_CONST = 0xA1,
    I_LOAD = 0xA2,
    I_STORE = 0xA3,
    I_POP = 0xA4,
    
    I_ADD = 0xA5,
    I_SUB = 0xA6,
    I_MUL = 0xA7,
    I_DIV = 0xA8,
    
    I_PRINT = 0xA9,
    
    EXIT = 0x73
};
```

writer.c

```
#include <stdio.h>
#include <stdint.h>

#include "opcodes.h"

void WriteOpcode1(uint8_t opcode, int arg, FILE *file)
{
    fputc(opcode, file);
    fwrite(&arg, sizeof(int), 1, file);
}

void WriteOpcode(uint8_t opcode, FILE *file)
{
    fputc(opcode, file);
}

int main()
{
    // Create the file
    FILE *file = fopen("./program.bin", "wb");
    
    // Write the signature and version
    fputs("SimpleVM", file);
    fputc(0x01, file);
    
    // Number of variables
    int count = 5;
    fwrite(&count, sizeof(int), 1, file);
    
    // iconst 50
    // istore 1
    // iconst 10
    // istore 2
    WriteOpcode1(I_CONST, 50, file);
    WriteOpcode1(I_STORE, 1, file);
    WriteOpcode1(I_CONST, 10, file);
    WriteOpcode1(I_STORE, 2, file);
    
    // iload 1
    // iload 2
    // imul
    // istore 3
    WriteOpcode1(I_LOAD, 1, file);
    WriteOpcode1(I_LOAD, 2, file);
    WriteOpcode(I_MUL, file);
    WriteOpcode1(I_STORE, 3, file);
    
    // iload 1
    // iload 2
    // idiv
    // istore 4
    WriteOpcode1(I_LOAD, 1, file);
    WriteOpcode1(I_LOAD, 2, file);
    WriteOpcode(I_DIV, file);
    WriteOpcode1(I_STORE, 4, file);
    
    // iload 3
    // iprint
    // ipop
    WriteOpcode1(I_LOAD, 3, file);
    WriteOpcode(I_PRINT, file);
    WriteOpcode(I_POP, file);
    
    // iload 4
    // iprint
    // ipop
    WriteOpcode1(I_LOAD, 4, file);
    WriteOpcode(I_PRINT, file);
    WriteOpcode(I_POP, file);
    
    // exit
    WriteOpcode(EXIT, file);
    
    // Close the file
    fclose(file);
}
```

reader.cpp

```
#include <cstdio>
#include <cstdint>
#include <stack>
#include <iostream>

#include "opcodes.h"

void run(FILE *file, int varSize)
{
    int vars[varSize];
    std::stack<int> stack;
    
    while (!feof(file))
    {
        uint8_t opcode;
        fread(&opcode, sizeof(uint8_t), 1, file);
        
        bool isDone = false;
        
        switch (opcode)
        {
            case I_CONST: {
                int arg = 0;
                fread(&arg, sizeof(int), 1, file);
                stack.push(arg);
            } break;
            
            case I_LOAD: {
                int arg = 0;
                fread(&arg, sizeof(int), 1, file);
                int val = vars[arg];
                stack.push(val);
            } break;
            
            case I_STORE: {
                int arg = 0;
                fread(&arg, sizeof(int), 1, file);
                
                int val = stack.top();
                stack.pop();
                vars[arg] = val;
            } break;
            
            case I_POP: {
                stack.pop();
            } break;
            
            case I_ADD:
            case I_SUB:
            case I_MUL:
            case I_DIV: {
                int arg2 = stack.top();
                stack.pop();
                
                int arg1 = stack.top();
                stack.pop();
                
                if (opcode == I_ADD)
                    stack.push(arg1 + arg2);
                else if (opcode == I_SUB)
                    stack.push(arg1 - arg2);
                else if (opcode == I_MUL)
                    stack.push(arg1 * arg2);
                else if (opcode == I_DIV)
                    stack.push(arg1 / arg2);
            } break;
            
            case I_PRINT: {
                std::cout << stack.top() << std::endl;
            } break;
            
            case EXIT: {
                isDone = true;
            } break;
            
            default: {
                std::cerr << "Error: Unknown opcode." << std::endl;
                isDone = true;
            } break;
        }
        
        if (isDone) break;
    }
}

int main()
{
    // Open the file
    FILE *file = fopen("./program.bin", "rb");
    
    // Verify that our program is valid
    char signature[9];
    fread(&signature, sizeof(char), 8, file);
    signature[8] = '\\0';
    
    if (std::string(signature) == "SimpleVM") {
        std::cout << "File is valid." << std::endl;
    } else {
        std::cout << "Invalid input file." << std::endl;
        std::cout << signature << std::endl;
        return 1;
    }
    
    // Check the version
    uint8_t version = 0;
    fread(&version, sizeof(uint8_t), 1, file);
    
    std::cout << "Version: " << (int)version << std::endl;
    std::cout << std::endl;
    
    // Get the variable size
    int varSize = 0;
    fread(&varSize, sizeof(int), 1, file);

    // Run the program
    run(file, varSize);
    
    // Close the file
    fclose(file);  

    return 0;
}
```

