# Cheat Editor Manager Tool

![Cheat Editor Manager Tool](assets/app-fullscreen.png)

![Version](https://img.shields.io/badge/version-1.4.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

Cheat Editor Manager Tool is a Windows desktop app for editing cheat files and exporting them to the folder layout expected by emulators, CFW setups, and homebrew targets.

It is built for users who already have cheat text and want a cleaner way to load it, edit it, fill the required IDs, preview the output path, and save it in the right place.

## Download

For normal use, download the ready-built Windows program. Python is not required.

[Latest Release](https://github.com/Awetspoon/cheat_editor_manager_tool/releases/latest)

1. Open the latest release link above.
2. Expand **Assets** if GitHub has collapsed the download list.
3. Download **`cheat_editor_manager_tool.exe`**.
4. Open the EXE to start the app. No installer or setup process is required.

Only download the EXE from this official repository. The current build is not
code-signed, so Windows may show a SmartScreen warning on first launch.

On a normal startup, the app checks GitHub for the latest published full release in
the background. No GitHub account or API key is needed. If a newer version exists,
the app shows **View Release** and **Later** options. It never downloads or installs
an update automatically, and an unavailable internet connection does not stop the app.

## What The Program Does

- Lets you write, paste, load, clean up, and save cheat text
- Detects supported IDs from known file paths where possible
- Shows the required TID, BID, CRC, serial, title ID, or core fields for the selected target
- Builds the correct output path before writing files
- Exports quickly to the expected emulator or CFW folder layout
- Keeps manual **Convert & Save** available when you want full control
- Saves reusable cheat snippets as templates
- Saves cheat source websites in Help Links
- Keeps custom emulator profiles separate from built-in CFW profiles
- Notifies you when a newer published GitHub release is available

## Quick Start

1. Open the app.
2. Choose a target group, such as **CFW / Homebrew**, **PC / Emulator**, or **Custom Emulators**.
3. Choose the target profile, such as Atmosphere, Ryujinx, PCSX2, RetroArch, or Dolphin.
4. Click **Load File** or paste cheat text into the editor.
5. Check the Helper panel for required IDs and the export preview.
6. Fill any missing ID fields.
7. Click **Quick Export** to save to the correct profile layout.

Use **Convert & Save** when you want to choose the save location and file extension yourself.

## Supported Targets

### Switch And CFW

- Atmosphere (Switch CFW)
- Yuzu
- Ryujinx
- Sudachi
- Suyu

### Emulators And Homebrew Profiles

- Citra (3DS)
- RetroArch
- Dolphin
- PCSX2
- PPSSPP
- DuckStation
- Cemu
- Xenia
- RPCS3
- Nintendo 3DS (Luma)
- PSP (CFW)
- PS Vita (taiHEN)
- Wii (Homebrew)
- Wii U (CFW)

User-added emulator profiles appear under **Custom Emulators** so they do not get mixed into the hardcoded CFW layouts.

## Main UI Sections

- **Header:** app identity, light/dark mode, Templates, Help Links, and Settings.
- **Target controls:** target group, target profile, profile details, and export root controls.
- **Helper panel:** required ID fields, profile notes, and live export preview.
- **Cheat editor:** the main text area with undo, redo, clear, wrap, scrolling, and optional drag-and-drop.
- **Action bar:** Load File, Quick Export, Convert & Save, and current status.
- **Templates:** saved cheat text snippets that can be edited and loaded into the editor.
- **Help Links:** saved cheat source websites where users found codes or notes. The app opens links in the browser; it does not download cheats automatically.
- **Settings:** profiles, appearance, and export-root preferences.

## ID Detection

When you load a cheat file, the app tries to read useful IDs from known layouts. For example:

- Switch layouts can fill TID and BID fields.
- Citra layouts can fill title IDs.
- Dolphin layouts can fill game IDs.
- PCSX2 layouts can fill CRC values.

If the file path does not contain enough information, the app leaves the fields empty and lets you enter them manually.

## What The App Does Not Do

- It does not download cheats automatically.
- It does not inject cheats into games, consoles, or emulators.
- Its editing and export features do not require accounts, cloud sync, API keys, or an internet connection.
- It does not replace emulator-specific cheat validation tools.

## User Data

The app stores preferences locally on the computer. This includes custom profiles, templates, Help Links, appearance settings, RetroArch core choices, and export-root overrides.

Built-in profiles are protected so CFW and emulator layouts stay reliable. Custom profiles are intended for extra emulator-only export rules.

## Run From Source

Use Python 3.10 or newer.

```bash
python -m pip install -e ".[dev]"
python cheat_editor_manager_tool.py
```

Package entry point:

```bash
python -m cheat_editor_manager
```

Optional drag-and-drop support:

```bash
python -m pip install -e ".[dev,dnd]"
```

`tkinterdnd2` is optional. If it is not installed, the app still runs and uses the normal **Load File** button.

## Test

Run the full test suite:

```bash
python -B -m unittest discover -s tests -p "test*.py" -q
```

The smoke tests can launch the app in a safe one-shot mode:

```bash
$env:CHEAT_EDITOR_MANAGER_SMOKE_EXIT = "1"
python -B cheat_editor_manager_tool.py
```

Compile check:

```bash
python -B -m compileall -q assets/generate_brand_assets.py cheat_editor_manager tests hooks
```

## Build For Windows

```bash
python -m PyInstaller --clean --noconfirm cheat_editor_manager_tool.spec
```

Output:

```text
dist/cheat_editor_manager_tool.exe
```

The build uses the custom Tk/Tcl hooks in `hooks/` and vendored Tcl/Tk runtime files in `vendor/tcl/`.

## Project Notes For Developers

The codebase is organised so UI, app logic, storage, and export rules are easier to maintain separately.

```text
cheat_editor_manager/
  app.py             App startup and main wiring
  app_actions.py     Thin UI callback wrappers
  export_logic.py    Pure export/path rules
  profiles.py        Built-in and custom profile helpers
  services/          Export, loading, help-link, core, and theme services
  storage/           Preferences and template storage
  ui/                Panels, dialogs, widgets, style, and theme code
tests/               Logic, storage, service, and GUI smoke tests
assets/              App icons, screenshots, logos, and brand files
hooks/               PyInstaller Tk/Tcl packaging hooks
vendor/tcl/          Vendored Tcl/Tk runtime files
```

Keep new export rules in `export_logic.py`, keep user-facing orchestration in `services/`, keep saved data handling in `storage/`, and keep visual UI work in `ui/`.

## Future Expansion Points

- Add more emulator or CFW targets through the profile/export rule system.
- Add stronger ID detection for more known cheat folder layouts.
- Improve template management with categories or search if the list grows.
- Add more focused tests whenever a new export layout is added.
- Keep dialogs small and section-based so Settings, Templates, and Help Links stay easy to use.

## Documentation

- This README explains what the program does and how to run it.
- [assets/README.md](assets/README.md) explains runtime assets, retained brand-source files, and screenshot usage.

## Known Limitations

- Source runs require Python with Tkinter support.
- Drag-and-drop requires optional `tkinterdnd2`.
- Export correctness still depends on choosing the right target profile and entering the required IDs.

## License

MIT License. See [LICENSE](LICENSE).
