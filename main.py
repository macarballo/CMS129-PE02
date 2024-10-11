import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os


# Main application class
class CompilerUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Programming Exercise 02: Lexical Analysis for IOL")
        self.geometry("1200x600")
        self.configure(bg="#f0f0f0")
        self.font_style = ("Courier", 12)

        # File and Token Stream Paths
        self.file_path = None
        self.token_file_path = "output.tkn"

        # Create Menu Bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New File", command=self.new_file)
        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)

        # Create a frame for buttons and align them horizontally
        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=15)

        button_style = {
            "font": ("Courier", 12, "bold"),
            "bg": "#6A9FB5",
            "fg": "white",
            "relief": tk.RAISED,
            "bd": 2,
            "activebackground": "#55859B",
        }

        compile_button = tk.Button(button_frame, text="Compile Code", command=self.compile_code, **button_style)
        compile_button.pack(side=tk.LEFT, padx=15, ipadx=10, ipady=5)

        token_button = tk.Button(
            button_frame, text="Show Tokenized Code", command=self.show_tokenized_code, **button_style
        )
        token_button.pack(side=tk.LEFT, padx=15, ipadx=10, ipady=5)

        output_button = tk.Button(
            button_frame, text="Save Tokenized Output", command=self.save_token_file, **button_style
        )
        output_button.pack(side=tk.LEFT, padx=15, ipadx=10, ipady=5)

        # I/O Frame (for input code editor and output console)
        io_frame = tk.Frame(self, bg="#f0f0f0")
        io_frame.pack(padx=15, pady=15, expand=True, fill=tk.BOTH)

        # Code Editor Section (Left side)
        code_editor_frame = tk.Frame(io_frame, bg="#f0f0f0")
        code_editor_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        code_editor_label = tk.Label(
            code_editor_frame, text="Built-in Code Editor", font=("Courier", 12, "bold"), bg="#f0f0f0"
        )
        code_editor_label.pack(anchor=tk.NW, pady=(0, 10))

        self.editor_area = scrolledtext.ScrolledText(
            code_editor_frame,
            wrap=tk.WORD,
            height=12,
            width=50,
            font=("Courier", 12),
            bd=2,
            relief=tk.SUNKEN,
            padx=10,
            pady=10,
        )
        self.editor_area.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)

        # Tokenized Code Section (Right side of code editor)
        token_output_frame = tk.Frame(io_frame, bg="#f0f0f0")
        token_output_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        token_output_label = tk.Label(
            token_output_frame, text="Compiled Code Output", font=("Courier", 12, "bold"), bg="#f0f0f0"
        )
        token_output_label.pack(anchor=tk.NW, pady=(0, 10))

        self.output_area = scrolledtext.ScrolledText(
            token_output_frame,
            wrap=tk.WORD,
            height=12,
            width=50,
            font=("Courier", 12),
            bd=2,
            relief=tk.SUNKEN,
            padx=10,
            pady=10,
        )
        self.output_area.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)

        # Output Console Section (For tokenized code, below the editor and output)
        output_frame = tk.Frame(self, bg="#f0f0f0")
        output_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        output_label = tk.Label(
            output_frame, text="Built-in Console (Tokenized Code)", font=("Courier", 12, "bold"), bg="#f0f0f0"
        )
        output_label.pack(anchor=tk.NW, pady=(0, 10))

        self.console_area = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            height=8,
            width=100,
            font=("Courier", 12),
            bd=2,
            relief=tk.SUNKEN,
            padx=10,
            pady=10,
        )
        self.console_area.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)

        # Store token stream, error list, and variable details (name, type)
        self.token_stream = []
        self.error_list = []
        self.variables = {}

    def new_file(self):
        self.editor_area.delete(1.0, tk.END)
        self.file_path = None
        # Clear output and console areas when a new file is opened
        self.output_area.config(state='normal')
        self.output_area.delete(1.0, tk.END)
        self.output_area.config(state='disabled')
        self.console_area.config(state='normal')
        self.console_area.delete(1.0, tk.END)
        self.console_area.config(state='disabled')

    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("IOL files", "*.iol")])
        if self.file_path:
            with open(self.file_path, 'r') as file:
                code = file.read()
            self.editor_area.delete(1.0, tk.END)
            self.editor_area.insert(tk.END, code)

    def save_file(self):
        if self.file_path:
            with open(self.file_path, 'w') as file:
                file.write(self.editor_area.get(1.0, tk.END).strip())
            messagebox.showinfo("Info", "File saved successfully.")
        else:
            self.save_file_as()

    def save_file_as(self):
        self.file_path = filedialog.asksaveasfilename(defaultextension=".iol", filetypes=[("IOL files", "*.iol")])
        if self.file_path:
            with open(self.file_path, 'w') as file:
                file.write(self.editor_area.get(1.0, tk.END).strip())
            messagebox.showinfo("Info", "File saved successfully.")

    def compile_code(self):
        code = self.editor_area.get(1.0, tk.END).strip()
        if not code:
            messagebox.showwarning("Warning", "Input program code is empty.")
            return

        # Perform lexical analysis
        self.token_stream = self.lexical_analysis(code)
        self.output_area.delete(1.0, tk.END)  # Clear output area
        self.console_area.delete(1.0, tk.END)  # Clear token console

        if self.error_list:
            self.display_lexical_errors()
        else:
            self.output_area.insert(tk.END, "Compilation successful! No lexical errors found.\n\n")
            self.display_variables_table()

    def show_tokenized_code(self):
        if not self.token_stream:
            messagebox.showinfo("Info", "No tokenized code available. Compile the code first.")
            return

        self.console_area.delete(1.0, tk.END)
        token_content = ""
        current_line = 1
        for lexeme, token in self.token_stream:
            if token == "NEWLN":
                current_line += 1
            token_content += f"Line {current_line}: {lexeme} -> {token}\n"
        self.console_area.insert(tk.END, token_content)

    def save_token_file(self):
        if not self.token_stream:
            messagebox.showwarning("Warning", "No tokenized output available. Compile the code first.")
            return

        token_content = "\n".join(f"{lexeme} -> {token}" for lexeme, token in self.token_stream)
        with open(self.token_file_path, "w") as file:
            file.write(token_content)
        messagebox.showinfo("Info", f"Tokenized output saved as {self.token_file_path}.")

    def lexical_analysis(self, code):
        tokens = []
        self.error_list = []
        # Define keywords and types
        keywords = {"IOL", "LOI", "INTO", "IS", "BEG", "NEWLN", "PRINT", "ADD", "SUB", "MULT", "DIV", "MOD"}
        types = {"INT", "STR"}
        lines = code.splitlines()

        for line_num, line in enumerate(lines, start=1):
            words = line.split()
            if not words:
                continue

            for i, word in enumerate(words):
                # Check if the word is a keyword or a type (INT or STR)
                if word in keywords or word in types:
                    tokens.append((word, word))
                    # Handle variable declaration if a type is encountered
                    if word in types and i + 1 < len(words):
                        var_name = words[i + 1]
                        if var_name.isidentifier():
                            default_value = 0 if word == "INT" else "Unassigned"
                            self.variables[var_name] = {"type": word, "value": default_value}
                            tokens.append((var_name, "IDENT"))
                        else:
                            self.error_list.append(f"Invalid identifier '{var_name}' on line {line_num}")
                # Check if the word is a valid integer literal
                elif word.isdigit():
                    tokens.append((word, "INT_LIT"))
                # Check if the word is a valid identifier
                elif word.isidentifier():
                    tokens.append((word, "IDENT"))
                # If the word does not match any valid token, mark it as an error
                else:
                    tokens.append((word, "ERR_LEX"))
                    self.error_list.append(f"Unknown lexeme '{word}' on line {line_num}")

        return tokens

    def display_lexical_errors(self):
        error_msg = "Lexical Errors:\n"
        error_msg += "\n".join(self.error_list)
        self.output_area.insert(tk.END, error_msg)

    def display_variables_table(self):
        # Calculate the longest variable name for dynamic column width
        max_var_length = max((len(var) for var in self.variables), default=8)
        var_col_width = max(max_var_length, len("Variable")) + 2
        type_col_width = max(len("Type"), 10) + 2
        value_col_width = max(len("Value"), 15) + 2

        # Clear the info area and add the header for the table
        self.output_area.delete(1.0, tk.END)
        header = f"{'Variable':<{var_col_width}} {'Type':<{type_col_width}} {'Value':<{value_col_width}}\n"
        self.output_area.insert(tk.END, header)
        self.output_area.insert(tk.END, "-" * (var_col_width + type_col_width + value_col_width) + "\n")

        # Display each variable with its name, type, and value
        for variable, details in self.variables.items():
            var_type = details.get("type", "Unassigned")
            value = details.get("value", "Unassigned")
            row = f"{variable:<{var_col_width}} {var_type:<{type_col_width}} {value:<{value_col_width}}\n"
            self.output_area.insert(tk.END, row)


if __name__ == "__main__":
    app = CompilerUI()
    app.mainloop()
