---
title: "RISC-V: New Project and New Stuff"
date: "2022-11-14"
categories: 
  - "project-updates"
  - "risc-v"
---

Hello all! This is my first time writing here in a while (but not the first, since I posted the lunar eclipse pictures I took the other day :) ). I'm going to briefly talk about a new project I'm working on and new stuff in general.

## RISC-V: New Project

In one of my classes this semester, we're writing a RISC-V simulator. It's been a very interesting project and the first to really get me going with computer science and projects once again. The project itself is a really good learning experience, and I personally haven't had any issues getting it completed, but I think the professor overestimated the C++ skill set of the rest of the class given the fact that it's a computer engineering, not a computer science class... And my own feelings about his obsession with the clock cycles aside... it's been very interesting.

But anyway. This project turned out to be something that I wanted anyway, so I've been working on my own fork of the school project, and on some tools and various components for the simulator. One of these projects is a simple assembler, which you can find here: [https://github.com/pflynn157/riscv-as](https://github.com/pflynn157/riscv-as).

I post this because it is a very good example of how to write a simple assembler, and assemblers for certain architectures are a great way to get started with compiler concepts without dealing with the compiler overhead that a full-blown language requires. And besides, writing an assembler gives you the most intimate knowledge of the hardware you can get from a purely software level. Of course, the keyword phrase here is "certain architectures." If you're aiming to learn by writing an x86 assembler, then yeah you're probably shooting yourself in the foot.

But to return to the RISC-V assembler: this assembler is really basic, and just generates flat binaries meant to be run by the simulator (though there's nothing to prevent it from being run on RISC-V hardware provided special formats aren't required). Even though it's basic, it supports the entire RISC-V 32I instruction set, and adding additional formats is trivial. Even adapting it to support ELF formats should be trivial. The project itself contains three main files: lex.cpp, pass1.cpp, and pass2.cpp. The "lex.cpp" file is the lexical analyzer. The "pass1.cpp" builds the symbol table. The "pass2.cpp" uses that symbol table to generate the actual binary.

This project is technically obsolete. I've since forked it to use in a new, larger RISC-V project so it has more features and more capabilities. The next thing I talk about will be this larger project. This assembler is here for the school RISC-V assembler, which I'll make public when the semester is over. I originally had it public, but a little bird told me someone was stealing from the repo for the class, so I had to make it private.

## New Stuff

You're probably wondering why the big gap in any writing here. I'll speak briefly on that.

Last spring was anything but an adventure to put it simply, so after the semester ended, I just spaced out and decided to take a break, focus on other things, and focus on work. Not only that, my creativity battery was drained so I needed some time to recharge it. In particular, my creativity battery with compilers was drained, so I needed a new project that wasn't yet another programming language or compiler. That's not to say I don't enjoy these fields, but it does reach a point where you need to take a break.

I'm also throttling back on doing any side projects for anything more than fun. If you were reading this site last spring, you may have noticed that I was doing a number of projects with tons of goals, often from a research-y angle, and that's fine of course, but for me personally, it took the fun out of a lot of it, and got to the point where the fun projects felt like work. And trust me, I have plenty of work between the job and school.

It's important to remember that every single thing doesn't need to have some ulterior purpose. We have plenty of ulterior purposes through our work and our day-to-day lives. Making something to learn or for no other reason then because you find the process enjoyable or fun is perfectly okay. If you think about it, that's what a lot of my projects are. Sure we have Microsoft Excel, but making a spreadsheet application was something I found a lot of fun. Sure we have a hundred million text editors, but making my own text editor was fun. Sure writing an operating system is redundant and is taping into a done science, but you learn a lot and it's fun. And so on. Nothing is a waste of time if you find it enjoyable.

But anyway. Going forward, I'm not going to stick to any post schedule or much of a plan or anything with my projects. I'm just going to write and post when I have something to write about and I feel inspired. The same goes with my projects. I'm not going to pressure myself with any of them, I'm just going to work on them and I'll post them here as I go. It's up to you to find them interesting :).

Thanks for reading, and hope to see you around soon!


