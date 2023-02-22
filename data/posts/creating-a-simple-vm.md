---
title: "Creating a Simple VM"
date: "2022-06-05"
categories: 
  - "compilers"
  - "programming-languages"
---

Welcome back! Today we’re going to learn how to write a simple application-level virtual machine. The VM we're making will be simple; all it does is add, subtract, and print the results. But this is an important first-step. Once you’re able to do this, we can start extending it for more advanced instructions.

The VM will be composed of two programs: the writer, and the reader. The writer generates our binary file, and the reader will execute it.

Let’s dive in!

## What is a VM?

You probably know what a virtual machine is from applications such as VMWare and VirtualBox. They run an entire operating system within another operating system by emulating a computer.

An application-level virtual machine is similar in concept to a conventional VM- it provides a virtual environment to run a program. It differs, however, in that it doesn’t emulate a full computer. Application-level virtual machines are generally used as a component of interpreted languages. Running interpreted languages from the source level is slow, but running a binary file is much faster. Furthermore, it is cross-platform. Your binary file for your VM can be run on any platform the VM is compatible with.

The best example of this is the Java Virtual Machine. As you likely know, Java doesn’t run on bare hardware. It uses the Java VM to run .class files. As long as your computer has the Java VM installed, it can run Java. Python and other languages operate on a similar concept.

Our VM is based on this concept. We have a custom binary file format, a program that generates it, and another program that runs it.

## Our Binary File

The first step to designing a VM is to design the file format (please note: I will be using “VM” to refer to application-level virtual machines such as ours for the rest of this post). Because this is our first VM, the design is going to be extremely simple:

Signature (String = “SimpleVM”)
Version (a 1-byte value)
Code (a 1-byte value followed by an optional 4-byte argument).

The signature and version is used to verify that the file can be run by the VM. While not strictly necessary, it is a very good section to have, especially if you plan on expanding your machine.

Next, we need to determine our opcodes. There is no rule for how to determine this; whatever numbering system works for you is sufficient. Generally, I use letters to determine the class of instructions.

```
enum Opcode
{
    I_LOAD = 0xA1,
    I_ADD = 0xA2,
    I_SUB = 0xA3,
    I_PRINT = 0xA7,
    EXIT = 0x73
};
```

## Generating the File

Okay, now we can generate the file. In the real world, you would probably want this to be an assembler or some sort of library, depending on what you are implementing. For right now however, the code is extremely simple. I’m not going to go into great detail here; I assume that you understand C and the library calls:

```
#include <stdio.h>
#include <stdint.h>

enum Opcode
{
    I_LOAD = 0xA1,
    I_ADD = 0xA2,
    I_SUB = 0xA3,
    I_PRINT = 0xA7,
    EXIT = 0x73
};

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
    
    // iload 5
    // iload 6
    WriteOpcode1(I_LOAD, 5, file);
    WriteOpcode1(I_LOAD, 6, file);
    
    // iadd
    WriteOpcode(I_ADD, file);
    
    // iprint
    WriteOpcode(I_PRINT, file);
    
    // iload 1
    // isub
    WriteOpcode1(I_LOAD, 1, file);
    WriteOpcode(I_SUB, file);
    
    // iprint
    WriteOpcode(I_PRINT, file);
    
    // exit
    WriteOpcode(EXIT, file);
    
    // Close the file
    fclose(file);
}
```

Build and run the program, and if all goes well, you won’t see any output. A way to verify that the file was generated correctly is to use hexdump. Notice the signature at the beginning of the file.

![](images/hexdump.png)

## Running the File

Okay, now that we have generated the file, let’s run it! Once again, the code is pretty straightforward, so I won’t go into great detail. I will just touch on the important points.

First, we have to verify the file. We read the string, which is 8 characters long (with the ninth being the NULL byte- the terminating character), and then we read the version. Currently, we don’t care about the version, but we still have to read the character so the file position is moved forward:

```
// Verify that our program is valid
char signature[9];
fread(&signature, sizeof(char), 8, file);
signature[8] = '\0';
    
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
```

Now that everything is verified, we can start executing code. This is done in the “run” function.

We will notice the “stack” object at the top of the function. This exists because our VM is a stack-based machine. This is another key difference between real machines and virtual machines (especially application VMs). Real-machines are generally register-based. Values to be operated on are stored in small memory segments called registers. Virtual machines use stacks. There are two reasons for this. First, on real machines, memory is finite, whereas on virtual machines, memory is infinite. While this isn’t technically true, you have vastly more memory in a VM then in a real machine. The second reason is because compiling for a stack machine is simpler than for a register-based machine.

Stack operations are simple since you don’t have to worry about location. All operations either push, pop, or peek from the stack.

The “iload” instruction reads an integer value and pushes it to the stack:

```
case I_LOAD: {
    int arg = 0;
    fread(&arg, sizeof(int), 1, file);
    stack.push(arg);
} break;
```

The “iadd” and “isub” instructions pop the top two values from the stack. Note that stacks operate in reverse order, so the second argument is the first one off the stack (this is important for subtraction and division operations).

```
int arg2 = stack.top();
stack.pop();

int arg1 = stack.top();
stack.pop();

if (opcode == I_ADD)
    stack.push(arg1 + arg2);
else if (opcode == I_SUB)
    stack.push(arg1 - arg2)

Finally, the “iprint” instruction simply peeks at the value at the top of the stack, and prints it.

case I_PRINT: {
    std::cout << stack.top() << std::endl;
} break;
```

For the full code output, see the end of the file.

## Conclusion

Hopefully this piqued your interest some. A good next step would be to add the multiplication and division instructions. It is extremely simple- simply add the proper opcodes, to both files, and the corresponding switch statements to the VM. A second task, especially if you plan to expand this, is to move the opcode definitions to to a header file.

I’m hoping to include some future posts on extending this machine. A good next step is to add support for labels and jumps- once these are in, you will have a full computer. After that, strings and other constants are handy features to have.

Hopefully you found this interesting and informative. Thanks for reading!

## The Code

Below you can find the complete code for the VM. All the code listed here is in the public domain.

```
#include <cstdio>
#include <cstdint>
#include <stack>
#include <iostream>

enum Opcode
{
    I_LOAD = 0xA1,
    I_ADD = 0xA2,
    I_SUB = 0xA3,
    I_PRINT = 0xA7,
    EXIT = 0x73
};

void run(FILE *file)
{
    std::stack<int> stack;
    
    while (!feof(file))
    {
        uint8_t opcode;
        fread(&opcode, sizeof(uint8_t), 1, file);
        
        bool isDone = false;
        
        switch (opcode)
        {
            case I_LOAD: {
                int arg = 0;
                fread(&arg, sizeof(int), 1, file);
                stack.push(arg);
            } break;
            
            case I_ADD:
            case I_SUB: {
                int arg2 = stack.top();
                stack.pop();
                
                int arg1 = stack.top();
                stack.pop();
                
                if (opcode == I_ADD)
                    stack.push(arg1 + arg2);
                else if (opcode == I_SUB)
                    stack.push(arg1 - arg2);
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

    // Run the program
    run(file);
    
    // Close the file
    fclose(file);  

    return 0;
}
```

