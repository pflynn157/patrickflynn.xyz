---
title: "New Project: LLIR"
date: "2022-05-18"
categories: 
  - "compilers"
  - "project-updates"
---

Hello everyone! Today, I’m announcing a new project: LLIR.

This project has actually been sitting around since the end of last year. I was saving it as part of a larger project that I was working on, but I put that project aside and decided to merge this with the rest of my work on Github.

LLIR is a compiler midend/backend framework with a similar design and purpose to LLVM. It was created in response to me wanting a hackable and easy-to-work with backend that I could do experiments on. While LLVM is great for easily writing compilers, its too big to do certain things with. In addition to the C++ framework, LLIR also features a midend compiler to allow you to compile textual IR to assembly. For an example of a real-world use with LLIR, see the [source code of Tiny Lang](https://github.com/pflynn157/tiny-lang).

To learn more about the project, and to see the documentation and source code, see [here](/llir.html).
