import pytest
import slackroll
from slackroll import (
    handle_writable_dir,
    standardize_locales,
    yield_slackroll_local_pkgs_dir,
)

import tests

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import Dict, List


@pytest.mark.parametrize(  # type: ignore
    "pkg_dir", ["/var/lib/pkgtools/packages", "/var/log/packages"]
)
def test_imported_main_initializes_local_package_paths(request, pkg_dir):
    # type: (pytest.FixtureRequest, str) -> None
    tests.start_patch(request, "slackroll.sys.argv", ["slackroll", "version"])
    tests.start_patch(request, "slackroll.os.path.isdir", lambda path: path == pkg_dir)
    tests.start_patch(request, "slackroll.standardize_locales")
    tests.start_patch(request, "slackroll.socket.setdefaulttimeout")
    tests.start_patch(request, "slackroll.handle_writable_dir")
    tests.start_patch(request, "slackroll.slackroll_local_pkgs_dir", create=True)
    tests.start_patch(request, "slackroll.slackroll_local_pkgs_glob", create=True)

    exc_info = pytest.raises(SystemExit, slackroll.main)

    assert exc_info.value.code is None
    assert slackroll.slackroll_local_pkgs_dir == pkg_dir
    assert slackroll.slackroll_local_pkgs_glob == pkg_dir + "/*"


def test_standardize_locales_clears_known_locale_vars_and_sets_lang(request):
    # type: (pytest.FixtureRequest) -> None
    environ = {
        "LANG": "en_US.UTF-8",
        "LC_TIME": "de_DE.UTF-8",
        "LC_MONETARY": "fr_FR.UTF-8",
        "PATH": "/usr/bin",
    }  # type: Dict[str, str]

    tests.start_patch(request, "slackroll.os.environ", environ)

    standardize_locales()

    assert environ == {
        "LANG": "C",
        "PATH": "/usr/bin",
    }


def test_yield_slackroll_local_pkgs_dir_returns_first_existing_directory(request):
    # type: (pytest.FixtureRequest) -> None
    tests.start_patch(
        request,
        "slackroll.slackroll_local_pkgs_dir_names",
        ["/missing", "/var/log/packages", "/var/lib/pkgtools/packages"],
    )
    tests.start_patch(
        request,
        "slackroll.os.path.isdir",
        lambda path: path == "/var/log/packages",
    )

    generator = yield_slackroll_local_pkgs_dir()

    if tests.PY2:
        assert generator.next() == "/var/log/packages"
    else:
        assert next(generator) == "/var/log/packages"


def test_yield_slackroll_local_pkgs_dir_exits_when_none_exist(request):
    # type: (pytest.FixtureRequest) -> None
    exit_mock = tests.start_patch(request, "sys.exit")
    exit_mock.side_effect = ValueError("boom")
    tests.start_patch(
        request,
        "slackroll.slackroll_local_pkgs_dir_names",
        ["/missing-a", "/missing-b"],
    )
    tests.start_patch(request, "slackroll.os.path.isdir", lambda _path: False)

    generator = yield_slackroll_local_pkgs_dir()

    def advance():
        # type: () -> str
        if tests.PY2:
            return generator.next()
        return next(generator)

    pytest.raises(ValueError, advance)

    exit_mock.assert_called_with("ERROR: unable to find local packages directory")


def test_handle_writable_dir_creates_missing_directory(request):
    # type: (pytest.FixtureRequest) -> None
    created = []  # type: List[str]

    tests.start_patch(request, "slackroll.os.path.exists", lambda _path: False)
    tests.start_patch(request, "slackroll.os.mkdir", lambda path: created.append(path))
    tests.start_patch(request, "slackroll.os.access", lambda _path, _mode: True)
    tests.start_patch(
        request, "slackroll.os.path.isdir", lambda path: path == "/tmp/newdir"
    )

    handle_writable_dir("/tmp/newdir")

    assert created == ["/tmp/newdir"]


def test_handle_writable_dir_exits_when_path_is_not_directory(request):
    # type: (pytest.FixtureRequest) -> None
    exit_mock = tests.start_patch(request, "sys.exit")
    exit_mock.side_effect = ValueError("boom")
    tests.start_patch(request, "slackroll.os.path.exists", lambda _path: True)
    tests.start_patch(request, "slackroll.os.path.isdir", lambda _path: False)

    pytest.raises(ValueError, handle_writable_dir, "/tmp/not-a-dir")

    exit_mock.assert_called_with("ERROR: /tmp/not-a-dir exists but is not a directory")


def test_handle_writable_dir_exits_when_directory_not_accessible(request):
    # type: (pytest.FixtureRequest) -> None
    exit_mock = tests.start_patch(request, "sys.exit")
    exit_mock.side_effect = ValueError("boom")
    tests.start_patch(request, "slackroll.os.path.exists", lambda _path: True)
    tests.start_patch(request, "slackroll.os.path.isdir", lambda _path: True)
    tests.start_patch(request, "slackroll.os.access", lambda _path, _mode: False)

    pytest.raises(ValueError, handle_writable_dir, "/tmp/no-access")

    exit_mock.assert_called_with(
        "ERROR: directory /tmp/no-access is not available for read and writing (are you root?)"
    )


def test_handle_writable_dir_exits_when_mkdir_fails(request):
    # type: (pytest.FixtureRequest) -> None
    exit_mock = tests.start_patch(request, "sys.exit")
    exit_mock.side_effect = ValueError("boom")
    tests.start_patch(request, "slackroll.os.path.exists", lambda _path: False)

    def raise_oserror(_path):
        # type: (str) -> None
        raise OSError("permission denied")

    tests.start_patch(request, "slackroll.os.mkdir", raise_oserror)

    pytest.raises(ValueError, handle_writable_dir, "/tmp/cannot-create")

    exit_mock.assert_called_with("ERROR: permission denied")
