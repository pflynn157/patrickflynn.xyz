---
title: "LLIR"
date: "2022-05-16"
template:page
output:llir
menu: false
---

LLIR is one of my newest projects and is in some ways a companion to Tiny Lang. So what is LLIR? LLIR is a midend/backend compiler framework, similar in design and concept to LLVM.

So why did I create this? The short answer is because LLVM is great, but also big and complex.

When I started Tiny Lang and other related projects that used LLVM, I did so because using LLVM would allow me to focus on the frontend and the language, without worrying about debugging all stages. Indeed, this is where LLVM’s strong point is. However, for some of my personal research, I want to be able to interact closely with the underlying hardware. In theory, one can do this with LLVM, but in reality the framework is huge and complicated, so doing so is less than practical. My solution to this was to create LLIR. Because I love the design of LLVM, I wanted to create something similar in design, but not a complete clone. The most noticeable difference will be how the IR is structured (in LLVM, everything is based on Values, where as in LLIR there are separate types for instructions, operands, and so forth). The difference lies more in my needs than because I think one is necessarily a better design.

The source code can be found [here](https://github.com/pflynn157/llir).

### The Status

LLIR is definitely new software. Between the alpha, beta, and release classifications, I would probably have to label this alpha software. At the moment, only the x86-64 architecture is supported. And while the IR itself is mostly complete and working, there are bugs in some areas, particularly in how structures are addressed.

That being said, the framework is complete enough to work in non-trivial applications. There is a fairly complete suite of tests, and it works fully with Tiny Lang (all the Tiny Lang tests build and pass using LLIR).

### Documentation

API documentation coming soon!

### How To Use

At the moment, I unfortunately don’t have any tutorials beside the documentation and examples on how to use this. The documentation is the best way to understand how to use the API, and the “examples” directory in the source code repository is the best way to see the framework in action.

There are two components in LLIR. The first is the C++ framework itself. In most cases, if you are constructing a compiler, this is what you would want to use. The other part is the LLIR language compiler. This parses and compiles straight LLIR code.

### Examples

This is an example of Hello World in LLIR:

```
#module hello
 
extern void puts(%0:\*i8);
 
global i32 main() {
entry:
  call void puts($STR0("Hi!"));
  ret i32 2;
}
```

This is an example of the C++ framework. It generates a simple program that returns 0.

```
#include <iostream>
#include <cstdlib>
#include <sys/stat.h>
#include <sys/types.h>
 
#include <llir.hpp>
#include <irbuilder.hpp>
#include <amd64/amd64.hpp>
using namespace LLIR;
 
int main(int argc, char \*\*argv) {
    Module \*mod = new Module("test1");
    IRBuilder \*builder = new IRBuilder(mod);
     
    //
    // func main:
    //     ret 0
    Type \*i32Type = Type::createI32Type();
    Function \*mainFunc = Function::Create("main", Linkage::Global, i32Type);
    mod->addFunction(mainFunc);
    builder->setCurrentFunction(mainFunc);
    builder->createBlock("entry");
     
    Operand \*i32 = builder->createI32(0);
    builder->createRet(i32Type, i32);
     
    mod->print();
    mod->transform();
     
    // Generate a binary
    mkdir("./test\_bin", 0700);
     
    LLIR::Amd64Writer \*writer = new LLIR::Amd64Writer(mod);
    writer->compile();
    writer->writeToFile("/tmp/test1.s");
    system("gcc /tmp/test1.s -o ./test\_bin/test1");
     
    return 0;
}
```


