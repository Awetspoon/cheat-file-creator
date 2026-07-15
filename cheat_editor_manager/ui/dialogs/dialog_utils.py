from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ...services import theme_service
from ...ui.style import (
    CONTROL_GAP,
    DIALOG_CONTENT_PAD_X,
    DIALOG_SECTION_WRAP,
    FONT_PANEL_TITLE,
    FONT_SECTION,
    PANEL_GAP,
    PANEL_INNER_PAD_X,
    PANEL_INNER_PAD_Y,
)
from ...ui.widgets import AutoScrollbar, configure_listbox_theme


def dialog_palette(app) -> dict[str, str]:
    colors = app.effective_colors()
    return {
        "bg": colors["bg"],
        "panel": colors["panel"],
        "border": colors["border"],
        "text": theme_service.ensure_text_contrast(
            colors["panel"], preferred=colors["text"], minimum=4.5
        ),
        "muted": theme_service.ensure_text_contrast(
            colors["panel"], preferred=colors["muted"], minimum=3.4
        ),
    }


def configure_dialog_window(
    app,
    window: tk.Toplevel,
    title: str,
    geometry: str,
    *,
    modal: bool = True,
    parent=None,
    resizable: bool | None = None,
) -> None:
    palette = dialog_palette(app)
    window.title(title)
    if geometry:
        window.geometry(_parent_relative_geometry(parent or app.root, geometry))
    window.transient(parent or app.root)
    if modal:
        window.grab_set()
    if resizable is not None:
        window.resizable(resizable, resizable)
    try:
        window.configure(bg=palette["bg"])
    except Exception:
        pass


def _parent_relative_geometry(parent, geometry: str) -> str:
    if "+" in geometry:
        return geometry
    try:
        width, height = (int(part) for part in geometry.lower().split("x", 1))
    except Exception:
        return geometry

    try:
        parent.update_idletasks()
        parent_width = max(width, parent.winfo_width())
        parent_height = max(height, parent.winfo_height())
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
    except Exception:
        return geometry

    x = parent_x + max(0, (parent_width - width) // 2)
    y = parent_y + max(0, (parent_height - height) // 2)
    return f"{width}x{height}+{x}+{y}"


def bind_dialog_shortcuts(
    window: tk.Toplevel,
    *,
    confirm=None,
    cancel=None,
) -> None:
    if confirm is not None:
        window.bind("<Return>", lambda _event: confirm(), add="+")
    if cancel is not None:
        window.bind("<Escape>", lambda _event: cancel(), add="+")


def build_dialog_header(
    app,
    parent,
    title: str,
    detail: str | None = None,
    *,
    padx: int = PANEL_INNER_PAD_X,
    pady: tuple[int, int] = (PANEL_INNER_PAD_Y, PANEL_GAP),
) -> tk.Frame:
    palette = dialog_palette(app)
    header = tk.Frame(
        parent,
        bg=palette["panel"],
        bd=0,
        highlightthickness=1,
        highlightbackground=palette["border"],
        highlightcolor=palette["border"],
    )
    header._dialog_surface = "panel"  # type: ignore[attr-defined]
    header.pack(fill="x", padx=padx, pady=pady)

    title_label = tk.Label(
        header,
        text=title,
        bg=palette["panel"],
        fg=palette["text"],
        font=FONT_SECTION,
        anchor="w",
    )
    title_label._dialog_text_role = "text"  # type: ignore[attr-defined]
    title_label.pack(
        fill="x",
        padx=PANEL_INNER_PAD_X,
        pady=(PANEL_GAP, 2 if detail else PANEL_GAP),
    )

    if detail:
        detail_label = tk.Label(
            header,
            text=detail,
            bg=palette["panel"],
            fg=palette["muted"],
            font=FONT_PANEL_TITLE,
            anchor="w",
            justify="left",
            wraplength=820,
        )
        detail_label._dialog_text_role = "muted"  # type: ignore[attr-defined]
        detail_label.pack(fill="x", padx=PANEL_INNER_PAD_X, pady=(0, PANEL_GAP))

    return header


def build_dialog_footer(
    app,
    parent,
    *,
    padx: int = PANEL_INNER_PAD_X,
    pady: tuple[int, int] = (0, PANEL_INNER_PAD_X),
    side: str | None = None,
) -> tk.Frame:
    palette = dialog_palette(app)
    footer = tk.Frame(
        parent,
        bg=palette["panel"],
        bd=0,
        highlightthickness=1,
        highlightbackground=palette["border"],
        highlightcolor=palette["border"],
    )
    footer._dialog_surface = "panel"  # type: ignore[attr-defined]
    pack_options = {"fill": "x", "padx": padx, "pady": pady}
    if side is not None:
        pack_options["side"] = side
    footer.pack(**pack_options)
    return footer


def build_dialog_page_header(
    parent,
    title: str,
    detail: str,
    *,
    wraplength: int = DIALOG_SECTION_WRAP,
    padx: int = DIALOG_CONTENT_PAD_X,
    pady: tuple[int, int] = (0, PANEL_GAP),
) -> ttk.Frame:
    header = ttk.Frame(parent)
    header.pack(fill="x", padx=padx, pady=pady)
    ttk.Label(header, text=title, font=FONT_SECTION).pack(anchor="w")
    ttk.Label(header, text=detail, wraplength=wraplength).pack(
        anchor="w", pady=(2, 0)
    )
    return header


def build_dialog_section(
    parent,
    title: str,
    *,
    fill: str = "x",
    expand: bool = False,
    padx: int = DIALOG_CONTENT_PAD_X,
    pady: tuple[int, int] = (0, PANEL_GAP),
) -> ttk.Frame:
    section = ttk.Frame(parent)
    section.pack(fill=fill, expand=expand, padx=padx, pady=pady)
    ttk.Label(section, text=title, font=FONT_PANEL_TITLE).pack(
        anchor="w", pady=(0, CONTROL_GAP)
    )
    return section


def build_dialog_list_with_sidebar(
    app,
    parent,
    *,
    height: int = 14,
    padx: int = PANEL_INNER_PAD_X,
    pady: tuple[int, int] = (0, PANEL_INNER_PAD_X),
) -> tuple[tk.Listbox, ttk.Frame]:
    body = ttk.Frame(parent)
    body.pack(fill="both", expand=True, padx=padx, pady=pady)
    body.columnconfigure(0, weight=1)
    body.rowconfigure(0, weight=1)

    list_frame = ttk.Frame(body)
    list_frame.grid(row=0, column=0, sticky="nsew")
    list_frame.columnconfigure(0, weight=1)
    list_frame.rowconfigure(0, weight=1)

    listbox = tk.Listbox(list_frame, activestyle="none", height=height)
    configure_listbox_theme(listbox, app)
    scrollbar = AutoScrollbar(list_frame, orient="vertical", command=listbox.yview)
    listbox.configure(yscrollcommand=scrollbar.set)
    listbox.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    sidebar = ttk.Frame(body)
    sidebar.grid(row=0, column=1, sticky="ns", padx=(PANEL_GAP, 0))
    return listbox, sidebar


def pack_sidebar_button(
    parent,
    *,
    text: str,
    command,
    pady: tuple[int, int] = (0, CONTROL_GAP),
    style: str | None = None,
) -> ttk.Button:
    options = {"text": text, "command": command}
    if style is not None:
        options["style"] = style
    button = ttk.Button(parent, **options)
    button.pack(fill="x", pady=pady)
    return button


def refresh_dialog_theme(app, *containers) -> None:
    palette = dialog_palette(app)

    def visit(widget) -> None:
        surface = getattr(widget, "_dialog_surface", None)
        text_role = getattr(widget, "_dialog_text_role", None)
        if surface:
            try:
                widget.configure(
                    bg=palette["panel"],
                    highlightbackground=palette["border"],
                    highlightcolor=palette["border"],
                )
            except Exception:
                pass
        if text_role:
            try:
                widget.configure(
                    bg=palette["panel"],
                    fg=palette.get(text_role, palette["text"]),
                )
            except Exception:
                pass
        try:
            children = widget.winfo_children()
        except Exception:
            children = []
        for child in children:
            visit(child)

    for container in containers:
        visit(container)
