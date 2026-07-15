# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path


PROJECT_ROOT = Path.cwd()
HOOKS_ROOT = PROJECT_ROOT / "hooks"
RUNTIME_ASSET_NAMES = (
    "app-icon.ico",
    "app-icon.png",
    "icon-256.png",
    "mark-48.png",
)
RUNTIME_ASSETS = [
    (str(PROJECT_ROOT / "assets" / asset_name), "assets")
    for asset_name in RUNTIME_ASSET_NAMES
]


a = Analysis(
    ["cheat_editor_manager_tool.py"],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=[
        (str(PROJECT_ROOT / "vendor" / "tcl" / "tcl8.6"), "_tcl_data"),
        (str(PROJECT_ROOT / "vendor" / "tcl" / "tk8.6"), "_tk_data"),
        *RUNTIME_ASSETS,
    ],
    hiddenimports=[
        "tkinter",
        "tkinter.font",
        "tkinter.ttk",
    ],
    hookspath=[str(HOOKS_ROOT)],
    hooksconfig={},
    runtime_hooks=[str(HOOKS_ROOT / "runtime" / "pyi_rth_tcl_vendor.py")],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="cheat_editor_manager_tool",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    icon=str(PROJECT_ROOT / "assets" / "app-icon.ico"),
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
