import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox


# Main application class
class CompilerUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Programming Exercise 02: Lexical Analysis")
        self.geometry("1000x600")
        self.configure(bg="#f0f0f0")  # Set a light gray background for the window
        self.font_style = ("Segoe UI", 12)  # Modern font for consistent styling

        # Create Menu Bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open File", command=self.open_file)

        # Create a frame for buttons and align them horizontally
        button_frame = tk.Frame(self, bg="#f0f0f0")  # Match background color
        button_frame.pack(pady=15)

        # Button styling (softer colors)
        button_style = {
            "font": ("Segoe UI", 12, "bold"),
            "bg": "#6A9FB5",
            "fg": "white",
            "relief": tk.RAISED,
            "bd": 2,
            "activebackground": "#55859B",
        }

        # Create Compile button
        compile_button = tk.Button(button_frame, text="Compile Code", command=self.compile_code, **button_style)
        compile_button.pack(side=tk.LEFT, padx=15, ipadx=10, ipady=5)

        # Create Tokenized Code button
        token_button = tk.Button(
            button_frame, text="Show Tokenized Code", command=self.show_tokenized_code, **button_style
        )
        token_button.pack(side=tk.LEFT, padx=15, ipadx=10, ipady=5)

        # Create a frame to hold both input and output sections horizontally
        io_frame = tk.Frame(self, bg="#f0f0f0")
        io_frame.pack(padx=15, pady=15, expand=True, fill=tk.BOTH)

        # Input area with label
        input_frame = tk.Frame(io_frame, bg="#f0f0f0")
        input_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        input_label = tk.Label(input_frame, text="Input Program Code", font=("Segoe UI", 12, "bold"), bg="#f0f0f0")
        input_label.pack(anchor=tk.NW, pady=(0, 10))

        self.editor_area = scrolledtext.ScrolledText(
            input_frame,
            wrap=tk.WORD,
            height=20,
            width=50,
            font=("Consolas", 12),
            bd=2,
            relief=tk.SUNKEN,
            padx=10,
            pady=10,
        )
        self.editor_area.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)

        # Output area with label
        output_frame = tk.Frame(io_frame, bg="#f0f0f0")
        output_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        output_label = tk.Label(output_frame, text="Output / Information", font=("Segoe UI", 12, "bold"), bg="#f0f0f0")
        output_label.pack(anchor=tk.NW, pady=(0, 10))

        self.info_area = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            height=20,
            width=50,
            font=("Consolas", 12),
            bd=2,
            relief=tk.SUNKEN,
            padx=10,
            pady=10,
        )
        self.info_area.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)

        # Store token stream and error list
        self.token_stream = []
        self.error_list = []

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("IOL files", "*.iol")])
        if file_path:
            with open(file_path, 'r') as file:
                code = file.read()
            self.editor_area.delete(1.0, tk.END)
            self.editor_area.insert(tk.END, code)

    def compile_code(self):
        code = self.editor_area.get(1.0, tk.END).strip()
        if not code:
            messagebox.showwarning("Warning", "Input program code is empty.")
            return

        # Perform lexical analysis
        self.token_stream = self.lexical_analysis(code)
        self.info_area.delete(1.0, tk.END)

        if self.error_list:
            self.display_lexical_errors()
        else:
            self.info_area.insert(tk.END, "Compilation successful! No lexical errors found.\n")
            self.display_variables_table()
            self.save_token_file()

    def lexical_analysis(self, code):
        tokens = []
        self.error_list = []
        # Example: Simple scanner to detect keywords, identifiers, integer literals, operators, and errors
        keywords = {"DEFINE", "INTO", "IS"}
        operators = {"+", "-", "*", "/", "=", "(", ")"}
        lines = code.splitlines()

        for line_num, line in enumerate(lines, start=1):
            for word in line.split():
                if word in keywords:
                    tokens.append((word, word))
                elif word in operators:
                    tokens.append((word, "OPERATOR"))
                elif word.isdigit():
                    tokens.append((word, "INT_LIT"))
                elif word.isidentifier():
                    tokens.append((word, "IDENT"))
                else:
                    tokens.append((word, "ERR_LEX"))
                    self.error_list.append(f"Unknown lexeme '{word}' on line {line_num}")

        return tokens

    def show_tokenized_code(self):
        if not self.token_stream:
            messagebox.showinfo("Info", "No tokenized code available. Compile the code first.")
            return

        self.info_area.delete(1.0, tk.END)
        for lexeme, token in self.token_stream:
            self.info_area.insert(tk.END, f"{lexeme}: {token}\n")

    def save_token_file(self):
        token_content = "\n".join(f"{lexeme} -> {token}" for lexeme, token in self.token_stream)
        with open("output.tkn", "w") as file:
            file.write(token_content)

    def display_variables_table(self):
        variables = [lexeme for lexeme, token in self.token_stream if token == "IDENT"]
        self.info_area.insert(tk.END, "Variables detected:\n")
        for variable in variables:
            self.info_area.insert(tk.END, f"{variable}: IDENT\n")

    def display_lexical_errors(self):
        self.info_area.insert(tk.END, "Lexical Errors found:\n")
        for error in self.error_list:
            self.info_area.insert(tk.END, f"{error}\n")


if __name__ == "__main__":
    app = CompilerUI()
    app.mainloop()
