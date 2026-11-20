
import tkinter as tk

from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from gui.editor import CodeEditor


class PyCMinorIDE:

    def __init__(self, root):

        self.root = root
        self.root.title("PyCMinor IDE")
        self.root.geometry("1400x850")
        self.root.minsize(1000, 650)

        self.current_file = None
        self.is_modified = False

        # Theme colors
        self.BG = "#0f172a"
        self.PANEL = "#111827"
        self.EDITOR_BG = "#0b1220"
        self.INPUT_BG = "#111827"
        self.OUTPUT_BG = "#111827"
        self.BORDER = "#263449"

        self.TEXT = "#e5e7eb"
        self.MUTED = "#94a3b8"

        self.root.configure(
            bg=self.BG
        )

        self.setup_styles()
        self.create_toolbar()
        self.create_workspace()
        self.create_statusbar()

        self.insert_starter_code()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

        # Keyboard shortcuts
        self.root.bind(
            "<Control-n>",
            self.new_file
        )

        self.root.bind(
            "<Control-o>",
            self.open_file
        )

        self.root.bind(
            "<Control-s>",
            self.save_file
        )

        self.root.bind(
            "<F5>",
            self.run_code
        )

        self.root.bind(
            "<Control-Return>",
            self.compile_code
        )

    # --------------------------------------------------
    # STYLES
    # --------------------------------------------------

    def setup_styles(self):

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "IDE.TButton",
            background="#1e293b",
            foreground=self.TEXT,
            borderwidth=0,
            padding=(12, 7),
            font=("Segoe UI", 9)
        )

        style.map(
            "IDE.TButton",
            background=[
                ("active", "#334155"),
                ("pressed", "#475569")
            ]
        )

        style.configure(
            "Compile.TButton",
            background="#2563eb",
            foreground="white",
            padding=(14, 7),
            borderwidth=0,
            font=("Segoe UI", 9, "bold")
        )

        style.map(
            "Compile.TButton",
            background=[
                ("active", "#1d4ed8")
            ]
        )

        style.configure(
            "Run.TButton",
            background="#15803d",
            foreground="white",
            padding=(14, 7),
            borderwidth=0,
            font=("Segoe UI", 9, "bold")
        )

        style.map(
            "Run.TButton",
            background=[
                ("active", "#166534")
            ]
        )

    # --------------------------------------------------
    # TOOLBAR
    # --------------------------------------------------

    def create_toolbar(self):

        toolbar = tk.Frame(
            self.root,
            bg=self.BG,
            height=55
        )

        toolbar.pack(
            side=tk.TOP,
            fill=tk.X,
            padx=12,
            pady=(10, 5)
        )

        toolbar.pack_propagate(False)

        tk.Label(
            toolbar,
            text="PyCMinor IDE",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 15, "bold")
        ).pack(
            side=tk.LEFT,
            padx=(5, 25)
        )

        ttk.Button(
            toolbar,
            text="New",
            style="IDE.TButton",
            command=self.new_file
        ).pack(
            side=tk.LEFT,
            padx=3
        )

        ttk.Button(
            toolbar,
            text="Open",
            style="IDE.TButton",
            command=self.open_file
        ).pack(
            side=tk.LEFT,
            padx=3
        )

        ttk.Button(
            toolbar,
            text="Save",
            style="IDE.TButton",
            command=self.save_file
        ).pack(
            side=tk.LEFT,
            padx=3
        )

        ttk.Button(
            toolbar,
            text="Compile",
            style="Compile.TButton",
            command=self.compile_code
        ).pack(
            side=tk.LEFT,
            padx=(15, 3)
        )

        ttk.Button(
            toolbar,
            text="Run",
            style="Run.TButton",
            command=self.run_code
        ).pack(
            side=tk.LEFT,
            padx=3
        )

        self.file_label = tk.Label(
            toolbar,
            text="Untitled.cminor",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        )

        self.file_label.pack(
            side=tk.RIGHT,
            padx=10
        )

    # --------------------------------------------------
    # MAIN WORKSPACE
    # --------------------------------------------------

    def create_workspace(self):

        self.main_pane = tk.PanedWindow(
            self.root,
            orient=tk.VERTICAL,
            bg=self.BORDER,
            sashwidth=5,
            sashrelief=tk.FLAT,
            bd=0
        )

        self.main_pane.pack(
            fill=tk.BOTH,
            expand=True,
            padx=12,
            pady=8
        )

        self.create_editor_panel()
        self.create_io_panels()

    # --------------------------------------------------
    # EDITOR PANEL
    # --------------------------------------------------

    def create_editor_panel(self):

        self.editor_container = tk.Frame(
            self.main_pane,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        self.main_pane.add(
            self.editor_container,
            minsize=300,
            stretch="always"
        )

        header = tk.Frame(
            self.editor_container,
            bg=self.PANEL,
            height=38
        )

        header.pack(
            side=tk.TOP,
            fill=tk.X
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="  CODE EDITOR",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(
            side=tk.LEFT,
            padx=8
        )

        tk.Label(
            header,
            text="C Minor",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        ).pack(
            side=tk.RIGHT,
            padx=12
        )

        # Reusable editor from editor.py
        self.code_editor = CodeEditor(
            self.editor_container,
            on_change=self.on_editor_change,
            on_cursor_change=self.on_cursor_change
        )

        self.code_editor.pack(
            fill=tk.BOTH,
            expand=True
        )

    # --------------------------------------------------
    # EDITOR CALLBACKS
    # --------------------------------------------------

    def on_editor_change(self):

        self.is_modified = True
        self.update_title()

        self.status_label.configure(
            text="Modified"
        )

    def on_cursor_change(self, line, column):

        self.cursor_label.configure(
            text=f"Line {line}, Column {column}"
        )

    def get_source(self):

        return self.code_editor.get_code()

    # --------------------------------------------------
    # INPUT AND OUTPUT PANELS
    # --------------------------------------------------

    def create_io_panels(self):

        self.io_container = tk.Frame(
            self.main_pane,
            bg=self.BG
        )

        self.main_pane.add(
            self.io_container,
            minsize=180,
            height=240,
            stretch="never"
        )

        self.io_pane = tk.PanedWindow(
            self.io_container,
            orient=tk.HORIZONTAL,
            bg=self.BORDER,
            sashwidth=5,
            sashrelief=tk.FLAT,
            bd=0
        )

        self.io_pane.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.create_input_panel()
        self.create_output_panel()

    # --------------------------------------------------
    # CUSTOM INPUT
    # --------------------------------------------------

    def create_input_panel(self):

        self.input_container = tk.Frame(
            self.io_pane,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        self.io_pane.add(
            self.input_container,
            minsize=250,
            stretch="always"
        )

        header = tk.Frame(
            self.input_container,
            bg=self.PANEL,
            height=38
        )

        header.pack(
            fill=tk.X
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="  CUSTOM INPUT",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(
            side=tk.LEFT,
            padx=8
        )

        ttk.Button(
            header,
            text="Clear",
            style="IDE.TButton",
            command=self.clear_input
        ).pack(
            side=tk.RIGHT,
            padx=8,
            pady=3
        )

        input_area = tk.Frame(
            self.input_container,
            bg=self.INPUT_BG
        )

        input_area.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.input_text = tk.Text(
            input_area,
            wrap=tk.NONE,
            bg=self.INPUT_BG,
            fg=self.TEXT,
            insertbackground="white",
            selectbackground="#334155",
            font=("Consolas", 10),
            padx=12,
            pady=10,
            relief=tk.FLAT,
            borderwidth=0
        )

        self.input_text.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        input_scrollbar = ttk.Scrollbar(
            input_area,
            orient=tk.VERTICAL,
            command=self.input_text.yview
        )

        input_scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        self.input_text.configure(
            yscrollcommand=input_scrollbar.set
        )

    # --------------------------------------------------
    # OUTPUT PANEL
    # --------------------------------------------------

    def create_output_panel(self):

        self.output_container = tk.Frame(
            self.io_pane,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        self.io_pane.add(
            self.output_container,
            minsize=250,
            stretch="always"
        )

        header = tk.Frame(
            self.output_container,
            bg=self.PANEL,
            height=38
        )

        header.pack(
            fill=tk.X
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="  OUTPUT",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(
            side=tk.LEFT,
            padx=8
        )

        ttk.Button(
            header,
            text="Clear",
            style="IDE.TButton",
            command=self.clear_output
        ).pack(
            side=tk.RIGHT,
            padx=8,
            pady=3
        )

        output_area = tk.Frame(
            self.output_container,
            bg=self.OUTPUT_BG
        )

        output_area.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.output_text = tk.Text(
            output_area,
            wrap=tk.WORD,
            bg=self.OUTPUT_BG,
            fg="#86efac",
            insertbackground="white",
            selectbackground="#334155",
            font=("Consolas", 10),
            padx=12,
            pady=10,
            relief=tk.FLAT,
            borderwidth=0,
            state=tk.DISABLED
        )

        self.output_text.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        output_scrollbar = ttk.Scrollbar(
            output_area,
            orient=tk.VERTICAL,
            command=self.output_text.yview
        )

        output_scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        self.output_text.configure(
            yscrollcommand=output_scrollbar.set
        )

    # --------------------------------------------------
    # STATUS BAR
    # --------------------------------------------------

    def create_statusbar(self):

        statusbar = tk.Frame(
            self.root,
            bg="#111827",
            height=30
        )

        statusbar.pack(
            side=tk.BOTTOM,
            fill=tk.X
        )

        statusbar.pack_propagate(False)

        self.status_label = tk.Label(
            statusbar,
            text="Ready",
            bg="#111827",
            fg=self.MUTED,
            font=("Segoe UI", 9)
        )

        self.status_label.pack(
            side=tk.LEFT,
            padx=12
        )

        self.cursor_label = tk.Label(
            statusbar,
            text="Line 1, Column 1",
            bg="#111827",
            fg=self.MUTED,
            font=("Segoe UI", 9)
        )

        self.cursor_label.pack(
            side=tk.RIGHT,
            padx=12
        )

    # --------------------------------------------------
    # STARTER CODE
    # --------------------------------------------------

    def insert_starter_code(self):

        starter_code = (
            "int main() {\n"
            "    int number = 10;\n"
            "    int result = number + 20;\n"
            "\n"
            "    return result;\n"
            "}\n"
        )

        self.code_editor.set_code(
            starter_code
        )

        self.is_modified = False
        self.update_title()

    # --------------------------------------------------
    # TITLE AND FILE STATUS
    # --------------------------------------------------

    def update_title(self):

        filename = (
            self.current_file.name
            if self.current_file
            else "Untitled.cminor"
        )

        marker = "*" if self.is_modified else ""

        self.file_label.configure(
            text=filename + marker
        )

        self.root.title(
            f"{filename}{marker} - PyCMinor IDE"
        )

    # --------------------------------------------------
    # OUTPUT HELPERS
    # --------------------------------------------------

    def write_output(self, message):

        self.output_text.configure(
            state=tk.NORMAL
        )

        self.output_text.insert(
            tk.END,
            str(message) + "\n"
        )

        self.output_text.see(
            tk.END
        )

        self.output_text.configure(
            state=tk.DISABLED
        )

    def clear_output(self):

        self.output_text.configure(
            state=tk.NORMAL
        )

        self.output_text.delete(
            "1.0",
            tk.END
        )

        self.output_text.configure(
            state=tk.DISABLED
        )

    def clear_input(self):

        self.input_text.delete(
            "1.0",
            tk.END
        )

    def get_input(self):

        return self.input_text.get(
            "1.0",
            "end-1c"
        )

    # --------------------------------------------------
    # FILE MANAGEMENT
    # --------------------------------------------------

    def new_file(self, event=None):

        if not self.confirm_discard():
            return "break"

        self.code_editor.clear()

        self.current_file = None
        self.is_modified = False

        self.update_title()
        self.clear_output()
        self.clear_input()

        self.status_label.configure(
            text="New file created"
        )

        self.code_editor.focus_editor()

        return "break"

    def open_file(self, event=None):

        if not self.confirm_discard():
            return "break"

        filename = filedialog.askopenfilename(
            title="Open C Minor File",
            filetypes=[
                ("C Minor Files", "*.cminor"),
                ("All Files", "*.*")
            ]
        )

        if not filename:
            return "break"

        try:

            path = Path(filename)

            content = path.read_text(
                encoding="utf-8"
            )

            self.code_editor.set_code(
                content
            )

            self.current_file = path
            self.is_modified = False

            self.update_title()

            self.status_label.configure(
                text=f"Opened {path.name}"
            )

            self.code_editor.focus_editor()

        except (OSError, UnicodeError) as error:

            messagebox.showerror(
                "Open Error",
                str(error)
            )

        return "break"

    def save_file(self, event=None):

        if self.current_file is None:

            filename = filedialog.asksaveasfilename(
                title="Save C Minor File",
                defaultextension=".cminor",
                filetypes=[
                    ("C Minor Files", "*.cminor"),
                    ("All Files", "*.*")
                ]
            )

            if not filename:
                return False

            self.current_file = Path(filename)

        try:

            self.current_file.write_text(
                self.get_source(),
                encoding="utf-8"
            )

            self.is_modified = False
            self.code_editor.reset_modified()

            self.update_title()

            self.status_label.configure(
                text=f"Saved {self.current_file.name}"
            )

            return True

        except OSError as error:

            messagebox.showerror(
                "Save Error",
                str(error)
            )

            return False

    def confirm_discard(self):

        if not self.is_modified:
            return True

        answer = messagebox.askyesnocancel(
            "Unsaved Changes",
            "Do you want to save your changes?"
        )

        if answer is None:
            return False

        if answer is True:
            return self.save_file()

        return True

    def on_close(self):

        if self.confirm_discard():
            self.root.destroy()

    # --------------------------------------------------
    # COMPILER INTEGRATION
    # --------------------------------------------------

    def compile_code(self, event=None):

        source = self.get_source()

        if not source.strip():

            messagebox.showwarning(
                "Empty Source",
                "Please write some C Minor code first."
            )

            return "break"

        if self.is_modified and self.current_file is not None:

            if not self.save_file():
                return "break"

        self.clear_output()

        self.status_label.configure(
            text="Compilation requested"
        )

        self.write_output("PyCMinor Compiler")
        self.write_output("------------------------------")

        self.write_output(
            "Compiler pipeline has not been connected yet."
        )

        self.write_output(
            "Next step: connect compiler.py."
        )

        return "break"

    def run_code(self, event=None):

        self.clear_output()

        self.status_label.configure(
            text="Execution requested"
        )

        self.write_output("PyCMinor Execution")
        self.write_output("------------------------------")

        self.write_output(
            "Execution is not connected yet."
        )

        self.write_output(
            "Next step: connect the compiler and executable pipeline."
        )

        return "break"


# ------------------------------------------------------
# APPLICATION ENTRY POINT
# ------------------------------------------------------

def main():

    root = tk.Tk()

    app = PyCMinorIDE(root)

    root.mainloop()


if __name__ == "__main__":
    main()
