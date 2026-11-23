import pytest
from slackroll import (
    download_report_hook,
    get_difftool,
    get_env_or,
    get_pager,
    get_temp_dir,
    get_visual,
    newer_than,
    optimum_size_conversion,
)

import tests

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import List


def test_download_report_hook_handles_empty_file(request):
    # type: (pytest.FixtureRequest) -> None
    calls = []  # type: List[str]
    tests.start_patch(request, "slackroll.print_flush", calls.append)

    download_report_hook("empty.txt", 0, 8192, 0)

    assert calls == ["\rDownloading empty.txt ... 100% of 0b"]


def test_get_env_or_returns_default_when_missing(request):
    # type: (pytest.FixtureRequest) -> None
    tests.start_patch(request, "slackroll.os.getenv", lambda _name: None)

    assert get_env_or("TMPDIR", "/tmp/default") == "/tmp/default"


def test_get_env_or_returns_environment_value(request):
    # type: (pytest.FixtureRequest) -> None
    tests.start_patch(request, "slackroll.os.getenv", lambda _name: "/custom/path")

    assert get_env_or("TMPDIR", "/tmp/default") == "/custom/path"


def test_get_env_wrappers_use_expected_variable_names(request):
    # type: (pytest.FixtureRequest) -> None
    seen = []

    def fake_getenv(name):
        # type: (str) -> str
        seen.append(name)
        return {
            "TMPDIR": "/tmp/override",
            "PAGER": "most",
            "PATH": "/bin:/usr/bin",
            "VISUAL": "nano",
            "SRDIFF": "diffuse",
        }[name]

    tests.start_patch(request, "slackroll.os.getenv", fake_getenv)
    tests.start_patch(
        request, "slackroll.os.path.isfile", lambda path: path == "/usr/bin/most"
    )
    tests.start_patch(
        request, "slackroll.os.access", lambda path, _mode: path == "/usr/bin/most"
    )

    assert get_temp_dir() == "/tmp/override"
    assert get_pager() == "most"
    assert get_visual() == "nano"
    assert get_difftool() == "diffuse"
    assert seen == ["TMPDIR", "PAGER", "VISUAL", "SRDIFF"]


def test_optimum_size_conversion_handles_boundaries():
    # type: () -> None
    assert optimum_size_conversion(0) == "0b"
    assert optimum_size_conversion(1023) == "1023b"
    assert optimum_size_conversion(1024) == "1.0k"
    assert optimum_size_conversion(1536) == "1.5k"
    assert optimum_size_conversion(1048576) == "1.0M"


def test_newer_than_defaults_true_when_both_missing(request):
    # type: (pytest.FixtureRequest) -> None
    tests.start_patch(request, "slackroll.os.path.exists", lambda _path: False)

    assert newer_than("missing-1", "missing-2") is True


def test_newer_than_false_when_reference_missing(request):
    # type: (pytest.FixtureRequest) -> None
    tests.start_patch(
        request,
        "slackroll.os.path.exists",
        lambda path: {"missing": False, "present": True}[path],
    )

    assert newer_than("missing", "present") is False


def test_newer_than_true_when_modified_missing(request):
    # type: (pytest.FixtureRequest) -> None
    tests.start_patch(
        request,
        "slackroll.os.path.exists",
        lambda path: {"present": True, "missing": False}[path],
    )

    assert newer_than("present", "missing") is True


def test_newer_than_compares_mtimes_when_both_exist(request):
    # type: (pytest.FixtureRequest) -> None
    tests.start_patch(request, "slackroll.os.path.exists", lambda _path: True)
    tests.start_patch(
        request,
        "slackroll.get_mtime",
        lambda path: {"newer": 20.0, "older": 10.0, "equal": 20.0}[path],
    )

    assert newer_than("newer", "older") is True
    assert newer_than("older", "newer") is False
    assert newer_than("newer", "equal") is False
