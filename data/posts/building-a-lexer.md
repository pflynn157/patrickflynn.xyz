---
title: "Building a Lexer"
date: "2021-10-03"
categories: 
  - "compilers"
  - "lexical-analysis"
  - "tutorial"
---

Welcome back!

As promised in the last post, this post will contain an actual hands-on example in creating a lexical analyzer. You can find the complete program at the end of this post. Through the post, I will break it down into digestible parts so you can understand how it works and hopefully better understand the greater concept behind this.

### Token Structure

While there are probably different ways to do this, my preferred method is to use a structure and an enumeration to represent tokens. Here are the structures:

```
enum TokenType {
    None,
    Eof,
    
    Int,
    
    Assign,
    SemiColon,
    
    Id,
    IntL
};

// The token structure. This holds all the information about the token.
struct Token {
    TokenType type;
    std::string idVal;
    int intVal;
};
```

The structure is what actually gets returned. The `TokenType` enumeration represents the token itself. The enumeration is important. Enumerations are basically named integer values, which is ideal for comparisons. This is what the parser uses to determine what type of token its looking at, and where to go from there.

As you may remember, some tokens represent identifiers and literals, so the parser will not only need to know what type of token it has, but also what the content of the token is. That's where the structure comes in. If the token is an identifier, the "idVal" struct member will be set. If the token is an integer literal, the "intVal" member will be set. And so on.

I've read that some lexers use functions to store the current buffer or something like that, but I find that this solution works the best. I've never measured performance, but realistically, I can't see it being worse than other methods as long as you don't start heap-allocating things.

### Why a Class?

Okay, let's talk about the structure. You may have noticed that I wrapped everything into a class:

```
class Scanner {
public:
    explicit Scanner(std::string input) {
        this->input = input;
    }
    
    bool isSymbol(char c);
    bool isInteger();
    TokenType getSymbol(char c);
    TokenType getKeyword();
    
    Token getNext();

    bool isEof();
    char getChar();
private:
    // Control variables needed by our class
    std::stack<Token> tokenStack;
    std::string buffer = "";
    
    std::string input;
    int pos = 0;
};
```

While object-oriented programming isn't my favorite thing ever, this is one area where I think it shines. In general, I think OOP is a well-suited to compilers since it can represent various inter\-relationships among components. But that's another topic for another day...

Anyway. I highly recommend that you wrap your scanner and all its component functions into a structure of some sort. Classes in C++, Java, and C\# are best. In Rust, I used a structure, which worked really, really well. Doing so will allow easy access amongst your functions to the buffer, the file reader, the token stack, and so forth. Moreover, it makes for a cleaner design since you are not having to pass stuff all over the place.

### Scanning

Ok, let's talk about this function:

```
Token Scanner::getNext()
```

This was something that actually threw me off back in my early compiler days. I thought parsers wanted a list of tokens returned, not one at a time. But in fact, this method works the best. When you read one token at a time, that sets things up for what to read next- what path to take in the parser (ie, do we have a variable declaration, function call, or something else?). If this doesn't make sense to you right off, don't worry; its not essential for understanding this post.

The "getNext()" routine starts with these two if-statements:

```
    if (tokenStack.size() > 0) {
        Token token = tokenStack.top();
        tokenStack.pop();
        return token;
    }

    if (isEof()) {
        Token token;
        token.type = Eof;
        return token;
    }
```

When the function is called, the very first thing we need to do is check the token stack. Even if we're at the end of the file, we should return tokens until the stack is completely empty. The next if-statement checks to see if we're at the end of the file. If we are, we return a token for that.

Next, we arrive at our loop:

```
    while (!isEof()) {
    
        // Get the next character in the input stream
        char next = getChar();
        
        // If we find a separator or a symbol, its time to do work!
        if (next == ' ' || isSymbol(next)) {
            // DO WORK....

        // Otherwise, just add the current character to the buffer
        } else {
            buffer += next;
        }
    }
```

Ideally, the base case of the loop should never be reached, but it's there as a safeguard to prevent infinite loops. Inside the loop, the first thing we do is get the next character. If the next character is a separator (a space) or a symbol (ie, '=' or ';'), then we need to stop and analyze. Otherwise, the character is part of a larger token, so we add it to the buffer.

Once inside the loop, we need to do a variety of checks. This code probably could be cleaner, but for explanation its better as is:

```
            // See if we have a symbol. If so, we need to create a token
            if (isSymbol(next)) {
                Token token;
                token.type = getSymbol(next);
                
                // If the buffer is empty, we can return the token immediately. Otherwise,
                // it needs to go on the stack.
                if (buffer.length() == 0) {
                    return token;
                } else {
                    tokenStack.push(token);
                }
            }
            
            // If the buffer is empty, don't do anything- just continue.
            if (buffer.length() == 0) {
                continue;
            }
```

All this code handles scenarios where a symbol representing a valid token follows another token, such as a keyword or an identifier. The first if-statement verifies that the symbol is a valid token, and if so, it will build that token. Now, if the buffer is empty (ie, a token following a token or a separator), we can return the token immediately. Otherwise, it needs to go on the stack so we can process the buffer. The next if-statement just checks to see if the buffer is empty (ie, two spaces were found). If the buffer is empty, we just continue on with the loop.

Once we have completed the symbol check and verified that something is in the buffer, we can check the buffer itself:

```
            // Check the buffer to see whether we have a keyword, literal, or identifier
            // An identifier is the default case
            Token token;
             
            if (getKeyword() != None) {
                token.type = getKeyword();
            } else if (isInteger()) {
                token.type = IntL;
                token.intVal = std::stoi(buffer);
            } else {
                token.type = Id;
                token.idVal = buffer;
            }
             
            buffer = "";
            return token;
```

This check is pretty straightforward. First, we need to see if we have a keyword. This should come first, as keywords have precedence over other tokens. Next, we check on literals. In this case, we are only checking for numerical literals, but in real life, you would need to check for things like floating point and hexadecimal literals. Finally, if all else fails, we have an identifier. If your language has rules of what does and does not constitute a valid identifier, this would be a good place to check. Bear in mind though that if you do, you will need error handling on this level.

See the full code listing for how these check functions are carried out. At the end, we clear the buffer and return the token.

### The Driver

Now for testing. Ideally this would be part of a parser, but we just want to see if it works. Here's the code:

```
// The driver function for testing our lexical analyzer
int main() {
    std::cout << "Enter a line to analyze:" << std::endl;
     
    std::string line = "";
    std::getline(std::cin, line);
     
    Scanner scanner(line);
     
    Token token = scanner.getNext();
    while (token.type != Eof) {
        switch (token.type) {
            case Short: std::cout << "Keyword: short" << std::endl; break;
            case Int: std::cout << "Keyword: int" << std::endl; break;
             
            case Assign: std::cout << "Symbol: \\'=\\'" << std::endl; break;
            case SemiColon: std::cout << "Symbol: \\';\\'" << std::endl; break;
             
            case Id: std::cout << "Identifier: " << token.idVal << std::endl; break;
            case IntL: std::cout << "Integer Literal: " << token.intVal << std::endl; break;
             
            default: {
                std::cout << "Error: Unknown token." << std::endl;
            }
        }
         
        token = scanner.getNext();
    }
     
    std::cout << "EOF reached." << std::endl;
     
    return 0;
}
```

As you can see, its pretty straightforward. We simply get an input string from the console, feed it to the lexer, and get each token out one by one. The loop runs until it's out of tokens to read. Experiment with it- see what works and what doesn't. As a bonus, try adding some of your own symbols or keywords, and see what happens.

To compile, any C++ compiler will work. No special libraries or flags are needed.

### Full Listing

Below is the full code listing. This code is in the public domain.

```
// Goal: Parse this: int x = 20;
 
#include <iostream>
#include <string>
#include <stack>
#include <cctype>
 
// An enumeration representing the types of tokens we could have
// We use an enum because its easy to understand, and allows for quick
// comparisons in the parser.
enum TokenType {
    None,
    Eof,
     
    Short,
    Int,
     
    Assign,
    SemiColon,
     
    Id,
    IntL
};
 
// The token structure. This holds all the information about the token.
struct Token {
    TokenType type;
    std::string idVal;
    int intVal;
};
 
// Its best to wrap the scanner into a pass. In real life, this should
// be separated into a header and source file, but since this is an
// example, its sufficient to do it like this.
class Scanner {
public:
    // In real life, the scanner would read directly from the file. Again, since this
    // is an example, things are different. The first three functions are used to simulate
    // common file functions that the lexer would use.
    explicit Scanner(std::string input) {
        this->input = input;
    }
     
    bool isEof() {
        if (pos >= input.length()) return true;
        return false;
    }
     
    char getChar() {
        if (isEof()) return 0;
        char c = input\[pos\];
        ++pos;
        return c;
    }
     
    // Checks to see whether the given character is a symbol or not
    bool isSymbol(char c) {
        switch (c) {
            case '=':
            case ';': return true;
             
            default: return false;
        }
    }
     
    // Checks to see if a given string is an integer literal
    bool isInteger() {
        for (char c : buffer) {
            if (!isdigit(c)) return false;
        }
        return true;
    }
     
    // Returns the corresponding token type for a given character
    // Because of the isSymbol() function, we should never get to the
    // default case.
    TokenType getSymbol(char c) {
        switch (c) {
            case '=': return Assign;
            case ';': return SemiColon;
             
            default: return None;
        }
    }
    
    // Returns a keyword for the buffer, or empty otherwise
    TokenType getKeyword() {
        if (buffer == "short") return Short;
        else if (buffer == "int") return Int;
        return None;
    }
     
    Token getNext();
private:
    // Control variables needed by our class
    std::stack<Token> tokenStack;
    std::string buffer = "";
     
    std::string input;
    int pos = 0;
};
 
// The main lexical routine
Token Scanner::getNext() {
     
    // First, check the stack. If there are tokens on it, pop one and return
    if (tokenStack.size() > 0) {
        Token token = tokenStack.top();
        tokenStack.pop();
        return token;
    }
     
    // Make sure we're not at the end of the file
    // If we are, send an end-of-file token.
    if (isEof()) {
        Token token;
        token.type = Eof;
        return token;
    }
     
    // Continue looping until we either find a token or hit the end of the file.
    // If we hit the end of the file, something is probably wrong.
    while (!isEof()) {
     
        // Get the next character in the input stream
        char next = getChar();
         
        // If we find a separator or a symbol, its time to do work!
        if (next == ' ' || isSymbol(next)) {
             
            // See if we have a symbol. If so, we need to create a token
            if (isSymbol(next)) {
                Token token;
                token.type = getSymbol(next);
                 
                // If the buffer is empty, we can return the token immediately. Otherwise,
                // it needs to go on the stack.
                if (buffer.length() == 0) {
                    return token;
                } else {
                    tokenStack.push(token);
                }
            }
             
            // If the buffer is empty, don't do anything- just continue.
            if (buffer.length() == 0) {
                continue;
            }
             
            // Check the buffer to see whether we have a keyword, literal, or identifier
            // An identifier is the default case
            Token token;
             
            if (getKeyword() != None) {
                token.type = getKeyword();
            } else if (isInteger()) {
                token.type = IntL;
                token.intVal = std::stoi(buffer);
            } else {
                token.type = Id;
                token.idVal = buffer;
            }
             
            buffer = "";
            return token;
             
        // Otherwise, just add the current character to the buffer
        } else {
            buffer += next;
        }
    }
    
    Token token;
    token.type = None;
    return token;
}
 
// The driver function for testing our lexical analyzer
int main() {
    std::cout << "Enter a line to analyze:" << std::endl;
     
    std::string line = "";
    std::getline(std::cin, line);
     
    Scanner scanner(line);
     
    Token token = scanner.getNext();
    while (token.type != Eof) {
        switch (token.type) {
            case Short: std::cout << "Keyword: short" << std::endl; break;
            case Int: std::cout << "Keyword: int" << std::endl; break;
             
            case Assign: std::cout << "Symbol: \\'=\\'" << std::endl; break;
            case SemiColon: std::cout << "Symbol: \\';\\'" << std::endl; break;
             
            case Id: std::cout << "Identifier: " << token.idVal << std::endl; break;
            case IntL: std::cout << "Integer Literal: " << token.intVal << std::endl; break;
             
            default: {
                std::cout << "Error: Unknown token." << std::endl;
            }
        }
         
        token = scanner.getNext();
    }
     
    std::cout << "EOF reached." << std::endl;
     
    return 0;
}
```

