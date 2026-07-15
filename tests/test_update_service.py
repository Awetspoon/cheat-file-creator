import json
import time
import unittest

from cheat_editor_manager.services.update_service import (
    GITHUB_API_VERSION,
    ReleaseInfo,
    UpdateCheckError,
    fetch_latest_release,
    find_available_update,
    is_newer_version,
    parse_version,
    release_from_payload,
    schedule_update_check,
)


RELEASE_URL = (
    "https://github.com/Awetspoon/cheat_editor_manager_tool/releases/tag/v1.4.0"
)


def release_payload(**overrides):
    payload = {
        "tag_name": "v1.4.0",
        "name": "Version 1.4.0",
        "html_url": RELEASE_URL,
        "published_at": "2026-07-15T12:00:00Z",
        "draft": False,
        "prerelease": False,
    }
    payload.update(overrides)
    return payload


class FakeResponse:
    def __init__(self, payload):
        self.raw = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self, limit):
        return self.raw[:limit]


class FakeScheduler:
    def __init__(self):
        self.callbacks = []

    def after(self, _delay, callback):
        self.callbacks.append(callback)
        return f"after-{len(self.callbacks)}"

    def run_next(self):
        self.callbacks.pop(0)()


class UpdateServiceTests(unittest.TestCase):
    def test_version_parser_and_comparison_handle_numeric_parts(self):
        self.assertEqual(parse_version("v1.4.0"), (1, 4, 0))
        self.assertEqual(parse_version("1.10.2"), (1, 10, 2))
        self.assertIsNone(parse_version("latest"))
        self.assertTrue(is_newer_version("v1.10.0", "1.9.9"))
        self.assertFalse(is_newer_version("v1.4", "1.4.0"))
        self.assertFalse(is_newer_version("v1.3.9", "1.4.0"))

    def test_release_payload_must_be_full_and_trusted(self):
        release = release_from_payload(release_payload())
        self.assertEqual(release.display_version, "1.4.0")
        self.assertEqual(release.url, RELEASE_URL)

        for invalid_payload in (
            release_payload(prerelease=True),
            release_payload(draft=True),
            release_payload(tag_name="latest"),
            release_payload(html_url="https://example.com/releases/tag/v1.4.0"),
        ):
            with self.subTest(payload=invalid_payload):
                with self.assertRaises(UpdateCheckError):
                    release_from_payload(invalid_payload)

    def test_fetch_latest_release_uses_required_github_headers(self):
        captured = {}

        def opener(request, *, timeout):
            captured["headers"] = {
                name.casefold(): value for name, value in request.header_items()
            }
            captured["timeout"] = timeout
            return FakeResponse(release_payload())

        release = fetch_latest_release(timeout=2.5, opener=opener)

        self.assertEqual(release.tag_name, "v1.4.0")
        self.assertEqual(captured["timeout"], 2.5)
        self.assertEqual(
            captured["headers"]["accept"],
            "application/vnd.github+json",
        )
        self.assertEqual(
            captured["headers"]["x-github-api-version"],
            GITHUB_API_VERSION,
        )
        self.assertTrue(captured["headers"]["user-agent"])

    def test_find_available_update_only_returns_newer_releases(self):
        newer = ReleaseInfo(
            tag_name="v1.4.1",
            name="Version 1.4.1",
            url=RELEASE_URL.replace("v1.4.0", "v1.4.1"),
            version=(1, 4, 1),
        )
        current = ReleaseInfo(
            tag_name="v1.4.0",
            name="Version 1.4.0",
            url=RELEASE_URL,
            version=(1, 4, 0),
        )

        self.assertIs(
            find_available_update("1.4.0", fetcher=lambda: newer),
            newer,
        )
        self.assertIsNone(
            find_available_update("1.4.0", fetcher=lambda: current)
        )

    def test_scheduled_check_delivers_result_from_background_worker(self):
        release = ReleaseInfo(
            tag_name="v1.4.1",
            name="Version 1.4.1",
            url=RELEASE_URL.replace("v1.4.0", "v1.4.1"),
            version=(1, 4, 1),
        )
        scheduler = FakeScheduler()
        received = []

        after_id = schedule_update_check(
            scheduler,
            "1.4.0",
            received.append,
            delay_ms=0,
            poll_interval_ms=0,
            fetcher=lambda: release,
        )
        self.assertEqual(after_id, "after-1")

        deadline = time.monotonic() + 1.0
        while not received and time.monotonic() < deadline:
            if scheduler.callbacks:
                scheduler.run_next()
            else:
                time.sleep(0.005)

        self.assertEqual(received, [release])


if __name__ == "__main__":
    unittest.main()
