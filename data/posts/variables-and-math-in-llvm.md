---
title: "Variables and Math in LLVM"
date: "2021-12-19"
categories: 
  - "compilers"
  - "llvm"
---

Hello everyone! Earlier, I wrote a post on generating a Hello World program using the LLVM framework. Today, I'm doing a follow-up post on that in which we'll be creating variables and doing some simple math. In the process, we're going to learn how to use the C "printf" function with LLVM.

Creating variables and performing operations on them is easy in LLVM, as well as a crucial step. After all, a program without variables is basically useless. LLVM makes variable management easy, meaning that you don't have to deal with things like the stack size and register allocation as you would when you're creating your own backend. Math is also easy too. Math operations in LLVM are almost identical to a math operation and assignment in high-level programming languages. But once again, you get the benefit of not having to deal with memory and register allocations. A single math statement handles load, store, and the operation itself.

In this post, we will be implementing a program that looks roughly like this in C:

```
#include <stdio.h>

int main() {
    int x = 10;
    int y = 14;
    int z = 0;

    z = x + y - 7;

    printf("Result: %d\n", z);

    return 3;
}
```

True, this is not the most spectacular program, but once you can do this in LLVM, you can build a large number of more complex programs.

Let's dive in!

## Getting Started

I'm going to try to introduce the new parts in sections, so I would recommend trying to follow along by adding the parts yourself. However, I'm not writing this completely from scratch. We are going to build directly off our original example:

```
#include <iostream>
#include <vector>

#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/BasicBlock.h"

// Needed to generate assembly
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/Host.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Support/TargetRegistry.h"
#include "llvm/Support/TargetSelect.h"
#include "llvm/Target/TargetMachine.h"
#include "llvm/Target/TargetOptions.h"
#include "llvm/IR/LegacyPassManager.h"

using namespace llvm;

std::unique_ptr<LLVMContext> context;
std::unique_ptr<Module> mod;
std::unique_ptr<IRBuilder<>> builder;

void assemble();

int main(int argc, char *argv[]) {
    // Setup everything
    context = std::make_unique<LLVMContext>();
    mod = std::make_unique<Module>("unit1", *context);
    builder = std::make_unique<IRBuilder<>>(*context);
    
    // Create an extern declaration to puts
    Type *putsRetType = Type::getVoidTy(*context);
    Type *putsArgType = Type::getInt8PtrTy(*context);
    
    FunctionType *putsFT = FunctionType::get(putsRetType, putsArgType, false);
    Function *putsFunc = Function::Create(putsFT, Function::ExternalLinkage, "puts", mod.get());
    
    // Create Function
    Type *funcRetType = Type::getInt32Ty(*context);
    FunctionType *FT = FunctionType::get(funcRetType, false);
    Function *func = Function::Create(FT, Function::ExternalLinkage, "main", mod.get());
    
    // Create the function body
    BasicBlock *mainBlock = BasicBlock::Create(*context, "entry", func);
    builder->SetInsertPoint(mainBlock);
    
    // Call puts, and print "Hello World!"
    std::vector<Value *> args;
    Value *str = builder->CreateGlobalStringPtr("Hello World!");
    args.push_back(str);
    
    Function *callee = mod->getFunction("puts");
    builder->CreateCall(callee, args);
    
    // Return 3
    Value *retValue = builder->getInt32(3);
    builder->CreateRet(retValue);
    
    //dump
    mod->print(errs(), nullptr);
    
    // Assemble and build
    assemble();
    
    // Compile
    // Using system() is bad; I am using it for the sake of readability
    system("as first.s -o first.o");
    
    std::string cmd = "ld ";
    cmd += "/usr/lib/x86_64-linux-gnu/crt1.o /usr/lib/x86_64-linux-gnu/crti.o /usr/lib/x86_64-linux-gnu/crtn.o ";
    cmd += "first.o -o first ";
    cmd += "-dynamic-linker /lib64/ld-linux-x86-64.so.2 -lc";
    system(cmd.c_str());
    
    return 0;
}

// Generate assemble and build
void assemble() {
    // We are going to generate for X86, so tell LLVM
    LLVMInitializeX86TargetInfo();
    LLVMInitializeX86Target();
    LLVMInitializeX86TargetMC();
    LLVMInitializeX86AsmParser();
    LLVMInitializeX86AsmPrinter();

    // Get the target triple so LLVM knows what to generate assembly for
    std::string triple = sys::getDefaultTargetTriple();
    mod->setTargetTriple(triple);
    
    // Look up the target
    std::string error;
    auto target = TargetRegistry::lookupTarget(triple, error);
    
    // Check for any errors with the target triple
    if (!target) {
        errs() << error;
        return;
    }
    
    // Setup the target writer
    auto CPU = "generic";
    auto features = "";
    
    TargetOptions options;
    auto RM = Optional<Reloc::Model>();
    auto machine = target->createTargetMachine(triple, CPU, features, options, RM);
    mod->setDataLayout(machine->createDataLayout());
    
    // Finally, generate assembly
    std::string outputPath = "./first.s";
    std::error_code errorCode;
    raw_fd_ostream writer(outputPath, errorCode, sys::fs::OF_None);
    
    if (errorCode) {
        errs() << "Unable to open file: " << errorCode.message();
        return;
    }
    
    legacy::PassManager pass;
    auto outputType = CGFT_AssemblyFile;
    
    if (machine->addPassesToEmitFile(pass, writer, nullptr, outputType)) {
        errs() << "Unable to write to file.";
        return;
    }
    
    pass.run(*mod);
    writer.flush();
}
```

There are two things to note here. First of all, when I ran it on my Linux Mint computer, I began running into weird issues with the linking step, so I had to change to a manual linking, which you can see near the bottom of the main function. Ordinarily, you should be able to pass the ".s" file directly into GCC, but for some reason that wasn't working. Learning how to link manually is a good thing to know if you are interested in compiler development, so I would recommend keeping this. However, if you are not on an Ubuntu-based system, you need to change the paths to the "crt" files (I think they are under "/usr/lib" on other systems).

The second thing to note is that we will only be working in the main function, so you don't have to worry about the second function at all. Everything I post going forward (except the final code listing) will be in the main function.

## Creating and Assigning a Variable

Okay, first let's create the variables for our program. We are creating three: "x, y, and z", all of int32 type:

```
// Create variables x, y, and z, all of int32 type
Type *i32Type = Type::getInt32Ty(*context);
    
Value *varX = builder->CreateAlloca(i32Type);
Value *varY = builder->CreateAlloca(i32Type);
Value *varZ = builder->CreateAlloca(i32Type);
```

Perfect! Now, let's initialize them:

```
// x = 10, y = 14, z = 0
Value *const10 = builder->getInt32(10);
builder->CreateStore(const10, varX);

Value *const14 = builder->getInt32(14);
builder->CreateStore(const14, varY);

Value *const0 = builder->getInt32(0);
builder->CreateStore(const0, varZ);
```

One thing I should note is to pay attention to "store". This is kind of confusing- to me at least- but the left value is what's being stored, and the right value is the destination (or memory location). I've found that many of the problems I've created for myself have been caused by me stupidly putting them in the wrong order.

## Doing Math

Okay, now that our variables are created, we can do math. We wish to do this equation:

```
z = x + y - 7
```

And this is the code we use:

```
Value *valX = builder->CreateLoad(varX);
Value *valY = builder->CreateLoad(varY);
Value *const7 = builder->getInt32(7);

Value *sum = builder->CreateAdd(valX, valY);
sum = builder->CreateSub(sum, const7);
    
builder->CreateStore(sum, varZ);
```

As you can see, doing math in LLVM is very straightforward. The first two lines load the values held by the variables (equivalent from loading from a memory location in the final assembly). The third line creates a constant, which could be thought of as an immediate value. The next two lines do the addition and subtraction. One of the nice things about LLVM is you can reassign values as the results change. Finally, we store the result to variable Z.

One thing I do want to note here is that these math instructions are only valid for integer types. You will notice that LLVM has float and double types. However, there are separate math and comparison instructions for those. I will go over floating point types in a different post, but for now just keep this in mind.

## Using Printf

The original code used "puts", which is only suitable for printing strings. So first, we need to convert to printf. Fortunately, it's really easy. First, find the code where we define the "puts" function, and replace it with the printf definition (which is really similar):

```
// Create an extern declaration to puts
Type *printfRetType = Type::getVoidTy(*context);
Type *printfArgType = Type::getInt8PtrTy(*context);
    
// -> Note that the last arg is "true" because variadic arguments are accepted now
FunctionType *printfFT = FunctionType::get(printfRetType, printfArgType, true);
Function *printfFunc = Function::Create(printfFT, Function::ExternalLinkage, "printf", mod.get());
```

The key thing to note is the last parameter where we create the "FunctionType" object. This is now "true" because it accepts variadic arguments, something important for printf.

Now, we need to change the function call and add the second parameter. This is not much different either from the original. The biggest difference is probably in the string- we have to change it to a "printf" style string for printing integers. Here is how it's done:

```
std::vector<Value *> args;
Value *str = builder->CreateGlobalStringPtr("X: %d\\n");
Value *xVal = builder->CreateLoad(varX);

args.push_back(str);
args.push_back(xVal);

Function *callee = mod->getFunction("printf");
builder->CreateCall(callee, args);
```

## Building and Running

To build and run this program, this line should work:

```
clang++ -g -O3 compiler.cpp `llvm-config --cxxflags --ldflags --system-libs --libs core` -o compiler
```

Once it builds, run the "compiler" binary. If all goes well, it will generate your assembly file, build, and link it. I mentioned this in the first part of the post, but you will probably have to adjust the linking command some if you are not on an Ubuntu based system. If you want to give GCC a try, go for it, but I was having issues so I can't guarantee that it would work.

## Conclusion

As you can see, creating and doing math on variables in LLVM is fairly easy, as is using the C library "printf" function. Between this post and previous posts, you now know many of the basics needed to construct more complex LLVM-based compilers. In future posts, we will do things like working with other functions, branches, loops, and floating-point variables.

Stay tuned, and thanks for reading!

## The Source

Here is the source code. Like the original listing, this too is in the public domain, so use and enjoy!

```
#include <iostream>
#include <vector>

#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/BasicBlock.h"

// Needed to generate assembly
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/Host.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Support/TargetRegistry.h"
#include "llvm/Support/TargetSelect.h"
#include "llvm/Target/TargetMachine.h"
#include "llvm/Target/TargetOptions.h"
#include "llvm/IR/LegacyPassManager.h"

using namespace llvm;

std::unique_ptr<LLVMContext> context;
std::unique_ptr<Module> mod;
std::unique_ptr<IRBuilder<>> builder;

void assemble();

int main(int argc, char *argv[]) {
    // Setup everything
    context = std::make_unique<LLVMContext>();
    mod = std::make_unique<Module>("unit1", *context);
    builder = std::make_unique<IRBuilder<>>(*context);
    
    // Create an extern declaration to puts
    Type *printfRetType = Type::getVoidTy(*context);
    Type *printfArgType = Type::getInt8PtrTy(*context);
    
    // -> Note that the last arg is "true" because variadic arguments are accepted now
    FunctionType *printfFT = FunctionType::get(printfRetType, printfArgType, true);
    Function *printfFunc = Function::Create(printfFT, Function::ExternalLinkage, "printf", mod.get());
    
    // Create Function
    Type *funcRetType = Type::getInt32Ty(*context);
    FunctionType *FT = FunctionType::get(funcRetType, false);
    Function *func = Function::Create(FT, Function::ExternalLinkage, "main", mod.get());
    
    // Create the function body
    BasicBlock *mainBlock = BasicBlock::Create(*context, "entry", func);
    builder->SetInsertPoint(mainBlock);
    
    // Create variables x, y, and z, all of int32 type
    Type *i32Type = Type::getInt32Ty(*context);
    
    Value *varX = builder->CreateAlloca(i32Type);
    Value *varY = builder->CreateAlloca(i32Type);
    Value *varZ = builder->CreateAlloca(i32Type);
    
    // x = 10, y = 14, z = 0
    Value *const10 = builder->getInt32(10);
    builder->CreateStore(const10, varX);
    
    Value *const14 = builder->getInt32(14);
    builder->CreateStore(const14, varY);
    
    Value *const0 = builder->getInt32(0);
    builder->CreateStore(const0, varZ);
    
    // z = x + y - 7
    Value *valX = builder->CreateLoad(varX);
    Value *valY = builder->CreateLoad(varY);
    Value *const7 = builder->getInt32(7);
    
    Value *sum = builder->CreateAdd(valX, valY);
    sum = builder->CreateSub(sum, const7);
    
    builder->CreateStore(sum, varZ);
    
    // Call printf, and print variable X
    std::vector<Value *> args;
    Value *str = builder->CreateGlobalStringPtr("Result: %d\\n");
    Value *valZ = builder->CreateLoad(varZ);
    
    args.push_back(str);
    args.push_back(valZ);
    
    Function *callee = mod->getFunction("printf");
    builder->CreateCall(callee, args);
    
    // Return 3
    Value *retValue = builder->getInt32(3);
    builder->CreateRet(retValue);
    
    //dump
    mod->print(errs(), nullptr);
    
    // Assemble and build
    assemble();
    
    // Compile
    // Using system() is bad; I am using it for the sake of readability
    system("as first.s -o first.o");
    
    std::string cmd = "ld ";
    cmd += "/usr/lib/x86_64-linux-gnu/crt1.o /usr/lib/x86_64-linux-gnu/crti.o /usr/lib/x86_64-linux-gnu/crtn.o ";
    cmd += "first.o -o first ";
    cmd += "-dynamic-linker /lib64/ld-linux-x86-64.so.2 -lc";
    system(cmd.c_str());
    
    return 0;
}

// Generate assemble and build
void assemble() {
    // We are going to generate for X86, so tell LLVM
    LLVMInitializeX86TargetInfo();
    LLVMInitializeX86Target();
    LLVMInitializeX86TargetMC();
    LLVMInitializeX86AsmParser();
    LLVMInitializeX86AsmPrinter();

    // Get the target triple so LLVM knows what to generate assembly for
    std::string triple = sys::getDefaultTargetTriple();
    mod->setTargetTriple(triple);
    
    // Look up the target
    std::string error;
    auto target = TargetRegistry::lookupTarget(triple, error);
    
    // Check for any errors with the target triple
    if (!target) {
        errs() << error;
        return;
    }
    
    // Setup the target writer
    auto CPU = "generic";
    auto features = "";
    
    TargetOptions options;
    auto RM = Optional<Reloc::Model>();
    auto machine = target->createTargetMachine(triple, CPU, features, options, RM);
    mod->setDataLayout(machine->createDataLayout());
    
    // Finally, generate assembly
    std::string outputPath = "./first.s";
    std::error_code errorCode;
    raw_fd_ostream writer(outputPath, errorCode, sys::fs::OF_None);
    
    if (errorCode) {
        errs() << "Unable to open file: " << errorCode.message();
        return;
    }
    
    legacy::PassManager pass;
    auto outputType = CGFT_AssemblyFile;
    
    if (machine->addPassesToEmitFile(pass, writer, nullptr, outputType)) {
        errs() << "Unable to write to file.";
        return;
    }
    
    pass.run(*mod);
    writer.flush();
}
```

