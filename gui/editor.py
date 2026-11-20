
import re
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional


class CodeEditor(tk.Frame):
    def __init__(
        self,
        parent,
        on_change: Optional[Callable] = None,
        on_cursor_change: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__(parent, **kwargs)

        self.on_change = on_change
        self.on_cursor_change = on_cursor_change

        self.configure(bg="#1e1e1e")

        self.create_editor()
        self.configure_syntax_tags()

        self.text.bind("<<Modified>>", self.on_text_modified)
        self.text.bind("<KeyRelease>", self.on_key_release)
        self.text.bind("<Return>", self.auto_indent)
        self.text.bind("<Tab>", self.insert_tab)
        self.text.bind("<Control-z>", self.undo)
        self.text.bind("<Control-y>", self.redo)

        self.update_line_numbers()
        self.highlight_syntax()

    # ---------------------------------------------------------
    # EDITOR UI
    # ---------------------------------------------------------

    def create_editor(self):
        self.container = tk.Frame(self, bg="#1e1e1e")
        self.container.pack(fill=tk.BOTH, expand=True)

        self.line_numbers = tk.Text(
            self.container,
            width=5,
            padx=8,
            pady=10,
            takefocus=0,
            border=0,
            background="#252526",
            foreground="#858585",
            font=("Consolas", 11),
            state=tk.DISABLED,
            wrap=tk.NONE,
            cursor="arrow"
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.text = tk.Text(
            self.container,
            wrap=tk.NONE,
            undo=True,
            maxundo=-1,
            autoseparators=True,
            font=("Consolas", 11),
            background="#1e1e1e",
            foreground="#d4d4d4",
            insertbackground="#ffffff",
            selectbackground="#264f78",
            selectforeground="#ffffff",
            padx=10,
            pady=10,
            border=0,
            spacing1=2,
            spacing3=2,
            tabs=("4c",)
        )
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar_y = ttk.Scrollbar(
            self.container,
            orient=tk.VERTICAL,
            command=self.scroll_vertical
        )
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollbar_x = ttk.Scrollbar(
            self,
            orient=tk.HORIZONTAL,
            command=self.text.xview
        )
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.text.configure(
            yscrollcommand=self.on_vertical_scroll,
            xscrollcommand=self.scrollbar_x.set
        )

        self.line_numbers.tag_configure(
            "line",
            foreground="#858585",
            justify=tk.RIGHT
        )

    # ---------------------------------------------------------
    # SYNTAX COLORS
    # ---------------------------------------------------------

    def configure_syntax_tags(self):
        self.text.tag_configure(
            "keyword",
            foreground="#c586c0"
        )

        self.text.tag_configure(
            "type",
            foreground="#4ec9b0"
        )

        self.text.tag_configure(
            "number",
            foreground="#b5cea8"
        )

        self.text.tag_configure(
            "boolean",
            foreground="#569cd6"
        )

        self.text.tag_configure(
            "string",
            foreground="#ce9178"
        )

        self.text.tag_configure(
            "comment",
            foreground="#6a9955"
        )

        self.text.tag_configure(
            "function",
            foreground="#dcdcaa"
        )

        self.text.tag_configure(
            "operator",
            foreground="#d4d4d4"
        )

    # ---------------------------------------------------------
    # SYNTAX HIGHLIGHTING
    # ---------------------------------------------------------

    def highlight_syntax(self):
        code = self.text.get("1.0", "end-1c")

        # Remove previous syntax tags.
        for tag in (
            "keyword",
            "type",
            "number",
            "boolean",
            "string",
            "comment",
            "function",
            "operator"
        ):
            self.text.tag_remove(tag, "1.0", tk.END)

        patterns = {
            "keyword": (
                r"\b(if|else|while|return)\b"
            ),

            "type": (
                r"\b(int|void|bool|float|double|string|char)\b"
            ),

            "number": (
                r"\b\d+(?:\.\d+)?\b"
            ),

            "boolean": (
                r"\b(true|false)\b"
            ),

            "string": (
                r'"(?:\\.|[^"\\])*"|'
                r"'(?:\\.|[^'\\])*'"
            ),

            "comment": (
                r"//[^\n]*|/\*[\s\S]*?\*/"
            ),

            "function": (
                r"\b[A-Za-z_]\w*(?=\s*\()"
            ),

            "operator": (
                r"==|!=|<=|>=|&&|\|\||[+\-*/%=<>!]"
            )
        }

        # Apply syntax highlighting.
        for tag, pattern in patterns.items():
            for match in re.finditer(pattern, code):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"

                self.text.tag_add(tag, start, end)

        # Comments and strings should appear above other tags.
        self.text.tag_raise("comment")
        self.text.tag_raise("string")

    # ---------------------------------------------------------
    # LINE NUMBERS
    # ---------------------------------------------------------

    def update_line_numbers(self):
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete("1.0", tk.END)

        line_count = int(self.text.index("end-1c").split(".")[0])

        line_text = "\n".join(
            str(number)
            for number in range(1, line_count + 1)
        )

        self.line_numbers.insert("1.0", line_text)
        self.line_numbers.config(state=tk.DISABLED)

        self.sync_line_numbers()

    def sync_line_numbers(self):
        self.line_numbers.yview_moveto(
            self.text.yview()[0]
        )

    def on_vertical_scroll(self, first, last):
        self.scrollbar_y.set(first, last)
        self.line_numbers.yview_moveto(first)

    def scroll_vertical(self, *args):
        self.text.yview(*args)
        self.line_numbers.yview(*args)

    # ---------------------------------------------------------
    # TEXT CHANGE EVENTS
    # ---------------------------------------------------------

    def on_text_modified(self, event=None):
        if self.text.edit_modified():
            self.update_line_numbers()
            self.highlight_syntax()

            if self.on_change:
                self.on_change()

            self.text.edit_modified(False)

    def on_key_release(self, event=None):
        self.update_cursor_position()

    def update_cursor_position(self):
        cursor_position = self.text.index(tk.INSERT)

        line, column = cursor_position.split(".")

        if self.on_cursor_change:
            self.on_cursor_change(
                int(line),
                int(column) + 1
            )

    # ---------------------------------------------------------
    # AUTO INDENTATION
    # ---------------------------------------------------------

    def auto_indent(self, event=None):
        current_line = self.text.get(
            "insert linestart",
            "insert"
        )

        match = re.match(r"[ \t]*", current_line)
        indentation = match.group() if match else ""

        stripped_line = current_line.strip()

        if stripped_line.endswith("{"):
            indentation += "    "

        self.text.insert(tk.INSERT, "\n" + indentation)

        return "break"

    # ---------------------------------------------------------
    # TAB INDENTATION
    # ---------------------------------------------------------

    def insert_tab(self, event=None):
        try:
            selected_text = self.text.get(
                tk.SEL_FIRST,
                tk.SEL_LAST
            )

            if selected_text:
                self.text.insert(tk.INSERT, "    ")
            else:
                self.text.insert(tk.INSERT, "    ")

        except tk.TclError:
            self.text.insert(tk.INSERT, "    ")

        return "break"

    # ---------------------------------------------------------
    # PUBLIC EDITOR METHODS
    # ---------------------------------------------------------

    def get_code(self):
        return self.text.get("1.0", "end-1c")

    def set_code(self, code):
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", code)

        self.text.edit_modified(False)

        self.update_line_numbers()
        self.highlight_syntax()
        self.update_cursor_position()

    def clear(self):
        self.set_code("")

    def insert_code(self, code):
        self.text.insert(tk.INSERT, code)
        self.text.focus_set()

    def is_modified(self):
        return self.text.edit_modified()

    def reset_modified(self):
        self.text.edit_modified(False)

    def focus_editor(self):
        self.text.focus_set()

    def undo(self, event=None):
        try:
            self.text.edit_undo()
        except tk.TclError:
            pass

        return "break"

    def redo(self, event=None):
        try:
            self.text.edit_redo()
        except tk.TclError:
            pass

        return "break"
