# cheat-file-editor
Cheat file creator + quick export paths for emulators
# 🎮 Cheat File Creator

Cheat File Creator is a simple GUI tool for creating cheat files and exporting them to the correct folder structure for popular emulators and console cheat systems.

✅ Works on Windows  
✅ Uses profiles.json to define emulators, extensions, and templates  
✅ Includes Quick Export (auto folders) and Convert & Save (manual save)

---

## ✨ What this app does

- Create and edit cheat files
- Load templates designed for each emulator
- Automatically build correct cheat folders
- Save files in supported formats per emulator

---

## 🧩 Emulator / Console Profiles

Choose an emulator from the dropdown and the app will automatically:

- Show the correct Quick Export fields
- Offer valid file extensions
- Load available templates for that emulator

All emulator definitions live in **profiles.json**.

---

## 📝 Templates

Templates help you start with the correct cheat format.

### How to use templates
1. Select an emulator
2. Select a template
3. Click **Open Template**
4. Choose to Replace or Append

### Default templates
- You can set a template as the default for each emulator
- Defaults are saved automatically

Buttons:
- Reset Default Template (current emulator)
- Reset ALL Defaults (every emulator)

Defaults are stored in **user_prefs.json**.

---

## 🧰 Add Cheat (Helper)

Click **Add Cheat (Helper)** to safely insert cheat blocks.

- Automatically formats cheats for supported emulators
- Prevents breaking strict cheat formats
- Generic helper is used for unsupported formats

---

## 🚀 Quick Export (Auto Folder Building)

Quick Export builds the correct folder path under your Export Root.

### Supported Quick Export targets

- RetroArch  
  ExportRoot/RetroArch/cheats/Core/ROM.cht

- PPSSPP (PSP)  
  ExportRoot/PPSSPP/PSP/Cheats/GAME_ID.ini

- Dolphin (GameCube / Wii)  
  ExportRoot/Dolphin/GameSettings/GAME_ID.ini

- PCSX2  
  ExportRoot/PCSX2/cheats/CRC.pnach

- Nintendo Switch (Atmosphère)  
  ExportRoot/Switch/atmosphere/contents/TID/cheats/BID.txt

- RetroArch – Citra core  
  ExportRoot/RetroArch/saves/Citra/cheats/game_id.txt

---

## 💾 Convert & Save

Use Convert & Save when you want full control.

It lets you:
- Choose where to save
- Choose from valid extensions for the selected emulator

---

## 📂 Export Root

Export Root is the base folder used by Quick Export.

Buttons:
- Open Folder – opens Export Root
- Change… – select a new folder
- Reset Default – restore the recommended default

Export Root is saved in **user_prefs.json**.

---

## 🧱 Project Files

Typical folder layout:

- cheat_creator.exe (Windows app)
- profiles.json (emulator definitions and templates)
- user_prefs.json (auto-generated user settings)
- README.md

---

## ➕ Adding New Emulators / Consoles

Edit **profiles.json** and add a new entry inside the profiles list.

Each profile includes:
- id (unique identifier)
- name (shown in the app)
- default_extension
- extensions (used by Convert & Save)
- templates (optional but recommended)

After editing:
- Restart the app OR
- Click Reload profiles

---

## 🪟 Build Windows EXE (Developers)

1. Install Python  
2. Install PyInstaller  
3. Build the app

The EXE will appear in the dist folder.

---

Enjoy creating cheats 🎮
