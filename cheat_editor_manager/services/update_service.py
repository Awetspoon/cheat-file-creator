from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import json
import queue
import re
import threading
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


LATEST_RELEASE_API_URL = (
    "https://api.github.com/repos/Awetspoon/cheat_editor_manager_tool/releases/latest"
)
GITHUB_API_VERSION = "2026-03-10"
RELEASE_URL_PATH_PREFIX = "/Awetspoon/cheat_editor_manager_tool/releases/"
MAX_RESPONSE_BYTES = 1_000_000
DEFAULT_TIMEOUT_SECONDS = 5.0
DEFAULT_START_DELAY_MS = 1_200
DEFAULT_POLL_INTERVAL_MS = 100
VERSION_PATTERN = re.compile(
    r"^[vV]?(?P<version>\d+(?:\.\d+){1,3})(?:[-+][0-9A-Za-z.-]+)?$"
)


class UpdateCheckError(RuntimeError):
    """Raised when release information cannot be read or trusted."""


@dataclass(frozen=True, slots=True)
class ReleaseInfo:
    tag_name: str
    name: str
    url: str
    version: tuple[int, ...]
    published_at: str = ""

    @property
    def display_version(self) -> str:
        if self.tag_name[:1].lower() == "v":
            return self.tag_name[1:]
        return self.tag_name


def parse_version(value: str) -> tuple[int, ...] | None:
    match = VERSION_PATTERN.fullmatch(str(value or "").strip())
    if match is None:
        return None
    return tuple(int(part) for part in match.group("version").split("."))


def is_newer_version(candidate: str, installed: str) -> bool:
    candidate_parts = parse_version(candidate)
    installed_parts = parse_version(installed)
    if candidate_parts is None or installed_parts is None:
        return False

    width = max(len(candidate_parts), len(installed_parts))
    candidate_key = candidate_parts + (0,) * (width - len(candidate_parts))
    installed_key = installed_parts + (0,) * (width - len(installed_parts))
    return candidate_key > installed_key


def fetch_latest_release(
    *,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    opener=None,
) -> ReleaseInfo:
    request = Request(
        LATEST_RELEASE_API_URL,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "CheatEditorManagerTool",
            "X-GitHub-Api-Version": GITHUB_API_VERSION,
        },
    )
    open_url = opener or urlopen

    try:
        with open_url(request, timeout=timeout) as response:
            raw_response = response.read(MAX_RESPONSE_BYTES + 1)
    except (OSError, TimeoutError) as exc:
        raise UpdateCheckError("GitHub release information is unavailable.") from exc

    if len(raw_response) > MAX_RESPONSE_BYTES:
        raise UpdateCheckError("GitHub returned an unexpectedly large response.")

    try:
        payload = json.loads(raw_response.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise UpdateCheckError("GitHub returned invalid release information.") from exc

    return release_from_payload(payload)


def release_from_payload(payload) -> ReleaseInfo:
    if not isinstance(payload, dict):
        raise UpdateCheckError("GitHub returned an invalid release record.")
    if payload.get("draft") or payload.get("prerelease"):
        raise UpdateCheckError("GitHub did not return a full published release.")

    tag_name = str(payload.get("tag_name") or "").strip()
    version = parse_version(tag_name)
    if version is None:
        raise UpdateCheckError("The latest GitHub release has an invalid version tag.")

    release_url = str(payload.get("html_url") or "").strip()
    if not is_trusted_release_url(release_url):
        raise UpdateCheckError("GitHub returned an untrusted release URL.")

    return ReleaseInfo(
        tag_name=tag_name,
        name=str(payload.get("name") or tag_name).strip() or tag_name,
        url=release_url,
        version=version,
        published_at=str(payload.get("published_at") or "").strip(),
    )


def is_trusted_release_url(url: str) -> bool:
    parsed = urlsplit(str(url or "").strip())
    return (
        parsed.scheme == "https"
        and (parsed.hostname or "").casefold() == "github.com"
        and parsed.path.casefold().startswith(RELEASE_URL_PATH_PREFIX.casefold())
    )


def find_available_update(
    installed_version: str,
    *,
    fetcher: Callable[[], ReleaseInfo] = fetch_latest_release,
) -> ReleaseInfo | None:
    release = fetcher()
    if is_newer_version(release.tag_name, installed_version):
        return release
    return None


def schedule_update_check(
    scheduler,
    installed_version: str,
    on_update: Callable[[ReleaseInfo], None],
    *,
    delay_ms: int = DEFAULT_START_DELAY_MS,
    poll_interval_ms: int = DEFAULT_POLL_INTERVAL_MS,
    fetcher: Callable[[], ReleaseInfo] = fetch_latest_release,
):
    """Schedule one non-blocking update check and return the first after ID."""

    def start_worker() -> None:
        results: queue.Queue[ReleaseInfo | None] = queue.Queue(maxsize=1)

        def worker() -> None:
            try:
                result = find_available_update(
                    installed_version,
                    fetcher=fetcher,
                )
            except UpdateCheckError:
                result = None
            results.put(result)

        thread = threading.Thread(
            target=worker,
            name="release-update-check",
            daemon=True,
        )
        thread.start()

        def poll_result() -> None:
            try:
                result = results.get_nowait()
            except queue.Empty:
                if thread.is_alive():
                    scheduler.after(poll_interval_ms, poll_result)
                return
            if result is not None:
                on_update(result)

        scheduler.after(poll_interval_ms, poll_result)

    return scheduler.after(delay_ms, start_worker)
