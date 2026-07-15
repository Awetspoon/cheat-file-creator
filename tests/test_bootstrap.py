from __future__ import annotations

import os
import unittest
from pathlib import Path

from cheat_editor_manager.resources import tk_file_path


class BootstrapTests(unittest.TestCase):
    def test_tk_file_path_uses_extended_windows_paths(self):
        runtime_path = tk_file_path(Path.cwd())

        if os.name == "nt":
            self.assertTrue(runtime_path.startswith("\\\\?\\"))
        else:
            self.assertEqual(runtime_path, str(Path.cwd().resolve()))


if __name__ == "__main__":
    unittest.main()
