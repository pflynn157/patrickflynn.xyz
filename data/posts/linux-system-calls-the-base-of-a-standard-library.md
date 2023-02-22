---
title: "Linux System Calls: The Base of a Standard Library"
date: "2021-07-25"
categories: 
  - "linux"
  - "standard-libraries"
  - "tutorial"
---

Have you ever wondered how the C library works? Or any language's standard library for that matter? Sure, its easy to understand how certain aspects are done- things like containers, strings, and mathematical functions are generally written in the language itself. But how does the library interact with the underlying operating system? The answer is with system calls. Indeed, many C standard library functions are little more than wrappers around a particular system call.

In this post, we're going to take a look at system calls and how to implement them.

### What is a System Call?

To quote Wikipedia (which actually has a very good definition), "a system call is the programmatic way in which a computer program requests a service from the kernel of the operating system".

Let's back up. Consider common operations a computer program may do: printing to the screen, reading from the keyboard, creating a file, opening a file, creating a folder, and so forth. How does a program do this?

The short answer is that it doesn't. Printing to the screen, or reading from the keyboard, or doing anything in the file system is a complicated operation. So complicated, that if every program had to implement these functions themselves, no work would ever get done. That's where the operating system comes in. The operating system (among other things) provides a clean interface to allow programs to easily access these resources. Because the operating system is a program itself, we can't access these resources via an ordinary library right off. We have to use a system calls, an interface that allows a program to call the running operating system. Most modern CPUs provide instructions to make this process easier.

You as a programmer don't have to write these system calls because they are abstracted into libraries, such as the C library. This makes your programs portable and your life easier.

### So Why Should I Care About This?

To answer this question, I will assume that we are asking this in context of a programming language designer.

When you create a programming language, you will need a standard library of some sort to access the system resources we mentioned. One option is to just link to the C library. While this may be a good idea for the early stages of development, it is not a good idea as your language matures. If you link to the C library, you have to follow all the C rules, down to linking with the C startup files, which initialize the standard library. And unless your language interpolates with C exactly, you will probably have to have boiler code for more advanced constructs.

Therefore, you should create your own standard library at some point, and to do so you will need to understand system calls. Let's go through and write a few simple ones to understand how this is done.

### Getting Started

System calls are both architecture and OS specific. The OS part shouldn't surprise you. MacOS, Linux, and Windows all have different system calls and their own way of doing things. In this tutorial, we are going to focus on Linux. I imagine MacOS, being a Unix-like system, is similar, but don't quote me on it. I have no idea how Windows works, but I've heard stories.

Regarding the architecture part, even within Linux, the system call numbers vary from platform to platform. x86-64, x86-32, AArch64, and Arm all have different system call numbers. Because most people are probably running on x86-64, we will focus on that. The calls can all be found in the kernel source, but for more common architectures, you can often find the same information online.

For the four architectures I mentioned, Google has an excellent table: [https://chromium.googlesource.com/chromiumos/docs/+/HEAD/constants/syscalls.md](https://chromium.googlesource.com/chromiumos/docs/+/HEAD/constants/syscalls.md)

### Syntax

The system calls themselves have to be done in assembly. Before you panic, don't worry- you don't have to implement your standard library in assembly. A common method is to create a platform-specific system call function, and then call that from a higher-level language. However, for the sake of learning, we are going to stick to assembly.

All Linux system calls have a number and up to five arguments. A system call can return a value, but you don't always need this. On x86-64, the system call register is RAX. The arguments will go in RDI, RSI, RDX, R10, R8, and R9.

Before continuing, I should note: since we are not using a library or a high level language, the starting function is not "main"; it is "\_start". Don't worry about this for now, just take my word for it. I will reserve discussion around that for another post.

### Hello World and Exit

Time to get our hands dirty! To start things out, we will write a simple program that exits and returns a number. Consider this source:

```
.intel_syntax noprefix
.global _start
_start:
    mov rax, 60
    mov rdi, 5
    syscall
```

I'm going to assume you know some assembly, so I'm not going to go through every line. This syntax is compatible with the GNU Assembler which should already be on your system (for the record, I HATE the AT&T syntax, so that's why I have the first line).

If you look at the table, the system call for "exit" is 60. The first argument specifies the exit code. In this case, we have 5, but any number is fine. Finally, we tell the CPU to call the kernel and exit our program. If you compile and run, you should see the exit code (the "echo $?" means to show the exit code of the last program that was run):

![](images/exit.png)

Excellent! Now, let's expand our example, and make it print "Hello World!" to the console.

```
.intel_syntax noprefix
.data
msg: .string "Hello, World!\n"
.text
.global _start
_start:
    mov rax, 1
    mov rdi, 1
    mov rsi, OFFSET FLAT:msg
    mov rdx, 14
    syscall
    mov rax, 60
    mov rdi, 5
    syscall
```

You'll notice we still kept the system call for exit. The C library does the same thing when the main function returns. This is because if you don't, the program will return a segmentation fault after printing. But to return to our print call. Again, looking at the table, you can see that 1 is the system call for write- we are writing to the console. The second argument is for the file descriptor. If you wanted to write to a file, you can use this same system call with the same syntax. However, since we are writing to a console, this argument becomes 1. 1 is still a file descriptor, but it represents STDOUT, a special file read by your terminal. The second argument is a pointer to your string, and the third argument is the length of the string.

If you compile and run, you should see this:

![](images/output.png)

### Writing to a File

Now let's do a more complicated example. We will further build onto our example above by creating a file, opening it, writing "Hello World", and then closing it. Examine this source code:

```
.intel_syntax noprefix
.data
fileName: .string "./file.txt"
msg: .string "Hello, World!\n"
.text
.global _start
_start:
    /* Create the file */
    mov rax, 85
    mov rdi, OFFSET FLAT:fileName
    mov rsi, 420
    syscall
    
    /* Open the file */
    mov rax, 2
    mov rdi, OFFSET FLAT:fileName
    mov rsi, 2
    mov rdx, 420
    syscall
    
    /* Save the file descriptor */
    mov rcx, rax
    
    /* Write to the file */
    mov rax, 1
    mov rdi, rcx
    mov rsi, OFFSET FLAT:msg
    mov rdx, 14
    syscall
    
    /* Close the file */
    mov rax, 3
    mov rdi, rcx
    syscall
    /* Exit */
    mov rax, 60
    mov rdi, 5
    syscall
```

I won't go into a ton of detail at this point, but I will cover a few key things. First, the "420" under file creation and opening is the mode- the permissions. This number corresponds to the octal "644". This means the current user can read and write the file, and everyone else can read it. Next, under file opening, you will notice the "2" for the second argument. This tells the kernel to open the file for reading and writing.

The final thing to note is after the file opening call, you will notice we have the instruction "mov rcx, rax". This is an example of a system call that returns something- in this case, it returns the file descriptor of the opened file. You will need the file descriptor to write and close it. Ordinarily, this would be saved to memory. However, that requires some complicated setup beyond the scope of this article, so we are going to save it to the RCX register. The choice of RCX is because it won't get clobbered (erased) by other system calls.

When you compile and run, you should see something like this:

![](images/file.png)

Congratulations! You have created and written to a file only using system calls!

### Conclusion

There's a lot more we can do with this- just scroll through the system call list. In my last big compiler project, the Ida language/compiler, the standard library eventually had capabilities to allocate and free memory; create, open, read, write, and close files; fork and run programs; and basic file system operations like creating directories. This particular case was a little easier because I had a native system call interface in the language. But still, its easy to expose a system call function to build your standard library.

If you're interested in making a library or knowing how one works, hopefully this presents a good starting point.

Thanks for reading!
