from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ...constants import DEFAULT_RETROARCH_CORES
from ...export_logic import profile_id_label
from ..style import (
    CONTROL_GAP,
    FONT_CODE_BOLD,
    FONT_PANEL_TITLE,
    PANEL_GAP,
    PANEL_INNER_PAD_X,
    PANEL_INNER_PAD_Y,
    PANEL_OUTER_PAD_X,
    TEXT_INSET_X,
    TEXT_INSET_Y,
)


CARD_PAD_X = PANEL_INNER_PAD_X
CARD_PAD_TOP = PANEL_INNER_PAD_Y
CARD_PAD_BOTTOM = PANEL_INNER_PAD_Y
CARD_GAP = CONTROL_GAP


def build_helper_panel(app) -> None:
    app._helper_layout_mode = "sidebar" if hasattr(app, "right_sidebar") else "strip"
    parent = getattr(app, "right_sidebar", app.body.inner)
    app.helper = tk.Frame(parent, bd=0, highlightthickness=1)
    if app._helper_layout_mode == "sidebar":
        app.helper.pack(fill="both", expand=True, padx=0, pady=(0, PANEL_GAP))
        app.helper.columnconfigure(0, weight=1)
    else:
        app.helper.pack(fill="x", padx=PANEL_OUTER_PAD_X, pady=(0, PANEL_GAP))
        app.helper.columnconfigure(0, weight=3, uniform="helper_content")
        app.helper.columnconfigure(1, weight=5, uniform="helper_content")

    app.helper_header = tk.Frame(app.helper, bd=0, highlightthickness=0)
    app.helper_header.grid(
        row=0,
        column=0,
        columnspan=1 if app._helper_layout_mode == "sidebar" else 2,
        sticky="ew",
        padx=PANEL_INNER_PAD_X,
        pady=(9, 4),
    )
    app.helper_header.columnconfigure(0, weight=1)
    app.helper_title = tk.Label(
        app.helper_header, text="Target Guide", font=FONT_PANEL_TITLE, anchor="w"
    )
    app.helper_title.grid(row=0, column=0, sticky="w")
    app.helper_subtitle = tk.Label(
        app.helper_header,
        text="Profile rules, required IDs, and final output preview",
        anchor="w",
    )
    app.helper_subtitle.grid(row=1, column=0, sticky="w", pady=(1, 0))

    app.helper_text = tk.StringVar(value="Select an emulator to see helper info.")
    app._helper_card = tk.Frame(app.helper, bd=0, highlightthickness=1)
    if app._helper_layout_mode == "sidebar":
        app._helper_card.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=PANEL_INNER_PAD_X,
            pady=(3, CONTROL_GAP),
        )
    else:
        app._helper_card.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(PANEL_INNER_PAD_X, CONTROL_GAP),
            pady=(3, 6),
        )
    app._helper_card.columnconfigure(0, weight=1)
    app._helper_card_title = tk.Label(
        app._helper_card, text="Profile Guidance", font=FONT_PANEL_TITLE, anchor="w"
    )
    app._helper_card_title.grid(
        row=0, column=0, sticky="w", padx=PANEL_INNER_PAD_X, pady=(8, 0)
    )
    app._helper_display = tk.Label(
        app._helper_card,
        textvariable=app.helper_text,
        justify="left",
        anchor="nw",
        padx=0,
        pady=0,
    )
    app._helper_display.grid(
        row=1, column=0, sticky="ew", padx=PANEL_INNER_PAD_X, pady=(4, 9)
    )
    app.helper.bind("<Configure>", app._on_helper_configure, add="+")

    app.tid_var = tk.StringVar()
    app.bid_var = tk.StringVar()
    app.core_var = tk.StringVar(
        value=app.prefs.get("retroarch_core", DEFAULT_RETROARCH_CORES[0])
    )
    app._preview_after = None
    _configure_live_preview(app)

    _build_atmosphere_layout(app)
    _build_switch_layout(app)
    _build_titleid_layout(app)
    _build_retroarch_layout(app)
    _build_generic_layout(app)
    _build_path_preview(app)

    app._set_helper_display(app.helper_text.get())


def _configure_live_preview(app) -> None:
    for variable in (
        app.profile_var,
        app.export_var,
        app.tid_var,
        app.bid_var,
        app.core_var,
    ):
        try:
            variable.trace_add("write", app._schedule_export_preview_update)
        except Exception:
            pass


def _target_layout_frame(app) -> tk.Frame:
    frame = tk.Frame(app.helper, bd=0, highlightthickness=1)
    if app._helper_layout_mode == "sidebar":
        frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=PANEL_INNER_PAD_X,
            pady=(0, CONTROL_GAP),
        )
    else:
        frame.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(CONTROL_GAP, PANEL_INNER_PAD_X),
            pady=(3, 6),
        )
    frame.columnconfigure(0, weight=1)
    frame.grid_remove()
    return frame


def _card_heading(
    parent: tk.Frame, *, text: str | None = None, textvariable=None
) -> tk.Label:
    label = tk.Label(
        parent,
        text=text or "",
        textvariable=textvariable,
        font=FONT_PANEL_TITLE,
    )
    label.grid(row=0, column=0, sticky="w", padx=CARD_PAD_X, pady=(CARD_PAD_TOP, 0))
    return label


def _card_hint(parent: tk.Frame, text: str, *, row: int = 1) -> tk.Label:
    label = tk.Label(parent, text=text, justify="left", anchor="w")
    label.grid(
        row=row,
        column=0,
        sticky="ew",
        padx=CARD_PAD_X,
        pady=(2, CARD_GAP),
    )
    return label


def _template_frame(parent: tk.Frame, *, row: int = 2) -> tk.Frame:
    frame = tk.Frame(parent, bd=0, highlightthickness=0)
    frame.grid(row=row, column=0, sticky="ew", padx=CARD_PAD_X, pady=(0, CARD_GAP))
    return frame


def _template_label(parent: tk.Frame, textvariable) -> tk.Label:
    label = tk.Label(
        parent,
        textvariable=textvariable,
        justify="left",
        anchor="w",
        font=FONT_CODE_BOLD,
    )
    label.pack(fill="x", padx=TEXT_INSET_X, pady=CONTROL_GAP)
    return label


def _card_note(parent: tk.Frame, textvariable, *, row: int) -> tk.Label:
    label = tk.Label(parent, textvariable=textvariable, justify="left", anchor="w")
    label.grid(
        row=row,
        column=0,
        sticky="ew",
        padx=CARD_PAD_X,
        pady=(0, CARD_PAD_BOTTOM),
    )
    return label


def _target_layouts(app) -> tuple[tk.Frame, ...]:
    return (
        app._atmo_layout,
        app._switch_layout,
        app._titleid_layout,
        app._retro_layout,
        app._generic_layout,
    )


def _build_atmosphere_layout(app) -> None:
    app._atmo_layout = _target_layout_frame(app)
    app._atmo_title = _card_heading(app._atmo_layout, text="Atmosphere export layout")
    app._atmo_hint = _card_hint(
        app._atmo_layout,
        text="The folder structure is fixed. Only TitleID and BuildID fields are editable.",
    )

    app._atmo_path_row = tk.Frame(app._atmo_layout)
    app._atmo_path_row.grid(
        row=2, column=0, sticky="ew", padx=CARD_PAD_X, pady=(0, CARD_GAP)
    )
    app._atmo_path_row.columnconfigure(0, weight=1)
    app._atmo_prefix_1 = tk.Label(app._atmo_path_row, text="SD:/atmosphere/contents/")
    app._atmo_prefix_1.grid(row=0, column=0, sticky="w")
    app._atmo_tid_entry = ttk.Entry(
        app._atmo_path_row, textvariable=app.tid_var, width=18
    )
    tid_grid = {"row": 1, "column": 0, "sticky": "ew", "pady": (3, 6)}
    if app._helper_layout_mode != "sidebar":
        tid_grid = {"row": 0, "column": 1, "sticky": "w", "padx": (6, 6)}
    app._atmo_tid_entry.grid(**tid_grid)
    app._atmo_prefix_2 = tk.Label(app._atmo_path_row, text="/cheats/")
    prefix_grid = {"row": 2, "column": 0, "sticky": "w"}
    if app._helper_layout_mode != "sidebar":
        prefix_grid = {"row": 0, "column": 2, "sticky": "w"}
    app._atmo_prefix_2.grid(**prefix_grid)
    app._atmo_bid_entry = ttk.Entry(
        app._atmo_path_row, textvariable=app.bid_var, width=28
    )
    bid_grid = {"row": 3, "column": 0, "sticky": "ew", "pady": (3, 6)}
    if app._helper_layout_mode != "sidebar":
        bid_grid = {"row": 0, "column": 3, "sticky": "w", "padx": (6, 6)}
    app._atmo_bid_entry.grid(**bid_grid)
    app._atmo_suffix = tk.Label(app._atmo_path_row, text=".txt")
    suffix_grid = {"row": 4, "column": 0, "sticky": "w"}
    if app._helper_layout_mode != "sidebar":
        suffix_grid = {"row": 0, "column": 4, "sticky": "w"}
    app._atmo_suffix.grid(**suffix_grid)

    app._atmo_path_note = _card_hint(
        app._atmo_layout,
        text=(
            "BuildID changes when the game updates, but the Atmosphere folder "
            "layout itself stays fixed."
        ),
        row=3,
    )


def _build_switch_layout(app) -> None:
    app._switch_layout_title = tk.StringVar(value="Switch emulator layout")
    app._switch_layout_template = tk.StringVar(value="")
    app._switch_layout_note = tk.StringVar(value="")
    app._switch_layout = _target_layout_frame(app)
    app._switch_layout_heading = _card_heading(
        app._switch_layout,
        textvariable=app._switch_layout_title,
    )
    app._switch_layout_hint = _card_hint(
        app._switch_layout,
        text=(
            "This target uses the emulator's folder pattern. Enter TitleID and "
            "BuildID(s) for the file it expects."
        ),
    )

    app._switch_layout_template_frame = _template_frame(app._switch_layout)
    app._switch_layout_template_label = _template_label(
        app._switch_layout_template_frame, app._switch_layout_template
    )

    app._switch_inputs = tk.Frame(app._switch_layout)
    app._switch_inputs.grid(
        row=3, column=0, sticky="ew", padx=CARD_PAD_X, pady=(0, CARD_GAP)
    )
    app._switch_inputs.columnconfigure(1, weight=1)
    app._switch_tid_title = tk.Label(app._switch_inputs, text="TitleID (TID):")
    app._switch_tid_title.grid(row=0, column=0, sticky="w")
    app._switch_tid_entry = ttk.Entry(
        app._switch_inputs, textvariable=app.tid_var, width=18
    )
    if app._helper_layout_mode == "sidebar":
        app._switch_tid_entry.grid(row=1, column=0, sticky="ew", pady=(3, 6))
        bid_label_grid = {"row": 2, "column": 0, "sticky": "w"}
        bid_entry_grid = {"row": 3, "column": 0, "sticky": "ew", "pady": (3, 0)}
    else:
        app._switch_tid_entry.grid(row=0, column=1, sticky="w", padx=(8, 14))
        bid_label_grid = {"row": 0, "column": 2, "sticky": "w"}
        bid_entry_grid = {"row": 0, "column": 3, "sticky": "w", "padx": (8, 0)}
    app._switch_bid_title = tk.Label(app._switch_inputs, text="BuildID(s) (BID):")
    app._switch_bid_title.grid(**bid_label_grid)
    app._switch_bid_entry = ttk.Entry(
        app._switch_inputs, textvariable=app.bid_var, width=28
    )
    app._switch_bid_entry.grid(**bid_entry_grid)

    app._switch_layout_note_label = _card_note(
        app._switch_layout, app._switch_layout_note, row=4
    )


def _build_titleid_layout(app) -> None:
    app._titleid_layout_title = tk.StringVar(value="ID-based export layout")
    app._titleid_layout_template = tk.StringVar(value="")
    app._titleid_layout_note = tk.StringVar(value="")
    app._titleid_field_label = tk.StringVar(value="TitleID / Game ID:")
    app._titleid_layout = _target_layout_frame(app)
    app._titleid_layout_heading = _card_heading(
        app._titleid_layout,
        textvariable=app._titleid_layout_title,
    )
    app._titleid_hint = _card_hint(
        app._titleid_layout,
        text="This target uses a required ID for the cheat filename or export folder.",
    )

    app._titleid_template_frame = _template_frame(app._titleid_layout)
    app._titleid_template_label = _template_label(
        app._titleid_template_frame, app._titleid_layout_template
    )

    app._titleid_inputs = tk.Frame(app._titleid_layout)
    app._titleid_inputs.grid(
        row=3, column=0, sticky="ew", padx=CARD_PAD_X, pady=(0, CARD_GAP)
    )
    app._titleid_inputs.columnconfigure(0, weight=1)
    app._titleid_label = tk.Label(
        app._titleid_inputs, textvariable=app._titleid_field_label
    )
    app._titleid_label.grid(row=0, column=0, sticky="w")
    app._titleid_entry = ttk.Entry(
        app._titleid_inputs, textvariable=app.tid_var, width=18
    )
    if app._helper_layout_mode == "sidebar":
        app._titleid_entry.grid(row=1, column=0, sticky="ew", pady=(3, 0))
    else:
        app._titleid_entry.grid(row=0, column=1, sticky="w", padx=(8, 0))
    app._titleid_note_label = _card_note(
        app._titleid_layout, app._titleid_layout_note, row=4
    )


def _build_retroarch_layout(app) -> None:
    app._retro_layout_template = tk.StringVar(value="")
    app._retro_layout_note = tk.StringVar(value="")
    app._retro_layout = _target_layout_frame(app)
    app._retro_layout_heading = _card_heading(
        app._retro_layout, text="RetroArch export layout"
    )
    app._retro_layout_hint = _card_hint(
        app._retro_layout,
        text=(
            "Choose the core folder first. Quick Export then places the cheat "
            "in RetroArch's cheats layout."
        ),
    )

    app._retro_layout_template_frame = _template_frame(app._retro_layout)
    app._retro_layout_template_label = _template_label(
        app._retro_layout_template_frame, app._retro_layout_template
    )

    app._retro_inputs = tk.Frame(app._retro_layout)
    app._retro_inputs.grid(
        row=3, column=0, sticky="ew", padx=CARD_PAD_X, pady=(0, CARD_GAP)
    )
    app._retro_inputs.columnconfigure(0, weight=1)
    app._core_label = tk.Label(app._retro_inputs, text="RetroArch Core:")
    app._core_cb = ttk.Combobox(
        app._retro_inputs,
        textvariable=app.core_var,
        values=app.prefs.get("retroarch_cores", DEFAULT_RETROARCH_CORES),
        state="readonly",
        width=18,
    )
    app._core_manage = ttk.Button(
        app._retro_inputs, text="Manage Cores...", command=app.manage_retroarch_cores
    )
    app._core_label.grid(row=0, column=0, sticky="w")
    if app._helper_layout_mode == "sidebar":
        app._core_cb.grid(row=1, column=0, sticky="ew", pady=(3, CONTROL_GAP))
        core_manage_grid = {"row": 2, "column": 0, "sticky": "ew"}
    else:
        app._core_cb.grid(row=0, column=1, sticky="w", padx=(8, 10))
        core_manage_grid = {"row": 0, "column": 2, "sticky": "w"}
    app._core_cb.bind("<<ComboboxSelected>>", lambda _e: app._save_retroarch_core())
    app._core_manage.grid(**core_manage_grid)

    app._retro_layout_note_label = _card_note(
        app._retro_layout, app._retro_layout_note, row=4
    )


def _build_generic_layout(app) -> None:
    app._generic_layout_title = tk.StringVar(value="Target export layout")
    app._generic_layout_template = tk.StringVar(value="")
    app._generic_layout_note = tk.StringVar(value="")
    app._generic_layout = _target_layout_frame(app)
    app._generic_layout_heading = _card_heading(
        app._generic_layout,
        textvariable=app._generic_layout_title,
    )
    app._generic_layout_hint = _card_hint(
        app._generic_layout,
        text=(
            "This target keeps a fixed export pattern. Use Quick Export to "
            "build the folder or file layout for you."
        ),
    )

    app._generic_layout_template_frame = _template_frame(app._generic_layout)
    app._generic_layout_template_label = _template_label(
        app._generic_layout_template_frame, app._generic_layout_template
    )
    app._generic_layout_note_label = _card_note(
        app._generic_layout, app._generic_layout_note, row=3
    )


def _build_path_preview(app) -> None:
    app.path_preview = tk.StringVar(value="")
    app._path_preview_frame = tk.Frame(app.helper, bd=0, highlightthickness=0)
    app._path_preview_frame.grid(
        row=3 if app._helper_layout_mode == "sidebar" else 2,
        column=0,
        columnspan=1 if app._helper_layout_mode == "sidebar" else 2,
        sticky="ew",
        padx=PANEL_INNER_PAD_X,
        pady=(0, PANEL_GAP),
    )
    app._path_preview_frame.columnconfigure(0, weight=1)
    app._path_preview_title = tk.Label(
        app._path_preview_frame, text="Export Preview", font=FONT_PANEL_TITLE, anchor="w"
    )
    app._path_preview_title.grid(row=0, column=0, sticky="w")
    app._path_preview_label = tk.Label(
        app._path_preview_frame,
        textvariable=app.path_preview,
        justify="left",
        anchor="w",
        padx=TEXT_INSET_X,
        pady=TEXT_INSET_Y,
        bd=0,
        highlightthickness=1,
    )
    app._path_preview_label.grid(row=1, column=0, sticky="ew", pady=(4, 0))


def show_core_layout(app, show: bool) -> None:
    _set_layout_visible(app._retro_layout, show)


def _set_layout_visible(layout: tk.Frame, show: bool) -> None:
    if show:
        layout.grid()
    else:
        layout.grid_remove()


def _show_only_layout(app, active_layout: tk.Frame) -> None:
    for layout in _target_layouts(app):
        _set_layout_visible(layout, layout is active_layout)


def refresh_target_cards(app, prof: str, info: dict) -> None:
    kind = info.get("kind", "generic")
    ext_text = " ".join(info.get("extensions") or [app._primary_extension(info)])

    if app._is_atmosphere_profile(prof, info):
        return

    if kind == "switch":
        app._switch_layout_title.set(f"{prof} layout")
        app._switch_layout_template.set(app._profile_template_path(prof, info))
        app._switch_layout_note.set(
            "TID selects the title folder. BID is usually the cheat file name "
            "and can change when the game updates. "
            f"File types: {ext_text}"
        )
        return

    if app._uses_id_layout(info):
        app._titleid_layout_title.set(f"{prof} layout")
        app._titleid_field_label.set(app._profile_id_field_label(info))
        app._titleid_hint.configure(
            text=app._profile_id_hint(info) or "Use the ID this target expects."
        )
        app._titleid_layout_template.set(app._profile_template_path(prof, info))
        note = app._profile_id_hint(info) or "Use the ID this target expects."
        if info.get("citra_enabled"):
            note += " Quick Export adds *citra_enabled if it is missing."
        elif info.get("fixed_filename"):
            note += " The folder uses that ID, while the cheat file name itself stays fixed."
        else:
            note += " Quick Export writes one file for that ID."
        app._titleid_layout_note.set(f"{note} File types: {ext_text}")
        return

    if kind == "retroarch":
        current_core = (
            app.core_var.get() or "Default (no subfolder)"
        ).strip() or "Default (no subfolder)"
        app._retro_layout_template.set(app._profile_template_path(prof, info))
        if current_core.casefold() == "default (no subfolder)":
            core_note = "Current core folder: Default (no subfolder)."
        else:
            core_note = f"Current core folder: {current_core}."
        app._retro_layout_note.set(f"{core_note} File types: {ext_text}")
        return

    app._generic_layout_title.set(f"{prof} layout")
    app._generic_layout_template.set(app._profile_template_path(prof, info))
    if kind == "singlefile":
        note = "This target exports one fixed file under the selected Export Root."
    elif kind == "modded":
        note = (
            "Point Export Root or Emulator Paths at the SD or homebrew folder "
            "you actually want to target."
        )
    else:
        note = (
            "Quick Export builds the folder and filename pattern above under "
            "the selected Export Root."
        )
    app._generic_layout_note.set(f"{note} File types: {ext_text}")


def refresh_profile_info(app) -> None:
    prof = app.profile_var.get()
    info = app.get_profile_info(prof)
    kind = info.get("kind", "generic")
    is_atmosphere = app._is_atmosphere_profile(prof, info)

    refresh_target_cards(app, prof, info)

    if is_atmosphere:
        _show_only_layout(app, app._atmo_layout)
    elif kind == "switch":
        _show_only_layout(app, app._switch_layout)
    elif app._uses_id_layout(info):
        _show_only_layout(app, app._titleid_layout)
    elif kind == "retroarch":
        _show_only_layout(app, app._retro_layout)
    else:
        _show_only_layout(app, app._generic_layout)

    notes = (info.get("notes") or "").strip()
    if is_atmosphere:
        base = "Atmosphere exports use a fixed folder layout. Fill in TitleID and BuildID below."
    elif kind == "switch":
        base = notes or (
            "Switch emulator exports follow the target layout shown below. Fill in "
            "TitleID and BuildID(s) for the selected target."
        )
    elif app._uses_id_layout(info):
        base = notes or (
            f"This target exports by {profile_id_label(info)} instead of using "
            "a free-form filename."
        )
    elif kind == "retroarch":
        base = notes or (
            "RetroArch exports are grouped by core folder, then saved as a "
            "cheat file for the selected game."
        )
    else:
        base = notes or (
            "Quick Export builds the target layout shown below using the "
            "selected Export Root."
        )

    extensions = info.get("extensions", [".txt"]) or [".txt"]
    extension_line = "Expected file types: " + " ".join(extensions)
    if is_atmosphere:
        tip_line = "Tip: only the TID and BID boxes are editable for Atmosphere exports."
    elif kind == "switch":
        tip_line = (
            "Tip: the template card shows the target's folder pattern while "
            "TID and BID stay editable."
        )
    elif app._uses_id_layout(info):
        tip_line = (
            f"Tip: enter the {profile_id_label(info)} and Quick Export builds "
            "the final cheat path for you."
        )
    elif kind == "retroarch":
        tip_line = (
            "Tip: choose the core here before exporting so the file lands in "
            "the right cheat folder."
        )
    else:
        tip_line = "Tip: Convert & Save still works when you want a manual filename or location."
    app._set_helper_display(base + "\n\n" + extension_line + "\n" + tip_line)
    app.update_export_preview()
