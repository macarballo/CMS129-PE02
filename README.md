# Programming Exercise 02 - Lexical Analysis

## Overview
This program implements a simple lexical analyzer as a part of a custom compiler for a programming language. The program reads a source code written in the custom programming language, performs lexical analysis by tokenizing the code, and outputs both the tokenized code and any lexical errors detected.

The program is built using Python's **tkinter** library to provide a graphical user interface (GUI), where users can input code, compile it, and see the results of lexical analysis.

## Features
- **Open File**: Load a source code file (.iol extension) into the editor.
- **Compile Code**: Analyze the input program code, perform lexical analysis, and display tokenization results.
- **Show Tokenized Code**: Display the tokenized version of the input program.
- **Error Handling**: Detect and display lexical errors, including unknown lexemes and line numbers where they occur.
- **Variable Table**: List all variables and their corresponding types after the code is compiled.
- **Save Token File**: The tokenized code can be saved to a .tkn file.

## Program Flow
1. **Open File or New File**: Users can load a program code from a file or manually enter code in the editor.
2. **Compile Code**: When the "Compile Code" button is clicked, the program performs lexical analysis on the input.
3. **Display Results**:
   - Lexical errors (if any) are displayed in the output area.
   - The list of variables and their types is shown in a table.
4. **Show Tokenized Code**: Clicking this button will display the tokenized form of the input program in the output area.
5. **Save Token File**: The tokenized code can be saved for future reference as a .tkn file.
