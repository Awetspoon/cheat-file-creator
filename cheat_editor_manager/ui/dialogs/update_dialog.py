from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser

from ...services.update_service import ReleaseInfo
from ...ui.style import CONTROL_GAP, FONT_PANEL_TITLE, PANEL_GAP, PANEL_INNER_PAD_X
from .dialog_utils import (
    bind_dialog_shortcuts,
    build_dialog_footer,
    build_dialog_header,
    configure_dialog_window,
)


UPDATE_DIALOG_GEOMETRY = "540x300"
UPDATE_DIALOG_WRAP = 490


def show_update_available(
    app,
    installed_version: str,
    release: ReleaseInfo,
) -> tk.Toplevel:
    existing = getattr(app, "_update_dialog", None)
    if existing is not None:
        try:
            if existing.winfo_exists():
                existing.deiconify()
                existing.lift()
                existing.focus_force()
                return existing
        except tk.TclError:
            pass

    window = tk.Toplevel(app.root)
    configure_dialog_window(
        app,
        window,
        "Update available",
        UPDATE_DIALOG_GEOMETRY,
        modal=False,
        resizable=False,
    )
    app._update_dialog = window

    def close_dialog() -> None:
        app._update_dialog = None
        window.destroy()

    def open_release() -> None:
        try:
            opened = webbrowser.open_new_tab(release.url)
        except Exception as exc:
            messagebox.showerror(
                "Open Release",
                f"Windows could not open the GitHub release page.\n\n{exc}",
                parent=window,
            )
            return
        if not opened:
            messagebox.showerror(
                "Open Release",
                f"Windows could not open the browser.\n\nRelease page:\n{release.url}",
                parent=window,
            )
            return
        close_dialog()

    window.protocol("WM_DELETE_WINDOW", close_dialog)
    build_dialog_header(
        app,
        window,
        "Update Available",
        f"Version {release.display_version} is ready to download.",
    )

    footer = build_dialog_footer(
        app,
        window,
        pady=(0, PANEL_INNER_PAD_X),
        side="bottom",
    )
    ttk.Button(footer, text="Later", command=close_dialog).pack(
        side="right",
        padx=(CONTROL_GAP, PANEL_INNER_PAD_X),
        pady=PANEL_GAP,
    )
    ttk.Button(
        footer,
        text="View Release",
        command=open_release,
        style="Primary.TButton",
    ).pack(side="right", pady=PANEL_GAP)

    body = ttk.Frame(window)
    body.pack(
        fill="both",
        expand=True,
        padx=PANEL_INNER_PAD_X * 2,
        pady=(0, PANEL_GAP),
    )
    body.columnconfigure(1, weight=1)

    ttk.Label(
        body,
        text=release.name,
        font=FONT_PANEL_TITLE,
        wraplength=UPDATE_DIALOG_WRAP,
        justify="left",
    ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, PANEL_GAP))

    ttk.Label(body, text="Installed version").grid(row=1, column=0, sticky="w")
    ttk.Label(body, text=installed_version).grid(
        row=1,
        column=1,
        sticky="w",
        padx=(CONTROL_GAP * 2, 0),
    )
    ttk.Label(body, text="Available version").grid(
        row=2,
        column=0,
        sticky="w",
        pady=(4, 0),
    )
    ttk.Label(body, text=release.display_version).grid(
        row=2,
        column=1,
        sticky="w",
        padx=(CONTROL_GAP * 2, 0),
        pady=(4, 0),
    )

    ttk.Label(
        body,
        text=(
            "Open the GitHub release page to read the changes and download the "
            "new version. The app will never install an update automatically."
        ),
        wraplength=UPDATE_DIALOG_WRAP,
        justify="left",
    ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(PANEL_GAP, 0))

    bind_dialog_shortcuts(window, confirm=open_release, cancel=close_dialog)
    window.focus_set()
    return window
