---
title: "New Project: RISC-V CPU"
date: "2021-12-15"
categories: 
  - "hardware"
  - "project-updates"
---

Yet another CPU project...

This project is similar to my last project, my LegV8 CPU. Like the LegV8 CPU, this is a CPU core written in VHDL. Unlike the other project, however, this implements the RISC-V 32-bit architecture, and is not a school project. This implements almost the entire RISC-V 32I base instruction set. I still have a few arithmetic instructions that need some help, but all the main arithmetic, load, store, and branching instructions are working.

A full, detailed description of the project can be found [here](/risc-v-cpu.html).

The code can be found [here](https://github.com/pflynn157/riscv32-cpu).

Here's a picture of it running this C program:

```
int n = 0;
for (int i = 0; i<10; i++) {
    n += i;
}

// n = 45
```

![](images/forloop-1024x611.png)
