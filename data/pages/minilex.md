---
title: "MiniLex"
date: "2022-05-16"
template:page
output:minilex
menu: false
---

Welcome to MiniLex! This is one of my newer projects, and started out mainly as a project of necessity. Nevertheless, it still seems to be working well. As its name may apply, MiniLex is a lexical analyzer generator. In some ways, its inspired by the classic Lex/Flex Unix programs. You can find the source code [here](https://github.com/pflynn157/minilex).

Despite the great variety of programming languages in existence, many principles are similar regardless of the language. One of them is the lexical analyzer component. Whether you are parsing C, C++, Python, HTML, or something else, the lexical analyzer will be fairly similar. The only difference lies in the keywords and symbols that define the language. As a result, once you have a fairly good lexical analyzer, you can adapt to other projects easily.

That’s where MiniLex came from. The lexical analyzer it generates began life in the Tiny programming language. Since then, I’ve been copying it to new projects and changing things as needed. As I was starting a new project that required a lexical analyzer, I began thinking that I could write a generator without a lot of effort. And thus, MiniLex was born.

MiniLex only generates a C++ lexical analyzer at the moment. MiniLex itself is written in Python.

### How To Use

Using MiniLex is very easy. First, download and install it. Then, create a file something like this:

```
##
## This is an example of a user-generated configuration file for
## minilex.
##

output\_path = "./src"

# Define the keywords
keywords = \[
    ("func", "Func"), ("is", "Is"), ("end", "End"),
    ("var", "Var"), ("return", "Return")
\]

# Define the symbols
symbols = \[
    (";", "SemiColon"), ("=", "Assign"), (":", "Colon"), (":=", "Assign2"), ("!=", "NEQ")
\]

# Define single-line comments
single\_comments = \[ "#", "//" \]

# Define multi-line comments
multi\_comments = \[ ("\*/", "\*/") \]
```

As you can probably see, this file is basically a Python file. Originally, minilex used a custom file format, but for consistency and ease of use, I decided to change it Python. This config file is imported as a Python module, and the variables are referenced directly in the generator. The output\_path defaults to "./src" if not specified, but all others variables are required. The generator will fail if they are not specified. Minilex looks for "config.py" by default. However, you can specify your own path and module name.

For keywords and symbols, each token is specified with a tuple of strings. The left value of the tuple is the keyword or symbol, and the right value is the generated token name. Single line comments are simply a list of tokens. Multi-line comments are a list of tuples, with the left value being the opening token, and the right value being the closing token.

Three files are generated:

- lex.cpp
- lex\_debug.cpp
- lex.hpp

“lex.hpp” defines the Scanner class and the Token structures. You want to include this file in places where the scanner is needed. “lex\_debug.cpp” contains simple debug code for printing the tokens. This is useful when writing parsers and debugging the lexical analyzer itself. Finally, “lex.cpp” contains the actual lexical analyzer.

To run, use this command:

```
# Defaults to ./config.py
minilex

# Optionally if you're using a custom path (DO NOT include .py)
# Assumes module is in ./src/lex/lex.py
minilex src/lex/lex
```

### The Lexical Analyzer

Token types are represented in this enumeration. These are the default tokens provided in every generated instance of the lexical analyzer.

```
enum TokenType {
    EmptyToken,
    Eof,
     
    //##TOKEN LIST
     
    // Literals
    Id,
    String,
    CharL,
    Int32
};
```

And this is the corresponding structure representing a token. It contains the essential “type” field containing the token type, and several optional fields used to hold identifier and literal values as needed.

```
struct Token {
    TokenType type;
    std::string id\_val;
    char i8\_val;
    int i32\_val;
     
    Token();
    void print();
};
```

This is an example of how to use the scanner class. All it does is read every token from the file and print it out.

```
#include <iostream>
#include <string>
 
#include "lex.hpp"
 
int main(int argc, char \*argv\[\]) {
    if (argc == 1) {
        std::cerr << "Error: No input file" << std::endl;
        return 1;
    }
     
    std::string input = argv\[1\];
     
    Scanner \*scanner = new Scanner(input);
    Token token = scanner->getNext();
    while (token.type != Eof) {
        token.print();
        token = scanner->getNext();
    }
    token = scanner->getNext();
     
    return 0;
}
```

### Future Work

Currently, this works well enough for the needs of my projects, so I’m not going to add anymore at the moment. That doesn’t mean I won’t. As I use it more, I may add things I end up needing.


