import os
from tkinter import ttk
import unittest

from cheat_editor_manager.ui.widgets import Scrollable
from tests.gui_test_utils import create_offscreen_root, destroy_root, offscreen_geometry


class ScrollableWidgetTests(unittest.TestCase):
    def setUp(self):
        if os.environ.get("CHEAT_EDITOR_MANAGER_SKIP_GUI_SMOKE") == "1":
            self.skipTest("GUI widget tests disabled by environment")
        self.root = create_offscreen_root()

    def tearDown(self):
        destroy_root(self.root)

    def test_scrollbars_stay_hidden_when_content_fits(self):
        self.root.geometry(offscreen_geometry(320, 180))
        scrollable = Scrollable(self.root)
        scrollable.pack(fill="both", expand=True)
        content = ttk.Frame(scrollable.inner, width=120, height=40)
        content.grid(row=0, column=0)
        content.grid_propagate(False)

        self.root.update_idletasks()
        self.root.update()

        self.assertFalse(scrollable.v.winfo_ismapped())
        self.assertFalse(scrollable.h.winfo_ismapped())

    def test_horizontal_scrollbar_appears_when_content_is_wider(self):
        self.root.geometry(offscreen_geometry(260, 160))
        scrollable = Scrollable(self.root)
        scrollable.pack(fill="both", expand=True)
        content = ttk.Frame(scrollable.inner, width=900, height=40)
        content.grid(row=0, column=0)
        content.grid_propagate(False)

        self.root.update_idletasks()
        self.root.update()

        self.assertTrue(scrollable.h.winfo_ismapped())
        self.assertFalse(scrollable.v.winfo_ismapped())


if __name__ == "__main__":
    unittest.main()
