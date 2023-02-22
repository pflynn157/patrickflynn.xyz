---
title: "Lex: The Entry to a Compiler"
date: "2021-09-26"
categories: 
  - "compilers"
  - "lexical-analysis"
  - "tutorial"
---

Welcome! Today we're going to dive into our first hands-on project in developing a compiler component. We're going to write a very simple lexer, which forms the first part of a language parser. The good news about this project is in addition to being the first part of a compiler, its also one of the easiest parts to write.

This will be divided into two posts. In this post, I will talk about what the lexer does and the overall concept of implementing it. Next week, we will write an actual working lexer in C++.

Let's dive in!

### What is a Lexer?

A lexer, or scanner, is a program that performs lexical analysis on a file or a string. Lexical analysis is the process of breaking down that file or string into a stream of tokens. These tokens are then used by a parser to determine the meaning or intent of the input file.

Lexical analysis is the first part of the compilation process. A lexer takes the source file and reads it, subdividing it into tokens. These tokens are passed to the parser, which uses them to construct an abstract syntax tree representing the source file. The rest of the compiler analyzes this syntax tree and eventually generates assembly code.

Lexical analysis is the easiest part of the compilation process (provided you know how to parse strings). Lexical tokens are also make up the easiest IR in the compiler. A lexical analyzer does very little, if any error reporting beyond possible file IO errors. All it does is return tokens. It is the job of the parser and later analyzers to check for correctness and report syntax errors. Because you are freed from this overhead, writing the lexical analyzer is a pretty straightforward process.

### A Hands-On Example

As mentioned at the beginning of the post, actual code will follow later. Let's consider a pseudo-code example. As our input, consider this line of code:

```
int x = 20;
```

Let's break this down. The first token is "int". It is a keyword, so we simply return a numerical value representing the integer keyword (in most languages, this is done with enumerated structures). Now let's look at the next token. "X" is a variable name- an identifier. Provided that the name is valid in the language (and it is), this token will represent something to the user but not necessarily the programming language (hence the name identifier). In this case, the lexer returns the Identifier token, and a string with the variable name.

The next token is the assignment operator. While it depends on the lexer, either the character itself or an enumerated value is returned. The next token is "20"- a numerical literal. Because this is in the file, it is text, so we don't know right off that its a number. Therefore, we perform a check, and if the string is a number, we convert it to an integer value, and return a token with both. Finally, we have the terminator- the semicolon. This is returned much like the assignment operator.

### Types of Tokens

The types of tokens you have will depend on the language you are parsing and how you structure the lexer itself. If you read the Wikipedia article on lexical analysis, you will notice there are six categories: identifier, keyword, operator, separator, literal, and comment.

Tokens should not be returned for comments. If you encounter a comment, you simply read text until you reach the end of a comment (a newline character in the case of single line comments, or some other terminator for multi-line comments).

In practice, operators and separators can be grouped into the same categories, depending on meaning. If you do have separators that the parser should never honor- ie, spaces between keywords, whitespace, etc, it is the lexer's job to ignore them before it gets to the parser.

Finally, there's keywords and literals. In many cases, it will be hard to tell the difference right off. When you reach a point where you have to determine what is what, the best way is to check for keywords first; literals second; and identifiers third. In many cases, identifiers can best be thought of as anything that is not a keyword or a literal.

### An Overview of the Lexer

Below is a pseudo-code overview of what a lexer could look like:

```
string buffer;
stack tokenStack;
while charsToRead() {
    if not tokenStack.isEmpty() {
        return tokenStack.pop();
    }
    char c = getChar();
    if isSeparator(c) or isOperator(c) {
        if isOperator(c) {
            Token token = getOperator(c);
            tokenStack.push(token);
        }
        Token token;
        if isKeyword(buffer) {
            token = getKeyword(buffer);
        } else if isInt(buffer) {
            token = INT;
            token.intVal = convInt(buffer);
        } else {
            token = ID;
            token.idVal = buffer;
        }
        buffer = "";
        return token;
    } else {
        buffer += c;
    }
}
```

Now, please understand that this is greatly simplified- probably over-simplified. While this analyzes many common tokens, there are many that it doesn't take into account such as string, character, hex, or float literals. But you should be able to see the overall flow here. The key to getting the lexer correct is the buffer variable. The buffer holds the current text, and is reset only after we find a keyword, literal, or identifier.

The token stack can be a little tricky to understand at first. But consider our line of code above. What happens when we hit this: `x=` (note lack of space).

The '=' is an operator- the assignment operator. But this is stuff on the buffer- "x"- the variable name. Both the variable name and the operator are valid tokens, but we can't return both at once. Moreover, they need to be processed one at a time, in the order that they were found.

This is where the stack comes in. Since the identifier came first, this is returned immediately. The operator token, meanwhile, is pushed to the stack. When the lexer is called again, because there is now a token on the stack, the lexer will skip reading more of the file altogether and return what's in the stack.

### Conclusion

I understand that for many people, trying to digest theory without code can be a little challenging. However, it is important to understand the big picture first, so hopefully this made sense and gave you the general idea. In the next post, we will start writing a simple lexer that will put these concepts in practice.

See you then!

