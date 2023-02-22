---
title: "New Project: Tiny Lang"
date: "2021-12-22"
categories: 
  - "project-updates"
---

Yes, its another compiler project. Actually, unlike my other projects, this one has a start, stop, and purpose.

Tiny Lang is a programming language specification and reference implementation all forked (more like "down-forked") from my Orka compiler project. It began shortly after my Christmas break from school started. I was doing some hardware projects, and needed a basic compiler. As I was getting rather tired of implementing things over and over again, and because I didn't have a compiler project that was suitable without substantial modifications, I decided to create a spec and a project that could form the base for future projects. And so Tiny Lang was born.

I also have a secondary goal that it can be used as a learning tool. Because the language is very simple, the implementation by consequence is simple. I hope this can be something people interesting in compilers can use.

You can find source code with examples [here](https://github.com/pflynn157/tiny-lang), and the project page [here on my site](/tiny-lang.html).

### Version 0.1

This is version 0.1 of the language and the implementation. While I think I'm mostly done with the language itself, the implementation inherited a number of problems from Orka, must notably bad syntax checking problems. This is on my to-do list, but I really want to go back to something else I was experimenting with, and I doubt anyone else is going to be using this in the near future, so I'll fix it later.

In short, this means if you are programming in Tiny, and its doing weird things, check and re-check your code :)
