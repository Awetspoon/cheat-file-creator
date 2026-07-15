from __future__ import annotations

import tkinter as tk

from cheat_editor_manager.app import App, create_app_root
from cheat_editor_manager.bootstrap import configure_tcl_environment


OFFSCREEN_POSITION = "+32000+32000"


def offscreen_geometry(width: int, height: int) -> str:
    return f"{width}x{height}{OFFSCREEN_POSITION}"


def reset_tk_root_state() -> None:
    root = getattr(tk, "_default_root", None)
    if root is not None:
        try:
            if root.winfo_exists():
                root.destroy()
        except Exception:
            pass
    try:
        tk._default_root = None
    except Exception:
        pass


def create_offscreen_root(width: int = 1280, height: int = 820) -> tk.Tk:
    reset_tk_root_state()
    configure_tcl_environment()
    root = create_app_root()
    root.geometry(offscreen_geometry(width, height))
    return root


def create_test_app() -> App:
    app = App(root=create_offscreen_root(), enable_update_check=False)
    app.root.update_idletasks()
    app.root.update()
    return app


def destroy_root(root: tk.Misc | None) -> None:
    if root is None:
        reset_tk_root_state()
        return
    try:
        root.destroy()
    except Exception:
        pass
    reset_tk_root_state()
