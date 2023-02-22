---
title: "RISC-V Toolchain"
date: "2022-11-13"
template:page
output:risc-v-toolchain
menu: false
---

This page contains the technical description of my RISC-V toolchain project. Note that I'll try to keep it as up-to-date as possible, but I can't promise anything :). At the time of writing this, I'm thinking about doing a redesign to the interrupt system, which is slight technically but practically breaks all my examples. But anyway, I'll post when I make breaking changes.

So what is this project? The name is admittedly a little misleading right now because this isn't a toolchain in the sense of being a compiler, assembler, linker, etc. There is a complete assembler, and all those other things are planned, but the main focus right now is the simulator. Currently, there is the assembler, the simulator, and some basic in-progress BIOSes for the simulator. The simulator supports the entire RV-32I instruction set and has a method for system calls and hardware interface, including display and storage media. The simulator itself is complete enough to mimic a real-world environment for writing an operating system.

This page contains the technical description of everything. The code can be found here: [https://github.com/pflynn157/riscv-toolchain](https://github.com/pflynn157/riscv-toolchain).

## The Assembler

The assembler is a direct fork of the RISC-V assembler you can see sitting on my Github profile. It supports the entire RV-32I instruction set, but with some additional features oriented towards the needs of the simulator.

#### Register Names

The assembler supports and defines the following extra register names: "bp", "ra", and "sp". BP is the base pointer, and although it's colloquially supposed to indicate the stack base, in this architecture, it is supposed to represent the base in memory for the currently executing area of the program. In other words, the BIOS starts with a base pointer of 0, does its thing, and then updates the BP to represent the start of either the operating system or whatever kernel it loads in memory. This could occur directly after the BIOS or at some arbitrary location in memory.

The "ra" register holds the return address for the "jalr" register. If you're jumping to a one-level function, you can simply maintain the register, but if you're possibly jumping to higher function calls, you should probably store "ra" in the stack somewhere. The "sp" register holds the stack pointer location. This should be updated as standard on other architectures, with the BIOS or the kernel setting the stack pointer, and any "children" functions allocating space for their needs.

"bp" corresponds to x29; "ra" corresponds to x30; "sp" corresponds to x31.

#### Extra Instructions: ecall and hlt

The "ecall" instruction is defined as an I-Type instruction taking a destination register, a source register, and an immediate. The "ecall" instruction is used for interrupts. However, the interrupt system will be described in the simulator. The "hlt" instruction is defined as 0xFFFFFFFF (all "1"s). This is also simulator specific. It tells the simulator to immediately stop executing and return.

#### Labels, Strings, and Binary Padding

Labels are defined as some name followed by a colon, ie `MYLABEL:`. If the label is not followed by anything, it simply reflects the location counter within the assembler. You would obviously want to use these for jumps and function calls. A string is represented by a label followed by a string, ie `STRING1: "Hello!"`. The location counter is updated with the length of the string, and this is encoded directly as-is into the binary file. As such, care should be taken that the simulator not try to execute the string. Empty binary padding can be defined like this: `PADDING: \[256\]`. This defines an empty space of 256 bytes. The location counter is updated with this result, and the binary produces that number of zeroed bytes at that location within the file.

## The Simulator

The simulator is meant to be a full RISC-V emulator capable of replicating conditions as accurately as possible. That being said, this simulator is not accurate in many areas. It is not cycle accurate- there is no concept of stalls, clock cycles, memory access time, etc. This is a deliberate design choice as I wanted to focus more on the toolchain and OS perspective than on the hardware perspective. The simulator is also not accurate in terms of hardware interfaces and interrupts- at least as I understand it. The privileged specification does talk about interrupts and environment interface, but for simplicity I just designed my own system using the "ecall" instruction. I am more familiar with x86- to a point to hate many parts of it- so the design of this section of the simulator probably replicates my idea of how x86 should look.

With that being said though, this is still RISC-V, so if you wanted to use this for RISC-V development work, the main thing you would have to change is your interrupt interface and anything else to adapt for whatever piece of hardware you are using. This simulator is meant to be more of a fun experimentation and teaching tool, not some serious, accurate development environment.

#### Running

The build system produces an executable simply called "sim". My plan is to change this because this is a horrible interface, but it currently doesn't take any arguments. The simulator requires two files to be present in the current working directory: "boot.bin" and "sata0.bin". The "boot.bin" file is a binary generated by the assembler. This is the BIOS- it gets loaded directly into memory at location 0, and execution starts there. Even though I call this the BIOS, in reality you can run anything produced by the assembler here- it doesn't have to fulfill the purposes of a BIOS. "sata0.bin" is the disk file.

When the simulator exits, it produces a dump of memory automatically and silently called "memory.bin". This is the state of the RAM at the moment the program finished executing. You can view this with hexdump. The simulator also outputs the contents of all the registers when the program finishes running. This is something I plan to change since the display, errors, and debug output all go to stdout, which gets really confusing really quickly.

#### The Overall Structure

The core of the simulator is obviously the RISC-V virtual CPU. This is fairly simple, as a testament to the beautiful simplicity of RISC-V.

The RAM is connected directly to memory. Because this is not cycle-accurate in any way, there is no concept of cache or anything like that. All devices are connected to the bus. There is a virtual bus in charge of interfacing the CPU with any devices, and triggering the interrupts as needed. The bus supports 256 devices. Device 0 is the display, and device 2 is hard drive 0. Currently, device 1 is for system calls (virtual interrupts), but I may change this behavior.

Everything is setup and connected in "main.cpp". Everything else is in its own source file.

#### Interrupts in General

Interrupts are done with the "ecall" instruction. The syntax of ecall is as follows: ecall <rd> <rs1> <imm>.

There is no concept of "in" or "out." This is entirely dependent on the hardware. The destination register (rd) holds the input data, and holds any data returned by the interrupt. The source register defines the port (or which interrupt to call). This is used by the bus to determine which device to send data to. So, for the display, you want to set "rs1" to 0, or for the disk drive, you want to set it "2". The immediate holds the command. This command is sent directly to the device to tell it what it should do (for example, do we want to read, write, or set the position of the disk?).

I don't love this design, I chose it for now so I could have something that would conform to the spec without introducing new instructions. In practice though, its proving really clunky and difficult to use, so I'm probably going to come up with a better method. But for now, use it like this.

#### Interfacing with the Display

As mentioned above, display is port 0 on the bus. The display controller accepts the following commands:

- 1 -> Display the current buffer (print to the screen)
- 2 -> Clear the buffer (this does not clear the screen)
- 3 -> Load a character to the buffer

The display controller maintains an internal buffer that you can add 8-bit (1-byte) characters to using command 3. Command 1 will tell the controller to print the entire string to the display.

#### Interfacing with the Disk

Although you can technically attach the disk anywhere on the bus, by default disk 0 is on port 2. The disk controller accepts the following commands:

- 0 -> Identify the disk. If the disk is present, "1" is saved to destination register (rd).
- 1 -> Read one byte from the disk
- 2 -> Write one byte to the disk
- 3 -> Set the position on the disk (for either reading or writing)

Please note that you should only call command 3 once before you begin reading or writer. When you read or write, the position is automatically updated to the next position, so calling command 3 after each read or write could cause double-reading or double-writing. Command 1 (read) saves the data to the destination register (rd), while command 2 (write) reads from the destination register (rd).

#### System Calls

The software system interrupt interface is called through port 1. This is handled directly by the CPU, despite the bus-like interface, so as a result, port 1 on the bus cannot be accessed. The system call interface accepts the following commands:

- 0 -> Trigger a call
- All others < 256 -> Set an interrupt

Setting an interrupt is done by placing the address of the interrupt function in the destination register (rd) and choosing an integer > 0 and < 256, and using this as the command call (the immediate). The CPU can handle up to 256 interrupts. Triggering a call is done by placing the call index in the destination register (rd). Any arguments are defined by the call (aka, by you). The CPU will take the address from the interrupt table, save the current program counter to register 30 (ra, x30), and then jump to the interrupt. To return to the regular control flow, use `jalr x0, ra, 0`.

I really don't like the design of the system calls or the interrupts in general, so I will probably be changing them. More than likely, I will move software interrupts to a separate mechanism, so this will probably change first.


