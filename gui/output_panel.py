
import tkinter as tk
from tkinter import ttk


class OutputPanel(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            bg="#1e1e1e",
            **kwargs
        )

        self.configure(highlightthickness=0)

        self.create_styles()
        self.create_interface()

    # ---------------------------------------------------------
    # STYLES
    # ---------------------------------------------------------

    def create_styles(self):
        self.style = ttk.Style()

        self.style.configure(
            "Output.TNotebook",
            background="#1e1e1e",
            borderwidth=0
        )

        self.style.configure(
            "Output.TNotebook.Tab",
            background="#252526",
            foreground="#cccccc",
            padding=(16, 8),
            font=("Segoe UI", 9)
        )

        self.style.map(
            "Output.TNotebook.Tab",
            background=[
                ("selected", "#1e1e1e"),
                ("active", "#333333")
            ],
            foreground=[
                ("selected", "#ffffff"),
                ("active", "#ffffff")
            ]
        )

    # ---------------------------------------------------------
    # MAIN INTERFACE
    # ---------------------------------------------------------

    def create_interface(self):
        self.header = tk.Frame(
            self,
            bg="#252526",
            height=38
        )
        self.header.pack(fill=tk.X)
        self.header.pack_propagate(False)

        self.title_label = tk.Label(
            self.header,
            text="CONSOLE",
            bg="#252526",
            fg="#cccccc",
            font=("Segoe UI", 9, "bold")
        )
        self.title_label.pack(
            side=tk.LEFT,
            padx=14
        )

        self.clear_button = tk.Button(
            self.header,
            text="Clear",
            command=self.clear_all,
            bg="#252526",
            fg="#cccccc",
            activebackground="#3c3c3c",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0,
            cursor="hand2",
            font=("Segoe UI", 9),
            padx=10
        )
        self.clear_button.pack(
            side=tk.RIGHT,
            padx=8
        )

        self.notebook = ttk.Notebook(
            self,
            style="Output.TNotebook"
        )
        self.notebook.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.create_input_tab()
        self.create_output_tab()
        self.create_messages_tab()

    # ---------------------------------------------------------
    # REUSABLE TEXT AREA
    # ---------------------------------------------------------

    def create_text_area(self, parent, readonly=False):
        container = tk.Frame(
            parent,
            bg="#1e1e1e"
        )

        container.pack(
            fill=tk.BOTH,
            expand=True
        )

        text_widget = tk.Text(
            container,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#ffffff",
            selectbackground="#264f78",
            selectforeground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0,
            padx=12,
            pady=10,
            undo=True
        )

        scrollbar = ttk.Scrollbar(
            container,
            orient=tk.VERTICAL,
            command=text_widget.yview
        )

        text_widget.configure(
            yscrollcommand=scrollbar.set
        )

        text_widget.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        if readonly:
            text_widget.configure(state=tk.DISABLED)

        return text_widget

    # ---------------------------------------------------------
    # INPUT TAB
    # ---------------------------------------------------------

    def create_input_tab(self):
        self.input_frame = tk.Frame(
            self.notebook,
            bg="#1e1e1e"
        )

        self.notebook.add(
            self.input_frame,
            text="Input"
        )

        self.input_label = tk.Label(
            self.input_frame,
            text="Standard Input (stdin)",
            bg="#1e1e1e",
            fg="#858585",
            font=("Segoe UI", 9)
        )
        self.input_label.pack(
            anchor=tk.W,
            padx=12,
            pady=(10, 4)
        )

        self.input_text = self.create_text_area(
            self.input_frame
        )

    # ---------------------------------------------------------
    # OUTPUT TAB
    # ---------------------------------------------------------

    def create_output_tab(self):
        self.output_frame = tk.Frame(
            self.notebook,
            bg="#1e1e1e"
        )

        self.notebook.add(
            self.output_frame,
            text="Output"
        )

        self.output_label = tk.Label(
            self.output_frame,
            text="Program Output (stdout)",
            bg="#1e1e1e",
            fg="#858585",
            font=("Segoe UI", 9)
        )
        self.output_label.pack(
            anchor=tk.W,
            padx=12,
            pady=(10, 4)
        )

        self.output_text = self.create_text_area(
            self.output_frame,
            readonly=True
        )

        self.output_text.tag_configure(
            "normal",
            foreground="#d4d4d4"
        )

    # ---------------------------------------------------------
    # COMPILER MESSAGES TAB
    # ---------------------------------------------------------

    def create_messages_tab(self):
        self.messages_frame = tk.Frame(
            self.notebook,
            bg="#1e1e1e"
        )

        self.notebook.add(
            self.messages_frame,
            text="Compiler Messages"
        )

        self.messages_label = tk.Label(
            self.messages_frame,
            text="Compilation and Execution Messages",
            bg="#1e1e1e",
            fg="#858585",
            font=("Segoe UI", 9)
        )
        self.messages_label.pack(
            anchor=tk.W,
            padx=12,
            pady=(10, 4)
        )

        self.messages_text = self.create_text_area(
            self.messages_frame,
            readonly=True
        )

        self.messages_text.tag_configure(
            "success",
            foreground="#4ec9b0"
        )

        self.messages_text.tag_configure(
            "error",
            foreground="#f48771"
        )

        self.messages_text.tag_configure(
            "warning",
            foreground="#dcdcaa"
        )

        self.messages_text.tag_configure(
            "info",
            foreground="#569cd6"
        )

    # ---------------------------------------------------------
    # INTERNAL TEXT HELPERS
    # ---------------------------------------------------------

    def append_text(self, widget, message, tag=None):
        widget.configure(state=tk.NORMAL)

        if tag:
            widget.insert(tk.END, message, tag)
        else:
            widget.insert(tk.END, message)

        widget.see(tk.END)
        widget.configure(state=tk.DISABLED)

    def replace_text(self, widget, message, tag=None):
        widget.configure(state=tk.NORMAL)
        widget.delete("1.0", tk.END)

        if tag:
            widget.insert("1.0", message, tag)
        else:
            widget.insert("1.0", message)

        widget.see(tk.END)
        widget.configure(state=tk.DISABLED)

    # ---------------------------------------------------------
    # INPUT METHODS
    # ---------------------------------------------------------

    def get_input(self):
        return self.input_text.get(
            "1.0",
            "end-1c"
        )

    def set_input(self, value):
        self.input_text.delete(
            "1.0",
            tk.END
        )

        self.input_text.insert(
            "1.0",
            value
        )

    def clear_input(self):
        self.input_text.delete(
            "1.0",
            tk.END
        )

    # ---------------------------------------------------------
    # OUTPUT METHODS
    # ---------------------------------------------------------

    def show_output(self, output):
        self.replace_text(
            self.output_text,
            str(output)
        )

        self.notebook.select(
            self.output_frame
        )

    def append_output(self, output):
        self.append_text(
            self.output_text,
            str(output)
        )

    def clear_output(self):
        self.replace_text(
            self.output_text,
            ""
        )

    # ---------------------------------------------------------
    # COMPILER MESSAGE METHODS
    # ---------------------------------------------------------

    def show_message(self, message, message_type="info"):
        tag = message_type.lower()

        if tag not in (
            "success",
            "error",
            "warning",
            "info"
        ):
            tag = "info"

        self.append_text(
            self.messages_text,
            str(message) + "\n",
            tag
        )

        self.notebook.select(
            self.messages_frame
        )

    def show_success(self, message):
        self.show_message(
            message,
            "success"
        )

    def show_error(self, message):
        self.show_message(
            message,
            "error"
        )

    def show_warning(self, message):
        self.show_message(
            message,
            "warning"
        )

    def show_info(self, message):
        self.show_message(
            message,
            "info"
        )

    def clear_messages(self):
        self.replace_text(
            self.messages_text,
            ""
        )

    # ---------------------------------------------------------
    # GENERAL METHODS
    # ---------------------------------------------------------

    def clear_all(self):
        self.clear_input()
        self.clear_output()
        self.clear_messages()

    def clear_results(self):
        self.clear_output()
        self.clear_messages()

    def get_all_data(self):
        return {
            "input": self.get_input(),
            "output": self.output_text.get(
                "1.0",
                "end-1c"
            ),
            "messages": self.messages_text.get(
                "1.0",
                "end-1c"
            )
        }
