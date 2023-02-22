---
title: "New Project: Orka"
date: "2021-07-30"
categories: 
  - "project-updates"
---

This actually isn't so "new" at this point; I realized I forgot to publish a post on it. A week or so ago, I released a new programming project. It is yet another programming language/compiler project, but it is genuienly a new thing.

The Orka project originally started out as a C++ clone of Ida; the difference (other than being C++) was rather than writing my own backend, I wanted to use LLVM, partly to make the process go faster, but mainly so I could learn LLVM for my job. The syntax was almost exactly the same at first, but I eventually began chaning it- mainly simplifying it. It still retains the Wirth language look that I like, but it is definitely less Wirth-like than Ida.

While I'm proud of the language and the fact it uses LLVM so well, I am (perhaps strangely) most proud of the frontend- the parser. While I've written several parsers and have gotten better at doing so, one thing I've struggled with is getting the expressions right. Expressions in an abstract syntax tree are supposed to actually be a tree... Not a liner list as I've been doing (and trust me, problems arise when you try to do it this way). I finally got the parser to parse and build an AST correctly, and the end result is that the translation to LLVM is super easy.

Currently, the language is somewhat of a finished product for me. I'll probably go back at some point and add to it, but I'm moving on to other projects at the moment, so you can consider it complete for now. My goal of learning LLVM has been accomplished. For those who are new to compilers and especially LLVM, hopefully this project can serve as a reference.

You can find the project in the links below:

- Source: [https://github.com/pflynn157/orka](https://github.com/pflynn157/orka)
- Documentation: [patrickflynn.xyz/orka](/orka.html)

