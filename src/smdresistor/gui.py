import json
import tkinter as tk
from pathlib import Path
from tkinter import ttk
from .decoder import decode, format_ohms

APP_TITLE = "SMD Resistor Decoder"
CONFIG_PATH = Path.home() / ".smd_resistor_decoder.json"


def run():
    root = tk.Tk()
    root.title(APP_TITLE)

    # Load config (geometry, theme, live decode)
    cfg = {"geometry": "420x240", "theme": "light", "live": True}
    if CONFIG_PATH.exists():
        try:
            cfg.update(json.loads(CONFIG_PATH.read_text()))
        except Exception:
            pass

    root.geometry(cfg.get("geometry", "420x240"))

    if tk.TkVersion >= 8.6:
        try:
            root.call("tk", "scaling", 1.2)
        except Exception:
            pass

    style = ttk.Style(root)
    available = style.theme_names()

    def apply_theme(theme: str):
        # Use a standard theme and adjust a few colors for dark
        target = "clam" if theme == "dark" and "clam" in available else style.theme_use()
        try:
            style.theme_use(target)
        except Exception:
            pass
        if theme == "dark":
            bg = "#222"
            fg = "#ddd"
            accent = "#2b7a0b"
            error = "#ff5c5c"
        else:
            bg = "#f7f7f7"
            fg = "#111"
            accent = "#2b7a0b"
            error = "#b00020"
        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=fg)
        style.configure("TEntry", fieldbackground="#fff" if theme == "light" else "#333", foreground=fg)
        style.configure("TButton")
        return accent, error

    accent_color, error_color = apply_theme(cfg.get("theme", "light"))

    mainframe = ttk.Frame(root, padding=16)
    mainframe.grid(row=0, column=0, sticky="nsew")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Title
    title = ttk.Label(mainframe, text=APP_TITLE, font=("Segoe UI", 14, "bold"))
    title.grid(row=0, column=0, columnspan=4, sticky="w")

    # Input
    ttk.Label(mainframe, text="Enter code:").grid(row=1, column=0, sticky="w", pady=(12, 0))
    code_var = tk.StringVar()
    code_entry = ttk.Entry(mainframe, textvariable=code_var, width=20)
    code_entry.grid(row=1, column=1, sticky="w", padx=(8, 0), pady=(12, 0))
    code_entry.focus_set()

    live_var = tk.BooleanVar(value=bool(cfg.get("live", True)))
    live_chk = ttk.Checkbutton(mainframe, text="Live decode", variable=live_var)
    live_chk.grid(row=1, column=2, sticky="w", padx=(8, 0), pady=(12, 0))

    # Theme toggle
    theme_var = tk.StringVar(value=cfg.get("theme", "light"))
    theme_btn = ttk.Button(mainframe, text="Toggle Theme", command=lambda: on_toggle_theme())
    theme_btn.grid(row=1, column=3, sticky="e", padx=(8, 0), pady=(12, 0))

    # Decode button
    def on_decode(*_):
        code = code_var.get().strip()
        if not code:
            set_status("Please enter a code.", error=True)
            result_var.set("")
            scheme_var.set("")
            return
        try:
            res = decode(code)
            result_var.set(format_ohms(res.ohms))
            scheme_var.set(res.scheme)
            set_status("Decoded successfully.")
        except Exception as e:
            result_var.set("—")
            scheme_var.set("—")
            set_status(str(e), error=True)

    decode_btn = ttk.Button(mainframe, text="Decode", command=on_decode)
    decode_btn.grid(row=1, column=4, sticky="w", padx=(8, 0), pady=(12, 0))

    # Output
    ttk.Label(mainframe, text="Value:").grid(row=2, column=0, sticky="w", pady=(16, 0))
    result_var = tk.StringVar(value="—")
    result_lbl = ttk.Label(mainframe, textvariable=result_var, font=("Segoe UI", 16, "bold"))
    result_lbl.grid(row=2, column=1, sticky="w", padx=(8, 0), pady=(12, 0))

    copy_btn = ttk.Button(mainframe, text="Copy", command=lambda: copy_to_clipboard(root, result_var.get()))
    copy_btn.grid(row=2, column=2, sticky="w", padx=(8, 0))

    ttk.Label(mainframe, text="Scheme:").grid(row=3, column=0, sticky="w")
    scheme_var = tk.StringVar(value="—")
    scheme_lbl = ttk.Label(mainframe, textvariable=scheme_var)
    scheme_lbl.grid(row=3, column=1, sticky="w", padx=(8, 0))

    # Examples
    examples = "Examples: 103  4R7  01C  1002  0R0"
    ex_lbl = ttk.Label(mainframe, text=examples)
    ex_lbl.grid(row=4, column=0, columnspan=5, sticky="w", pady=(12, 0))

    # Status bar
    status_var = tk.StringVar(value="Ready")
    status = ttk.Label(root, textvariable=status_var, relief=tk.SUNKEN, anchor="w", padding=(8, 4))
    status.grid(row=1, column=0, sticky="ew")

    def set_status(msg: str, error: bool = False):
        status_var.set(msg)
        status.configure(foreground=(error_color if error else accent_color))

    # Handlers
    def on_key_release(_):
        if live_var.get():
            on_decode()

    def on_toggle_theme():
        theme_var.set("dark" if theme_var.get() == "light" else "light")
        nonlocal_vars = {}
        nonlocal_vars["accent"], nonlocal_vars["err"] = apply_theme(theme_var.get())
        nonlocal accent_color, error_color
        accent_color, error_color = nonlocal_vars["accent"], nonlocal_vars["err"]
        set_status(f"Theme: {theme_var.get()}")

    def on_close():
        # Save geometry and preferences
        data = {
            "geometry": root.geometry(),
            "theme": theme_var.get(),
            "live": bool(live_var.get()),
        }
        try:
            CONFIG_PATH.write_text(json.dumps(data))
        except Exception:
            pass
        root.destroy()

    def copy_to_clipboard(win: tk.Tk, text: str):
        try:
            win.clipboard_clear()
            win.clipboard_append(text)
            set_status("Copied to clipboard")
        except Exception as e:
            set_status(f"Copy failed: {e}", error=True)

    # Bindings
    root.bind("<Return>", on_decode)
    code_entry.bind("<KeyRelease>", on_key_release)
    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()


if __name__ == "__main__":
    run()

