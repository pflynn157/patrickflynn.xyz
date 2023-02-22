---
title: "New Project: Espresso"
date: "2021-08-11"
categories: 
  - "project-updates"
---

I released yet another one of my new geeky projects: my [Espresso language/compiler](/espresso.html).

This project is very proof-of-concept, meaning that I created it not so much for practicality, but as a personal goal that I could create something that actually runs on the Java Virtual Machine. That said, the language is not complete. It can do some non-trivial things, but key parts such as loops and conditionals are lacking.

The project originally started as an experiment at redoing an earlier Java code generation project, and as it became successful, I decided to try my hand at creating a full language compiler with it. Since I already had a very nice AST in my Orka project, I simply forked Orka, replaced the LLVM backend with my new Java backend, dropped the AST elements I didn't need, and connected it all together. It works rather well too.

Originally, I was going to add better language support, including elements like loops, conditionals, arrays, better Java library interfacing, and so forth, but I began working on other projects, and while I find it very neat to have something running on the JVM, it's not something I find interesting enough to work on long term. It's also not something that many people would find useful. However, enough is working to justify releasing it and putting aside for the time being.
