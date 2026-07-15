import os
from tkinter import ttk
import unittest
from unittest.mock import patch

from cheat_editor_manager.services.update_service import ReleaseInfo
from cheat_editor_manager.ui.dialogs.update_dialog import show_update_available
from tests.gui_test_utils import create_test_app, destroy_root


RELEASE_URL = (
    "https://github.com/Awetspoon/cheat_editor_manager_tool/releases/tag/v9.9.9"
)


def collect_widgets(widget, widget_type):
    matches = []
    if isinstance(widget, widget_type):
        matches.append(widget)
    for child in widget.winfo_children():
        matches.extend(collect_widgets(child, widget_type))
    return matches


class UpdateDialogTests(unittest.TestCase):
    def setUp(self):
        if os.environ.get("CHEAT_EDITOR_MANAGER_SKIP_GUI_SMOKE") == "1":
            self.skipTest("GUI update dialog tests disabled by environment")
        self.app = create_test_app()
        self.release = ReleaseInfo(
            tag_name="v9.9.9",
            name="Test Release",
            url=RELEASE_URL,
            version=(9, 9, 9),
        )

    def tearDown(self):
        destroy_root(getattr(self.app, "root", None))

    def test_view_release_button_opens_github_and_closes_dialog(self):
        window = show_update_available(self.app, "1.4.0", self.release)
        self.app.root.update_idletasks()
        buttons = {
            button.cget("text"): button
            for button in collect_widgets(window, ttk.Button)
        }

        self.assertIn("View Release", buttons)
        self.assertIn("Later", buttons)
        with patch(
            "cheat_editor_manager.ui.dialogs.update_dialog.webbrowser.open_new_tab",
            return_value=True,
        ) as open_new_tab:
            buttons["View Release"].invoke()

        open_new_tab.assert_called_once_with(RELEASE_URL)
        self.assertIsNone(self.app._update_dialog)

    def test_later_button_closes_without_opening_browser(self):
        window = show_update_available(self.app, "1.4.0", self.release)
        buttons = {
            button.cget("text"): button
            for button in collect_widgets(window, ttk.Button)
        }

        with patch(
            "cheat_editor_manager.ui.dialogs.update_dialog.webbrowser.open_new_tab"
        ) as open_new_tab:
            buttons["Later"].invoke()

        open_new_tab.assert_not_called()
        self.assertIsNone(self.app._update_dialog)


if __name__ == "__main__":
    unittest.main()
