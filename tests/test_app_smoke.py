import os
import subprocess
import sys
import unittest
from pathlib import Path

from cheat_editor_manager import APP_NAME, APP_VERSION, configure_tcl_environment
from cheat_editor_manager.app import App
from cheat_editor_manager.services import theme_service


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class AppSmokeTests(unittest.TestCase):
    def test_imports_and_theme_helpers_are_available(self):
        self.assertTrue(APP_NAME)
        self.assertTrue(APP_VERSION)
        configure_tcl_environment()
        self.assertGreater(theme_service.contrast_ratio("#ffffff", "#000000"), 10)
        self.assertEqual(theme_service.normalize_hex_color("#ABCDEF"), "#abcdef")

    def test_startup_window_uses_standard_non_fullscreen_size(self):
        self.assertEqual((App.DEFAULT_WINDOW_WIDTH, App.DEFAULT_WINDOW_HEIGHT), (1180, 720))
        self.assertEqual(App._fit_startup_size(1180, 720, 1920, 1080), (1180, 720))
        self.assertEqual(App._fit_startup_size(1180, 720, 1366, 768), (1180, 688))
        fitted_width, fitted_height = App._fit_startup_size(1180, 720, 1024, 600)
        self.assertLessEqual(fitted_width, 1024)
        self.assertLessEqual(fitted_height, 600)

    def test_direct_script_entrypoint_starts_in_smoke_mode(self):
        self._run_smoke_entrypoint("cheat_editor_manager_tool.py")

    def test_package_entrypoint_starts_in_smoke_mode(self):
        self._run_smoke_entrypoint("-m", "cheat_editor_manager")

    def _run_smoke_entrypoint(self, *args: str) -> None:
        if os.environ.get("CHEAT_EDITOR_MANAGER_SKIP_GUI_SMOKE") == "1":
            self.skipTest("GUI startup smoke tests disabled by environment")

        env = os.environ.copy()
        env["CHEAT_EDITOR_MANAGER_SMOKE_EXIT"] = "1"

        completed = subprocess.run(
            [sys.executable, *args],
            cwd=PROJECT_ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        self.assertEqual(
            completed.returncode,
            0,
            f"Smoke entry point failed: {args}\nSTDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}",
        )
