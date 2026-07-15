from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent


class BuildConfigTests(unittest.TestCase):
    def test_tkinterdnd2_is_optional_in_project_metadata(self):
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

        self.assertIn('dnd = ["tkinterdnd2>=0.4"]', pyproject)
        dependencies_block = pyproject.split("[project.optional-dependencies]", 1)[0]
        self.assertNotIn("tkinterdnd2", dependencies_block)

    def test_manifest_includes_runtime_asset_and_vendor_folders(self):
        manifest = (ROOT / "MANIFEST.in").read_text(encoding="utf-8")

        self.assertIn("recursive-include assets *", manifest)
        self.assertIn("recursive-include vendor/tcl *", manifest)
        self.assertIn("recursive-include hooks *.py", manifest)
        self.assertNotIn("recursive-include docs", manifest)
        self.assertNotIn("recursive-include scripts", manifest)

    def test_gitignore_excludes_generated_build_outputs(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

        for pattern in ("build/", "dist/", "_tmp_mei/", "**/__pycache__/"):
            self.assertIn(pattern, gitignore)

    def test_pyinstaller_spec_references_packaged_runtime_paths(self):
        spec = (ROOT / "cheat_editor_manager_tool.spec").read_text(encoding="utf-8")

        for asset_name in ("app-icon.ico", "app-icon.png", "icon-256.png", "mark-48.png"):
            self.assertIn(f'"{asset_name}"', spec)
        self.assertNotIn('(str(PROJECT_ROOT / "assets"), "assets")', spec)
        self.assertIn('"_tcl_data"', spec)
        self.assertIn('"_tk_data"', spec)


if __name__ == "__main__":
    unittest.main()
