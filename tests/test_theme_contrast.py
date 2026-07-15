import unittest

from cheat_editor_manager.constants import (
    DEFAULT_BUTTON_COLORS,
    DEFAULT_THEME_DARK,
    DEFAULT_THEME_LIGHT,
)
from cheat_editor_manager.services import theme_service


class ThemeContrastTests(unittest.TestCase):
    def assertContrastAtLeast(self, fg: str, bg: str, minimum: float) -> None:
        ratio = theme_service.contrast_ratio(fg, bg)
        self.assertGreaterEqual(
            ratio,
            minimum,
            msg=f"Expected contrast >= {minimum:.2f}, got {ratio:.2f} for {fg} on {bg}",
        )

    def test_default_button_palettes_keep_text_readable(self):
        for theme in (DEFAULT_THEME_LIGHT, DEFAULT_THEME_DARK):
            for key, bg in DEFAULT_BUTTON_COLORS.items():
                palette = theme_service.button_palette(bg, theme["bg"], theme["text"])
                self.assertContrastAtLeast(palette["fg"], palette["bg"], 4.5)
                self.assertContrastAtLeast(palette["active_fg"], palette["active_bg"], 4.5)
                self.assertContrastAtLeast(palette["disabled_fg"], palette["disabled_bg"], 3.0)

    def test_selection_palette_keeps_text_readable(self):
        for accent in DEFAULT_BUTTON_COLORS.values():
            bg, fg = theme_service.selection_palette(accent)
            self.assertContrastAtLeast(fg, bg, 4.5)

    def test_effective_button_colors_normalizes_custom_values(self):
        colors = theme_service.effective_button_colors(
            {
                "button_colors": {
                    "primary": "not-a-color",
                    "secondary": "#ABCDEF",
                    "unused": "#000000",
                }
            }
        )

        self.assertEqual(colors["primary"], DEFAULT_BUTTON_COLORS["primary"].lower())
        self.assertEqual(colors["secondary"], "#abcdef")
        self.assertNotIn("unused", colors)

    def test_sanitize_theme_repairs_low_contrast_custom_values(self):
        broken = {key: "#f7f3ea" for key in DEFAULT_THEME_LIGHT}
        sanitized = theme_service.sanitize_theme_colors(broken, DEFAULT_THEME_LIGHT)
        self.assertContrastAtLeast(sanitized["text"], sanitized["bg"], 4.5)
        self.assertContrastAtLeast(sanitized["muted"], sanitized["panel"], 3.4)
        self.assertContrastAtLeast(sanitized["editor_fg"], sanitized["editor_bg"], 4.5)
        self.assertGreaterEqual(
            theme_service.contrast_ratio(sanitized["border"], sanitized["bg"]), 1.2
        )
        self.assertGreaterEqual(
            theme_service.contrast_ratio(sanitized["entry"], sanitized["panel"]), 1.08
        )


if __name__ == "__main__":
    unittest.main()
