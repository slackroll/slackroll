# -*- coding: utf-8 -*-
import pytest
from slackroll import (
    kernel_clean_operation,
    kernel_upgrade_operation,
)

import tests

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import Dict, List, Tuple

    from slackroll import SlackwarePackage


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _kernel_pkg(name, version):
    # type: (str, str) -> SlackwarePackage
    return tests.build_pkg(name, version, "./slackware64/a")


def _kernel_upgrade(local_list, remote_list, plist):
    # type: (Dict[str, List[SlackwarePackage]], Dict[str, List[SlackwarePackage]], tests.PersistentList) -> None
    kernel_upgrade_operation(local_list, remote_list, plist)  # type: ignore[arg-type]


def _kernel_clean(local_list, remote_list, plist):
    # type: (Dict[str, List[SlackwarePackage]], Dict[str, List[SlackwarePackage]], tests.PersistentList) -> None
    kernel_clean_operation(local_list, remote_list, plist)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# kernel_upgrade_operation tests
# ---------------------------------------------------------------------------


def test_kernel_upgrade_prints_no_outdated_when_none(request):
    # type: (pytest.FixtureRequest) -> None
    # installed kernel package - not outdated
    pkg = _kernel_pkg("kernel-generic", "6.1.0")
    local_list = tests.package_map([pkg])
    remote_list = tests.package_map([pkg])
    plist = tests.PersistentList({"kernel-generic": 2})  # state_installed

    fake_stdout = tests.Mock()
    tests.start_patch(request, "slackroll.sys.stdout", fake_stdout)
    tests.start_patch(request, "slackroll.slackroll_batch_mode", True)
    tests.start_patch(
        request, "slackroll.install_operations_family", lambda *a, **kw: None
    )
    tests.start_patch(request, "slackroll.post_kernel_operation", lambda: None)

    _kernel_upgrade(local_list, remote_list, plist)

    assert "No outdated kernel packages" in tests.mock_output(fake_stdout)


def test_kernel_upgrade_upgrades_outdated_kernel_pkg(request):
    # type: (pytest.FixtureRequest) -> None
    old_pkg = _kernel_pkg("kernel-generic", "6.1.0")
    new_pkg = _kernel_pkg("kernel-generic", "6.6.0")
    local_list = tests.package_map([old_pkg])
    remote_list = tests.package_map([new_pkg])
    plist = tests.PersistentList({"kernel-generic": 6})  # state_outdated

    install_calls = []  # type: List[Tuple[str, List[str], bool]]
    post_calls = []  # type: List[int]

    def fake_install(op, names, ll, rl, pl, use_pasture=True):
        # type: (str, List[str], object, object, object, bool) -> None
        install_calls.append((op, list(names), use_pasture))

    tests.start_patch(request, "slackroll.slackroll_batch_mode", True)
    tests.start_patch(request, "slackroll.install_operations_family", fake_install)
    tests.start_patch(
        request, "slackroll.post_kernel_operation", lambda: post_calls.append(1)
    )

    _kernel_upgrade(local_list, remote_list, plist)

    assert install_calls == [("installpkg", ["kernel-generic"], False)]
    assert post_calls == [1]


def test_kernel_upgrade_ignores_non_kernel_pkgs(request):
    # type: (pytest.FixtureRequest) -> None
    # 'vim' is outdated but not a kernel package
    vim_old = tests.build_pkg("vim", "8.2", "./slackware64/ap")
    vim_new = tests.build_pkg("vim", "9.1", "./slackware64/ap")
    local_list = tests.package_map([vim_old])
    remote_list = tests.package_map([vim_new])
    plist = tests.PersistentList({"vim": 6})  # state_outdated

    install_calls = []  # type: List[List[str]]

    def fake_install(op, names, ll, rl, pl, use_pasture=True):
        # type: (str, List[str], object, object, object, bool) -> None
        install_calls.append(list(names))

    fake_stdout = tests.Mock()
    tests.start_patch(request, "slackroll.sys.stdout", fake_stdout)
    tests.start_patch(request, "slackroll.slackroll_batch_mode", True)
    tests.start_patch(request, "slackroll.install_operations_family", fake_install)
    tests.start_patch(request, "slackroll.post_kernel_operation", lambda: None)

    _kernel_upgrade(local_list, remote_list, plist)

    # No outdated kernel packages -- message printed and nothing is installed
    assert "No outdated kernel packages" in tests.mock_output(fake_stdout)
    assert install_calls == []


def test_kernel_upgrade_does_not_call_post_kernel_when_empty(request):
    # type: (pytest.FixtureRequest) -> None
    post_calls = []  # type: List[int]
    tests.start_patch(request, "slackroll.sys.stdout", tests.Mock())
    tests.start_patch(request, "slackroll.slackroll_batch_mode", True)
    tests.start_patch(
        request, "slackroll.install_operations_family", lambda *a, **kw: None
    )
    tests.start_patch(
        request, "slackroll.post_kernel_operation", lambda: post_calls.append(1)
    )

    _kernel_upgrade({}, {}, tests.PersistentList())

    assert post_calls == []


# ---------------------------------------------------------------------------
# kernel_clean_operation tests
# ---------------------------------------------------------------------------


def test_kernel_clean_prints_no_obsolete_when_none(request):
    # type: (pytest.FixtureRequest) -> None
    # Same version locally and remotely -> not obsolete
    pkg = _kernel_pkg("kernel-generic", "6.6.0")
    local_list = tests.package_map([pkg])
    remote_list = tests.package_map([pkg])
    plist = tests.PersistentList({"kernel-generic": 2})  # state_installed

    fake_stdout = tests.Mock()
    tests.start_patch(request, "slackroll.sys.stdout", fake_stdout)
    tests.start_patch(request, "slackroll.remove_pkgs", lambda pkgs: None)
    tests.start_patch(request, "slackroll.post_kernel_operation", lambda: None)

    _kernel_clean(local_list, remote_list, plist)

    assert "No obsolete kernel packages found" in tests.mock_output(fake_stdout)


def test_kernel_clean_removes_local_version_absent_from_remote(request):
    # type: (pytest.FixtureRequest) -> None
    # Old local version not present remotely -> obsolete
    old_pkg = _kernel_pkg("kernel-generic", "6.1.0")
    new_pkg = _kernel_pkg("kernel-generic", "6.6.0")
    local_list = tests.package_map([old_pkg])
    # Remote only has the new version; old_pkg is absent
    remote_list = tests.package_map([new_pkg])
    plist = tests.PersistentList({"kernel-generic": 2})  # state_installed

    removed = []  # type: List[object]
    post_calls = []  # type: List[int]
    tests.start_patch(
        request, "slackroll.remove_pkgs", lambda pkgs: removed.extend(pkgs)
    )
    tests.start_patch(
        request, "slackroll.post_kernel_operation", lambda: post_calls.append(1)
    )

    _kernel_clean(local_list, remote_list, plist)

    assert removed == [old_pkg]
    assert post_calls == [1]


def test_kernel_clean_skips_outdated_kernel_pkgs(request):
    # type: (pytest.FixtureRequest) -> None
    # Outdated (state 6) kernel packages are not cleaned -- only installed (state 2) ones
    old_pkg = _kernel_pkg("kernel-generic", "6.1.0")
    new_pkg = _kernel_pkg("kernel-generic", "6.6.0")
    local_list = tests.package_map([old_pkg])
    remote_list = tests.package_map([new_pkg])
    plist = tests.PersistentList(
        {"kernel-generic": 6}
    )  # state_outdated -- should be skipped

    fake_stdout = tests.Mock()
    removed = []  # type: List[object]
    tests.start_patch(request, "slackroll.sys.stdout", fake_stdout)
    tests.start_patch(
        request, "slackroll.remove_pkgs", lambda pkgs: removed.extend(pkgs)
    )
    tests.start_patch(request, "slackroll.post_kernel_operation", lambda: None)

    _kernel_clean(local_list, remote_list, plist)

    assert removed == []
    assert "No obsolete kernel packages found" in tests.mock_output(fake_stdout)


def test_kernel_clean_ignores_non_kernel_pkgs(request):
    # type: (pytest.FixtureRequest) -> None
    old_vim = tests.build_pkg("vim", "8.2", "./slackware64/ap")
    new_vim = tests.build_pkg("vim", "9.1", "./slackware64/ap")
    local_list = tests.package_map([old_vim])
    remote_list = tests.package_map([new_vim])
    plist = tests.PersistentList({"vim": 2})  # installed but not a kernel pkg

    fake_stdout = tests.Mock()
    removed = []  # type: List[object]
    tests.start_patch(request, "slackroll.sys.stdout", fake_stdout)
    tests.start_patch(
        request, "slackroll.remove_pkgs", lambda pkgs: removed.extend(pkgs)
    )
    tests.start_patch(request, "slackroll.post_kernel_operation", lambda: None)

    _kernel_clean(local_list, remote_list, plist)

    assert removed == []
    assert "No obsolete kernel packages found" in tests.mock_output(fake_stdout)


def test_kernel_clean_does_not_call_post_when_nothing_removed(request):
    # type: (pytest.FixtureRequest) -> None
    post_calls = []  # type: List[int]
    fake_stdout = tests.Mock()
    tests.start_patch(request, "slackroll.sys.stdout", fake_stdout)
    tests.start_patch(request, "slackroll.remove_pkgs", lambda pkgs: None)
    tests.start_patch(
        request, "slackroll.post_kernel_operation", lambda: post_calls.append(1)
    )

    _kernel_clean({}, {}, tests.PersistentList())

    assert post_calls == []
