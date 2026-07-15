from __future__ import annotations

from pathlib import Path
from typing import Optional

from .services import export_service
from .services import retroarch_core_service
from .services.file_load_service import load_file_into_app
from .storage import save_prefs
from .ui.dialogs.extension_dialog import pick_extension_for_save
from .ui.panels.editor_panel import handle_drop_files


class ExportFileActionsMixin:
    """Stable App callback methods for file loading, previewing, and exporting."""

    def _effective_export_root_for_profile(self, prof: str) -> Path:
        return export_service.effective_export_root_for_profile(self, prof)

    def _get_all_known_extensions(self):
        return export_service.get_all_known_extensions(self)

    def _pick_extension_for_save(self, prof: str):
        profile_exts, all_exts = export_service.extension_options_for_profile(self, prof)
        return pick_extension_for_save(self, prof, profile_exts, all_exts)

    def convert_save(self):
        return export_service.convert_save(self)

    def load_file(self, filepath: Optional[str] = None):
        return load_file_into_app(self, filepath)

    def _on_drop_files(self, event):
        return handle_drop_files(self, event)

    def _validate_export_inputs(self, prof: str) -> Optional[str]:
        return export_service.validate_export_inputs_for_profile(self, prof)

    def build_export_plan(self, prof: str) -> dict:
        return export_service.build_export_plan_from_app(self, prof)

    def _schedule_export_preview_update(self, *_):
        return export_service.schedule_export_preview_update(self, *_)

    def _on_editor_modified(self, *_):
        return export_service.on_editor_modified(self, *_)

    def update_export_preview(self):
        return export_service.update_export_preview(self)

    def quick_export(self):
        return export_service.quick_export(self)


class RetroarchCoreActionsMixin:
    """Stable App callback methods for RetroArch core preferences and widgets."""

    def _save_retroarch_core(self):
        retroarch_core_service.set_current_core(self.prefs, self.core_var.get())
        save_prefs(self.prefs)
        try:
            self.refresh_profile_info()
        except Exception:
            pass

    def _audit_retroarch_cores(self):
        before = (
            list(self.prefs.get("retroarch_cores") or []),
            str(self.prefs.get("retroarch_core") or ""),
        )
        retroarch_core_service.ensure_core_preferences(self.prefs)
        after = (
            list(self.prefs.get("retroarch_cores") or []),
            str(self.prefs.get("retroarch_core") or ""),
        )
        if before == after:
            return
        try:
            save_prefs(self.prefs)
        except OSError as exc:
            recorder = getattr(self, "_record_startup_warning", None)
            if callable(recorder):
                recorder(f"Preferences were updated but could not be saved: {exc}")

    def _sync_core_dropdown(self):
        cores, current = retroarch_core_service.ensure_core_preferences(self.prefs)
        self.core_var.set(current)
        try:
            self._core_cb.configure(values=cores)
        except Exception:
            pass
