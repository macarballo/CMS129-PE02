import tkinter as tk
from tkinter import filedialog, scrolledtext

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
        button_style = {"font": ("Segoe UI", 12, "bold"), "bg": "#6A9FB5", "fg": "white", "relief": tk.RAISED, "bd": 2, "activebackground": "#55859B"}

        # Create Compile button
        compile_button = tk.Button(button_frame, text="Compile Code", command=self.compile_code, **button_style)
        compile_button.pack(side=tk.LEFT, padx=15, ipadx=10, ipady=5)

        # Create Tokenized Code button
        token_button = tk.Button(button_frame, text="Show Tokenized Code", command=self.show_tokenized_code, **button_style)
        token_button.pack(side=tk.LEFT, padx=15, ipadx=10, ipady=5)

        # Create a frame to hold both input and output sections horizontally
        io_frame = tk.Frame(self, bg="#f0f0f0")
        io_frame.pack(padx=15, pady=15, expand=True, fill=tk.BOTH)

        # Input area with label
        input_frame = tk.Frame(io_frame, bg="#f0f0f0")
        input_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        input_label = tk.Label(input_frame, text="Input Program Code", font=("Segoe UI", 12, "bold"), bg="#f0f0f0")
        input_label.pack(anchor=tk.NW, pady=(0, 10))

        self.editor_area = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=20, width=50, font=("Consolas", 12), bd=2, relief=tk.SUNKEN, padx=10, pady=10)
        self.editor_area.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)

        # Output area with label
        output_frame = tk.Frame(io_frame, bg="#f0f0f0")
        output_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        output_label = tk.Label(output_frame, text="Output / Information", font=("Segoe UI", 12, "bold"), bg="#f0f0f0")
        output_label.pack(anchor=tk.NW, pady=(0, 10))

        self.info_area = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=20, width=50, font=("Consolas", 12), bd=2, relief=tk.SUNKEN, padx=10, pady=10)
        self.info_area.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)

    # Functions for menu actions
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("IOL files", "*.iol")])
        if file_path:
            with open(file_path, 'r') as file:
                code = file.read()
            self.editor_area.delete(1.0, tk.END)  # Clear current content
            self.editor_area.insert(tk.END, code)  # Insert file content into editor

    def compile_code(self):
        # Placeholder for lexical analysis function
        # - Scans and tokenizes the code from the editor area
        # - Replaces lexemes with tokens
        # - Displays error messages in the info area for lexical errors
        # - Outputs a .tkn file with the token stream
        # - Displays a list of variables in the output section
        pass

    def show_tokenized_code(self):
        # Placeholder to display the tokenized version of the code
        # - Fetch tokenized code (from compile_code)
        # - Display it in the info_area
        pass

    # Additional methods for functionalities can be added here:
    def save_token_file(self, token_stream):
        # Placeholder to save tokenized code to a .tkn file
        pass

    def display_variables_table(self):
        # Placeholder to display the variables and types table in the output area
        pass

    def display_lexical_errors(self, error_list):
        # Placeholder to display lexical errors with line numbers in the output area
        pass

if __name__ == "__main__":
    app = CompilerUI()
    app.mainloop()