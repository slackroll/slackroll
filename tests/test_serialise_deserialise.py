# -*- coding: utf-8 -*-

import os
import sys
from tempfile import NamedTemporaryFile

import pytest
from slackroll import ChangeLog, ChangeLogEntry, try_dump, try_load

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import List, Optional, Tuple


@pytest.fixture  # type: ignore
def blacklist():
    # type: () -> List[str]
    return [
        "^\\.\\/(?!chromium|libreoffice|vlc).*$@\\/sbrepos\\/",
        "^\\./testing.*",
        "glibc-(?!zoneinfo)@^(?!http)",
    ]


@pytest.fixture  # type: ignore
def repos():
    # type: () -> List[str]
    return [
        "https://slackware.nl/people/alien/multilib/15.0/",
        "https://slackware.nl/people/alien/sbrepos/15.0/x86_64/",
    ]


@pytest.fixture  # type: ignore
def manifestlist():
    # type: () -> List[Tuple[Optional[int], str, str]]
    return [
        (
            None,
            "https://slackware.osuosl.org/slackware64-15.0/",
            "./extra/MANIFEST.bz2",
        ),
        (
            None,
            "https://slackware.osuosl.org/slackware64-15.0/",
            "./pasture/MANIFEST.bz2",
        ),
        (
            None,
            "https://slackware.osuosl.org/slackware64-15.0/",
            "./patches/MANIFEST.bz2",
        ),
        (
            None,
            "https://slackware.osuosl.org/slackware64-15.0/",
            "./slackware64/MANIFEST.bz2",
        ),
        (
            None,
            "https://slackware.osuosl.org/slackware64-15.0/",
            "./testing/MANIFEST.bz2",
        ),
        (0, "https://slackware.nl/people/alien/multilib/15.0/", "./MANIFEST.bz2"),
        (1, "https://slackware.nl/people/alien/sbrepos/15.0/x86_64/", "./MANIFEST.bz2"),
    ]


@pytest.fixture(scope="session")  # type: ignore
def changelog_pickle():
    # type: () -> Generator[None, None, None]

    # register classes in the __main__ module where they were originally pickled
    setattr(sys.modules["__main__"], "ChangeLog", ChangeLog)
    setattr(sys.modules["__main__"], "ChangeLogEntry", ChangeLogEntry)

    yield

    delattr(sys.modules["__main__"], "ChangeLog")
    delattr(sys.modules["__main__"], "ChangeLogEntry")


@pytest.fixture  # type: ignore
def changelog(changelog_pickle):
    # type: (None) -> ChangeLog
    cl = ChangeLog()
    cl.add_entry(
        ChangeLogEntry(
            "Thu Aug 15 20:07:37 UTC 2024",
            "patches/packages/libX11-1.8.10-i586-1_slack15.0.txz:  Upgraded.\n  This is a bug fix release, correcting an empty XKeysymDB file.\n  Thanks to Jonathan Woithe for the bug report. \n",
        )
    )
    cl.add_entry(
        ChangeLogEntry(
            "Wed Aug 14 19:36:01 UTC 2024",
            "patches/packages/dovecot-2.3.21.1-i586-1_slack15.0.txz:  Upgraded.\n  This update fixes security issues:\n  A large number of address headers in email resulted in excessive CPU usage.\n  Abnormally large email headers are now truncated or discarded, with a limit\n  of 10MB on a single header and 50MB for all the headers of all the parts of\n  an email.\n  For more information, see:\n    https://www.cve.org/CVERecord?id=CVE-2024-23184\n    https://www.cve.org/CVERecord?id=CVE-2024-23185\n  (* Security fix *)\n",
        )
    )
    return cl


@pytest.fixture  # type: ignore
def changelog_non_ascii(changelog_pickle):
    # type: (None) -> ChangeLog

    cl = ChangeLog()
    cl.add_entry(
        ChangeLogEntry(
            "Fri Jan 11 21:15:41 UTC 2019",
            'a/bash-5.0.000-i586-1.txz:  Upgraded.\na/glibc-zoneinfo-2018i-noarch-1.txz:  Upgraded.\na/lzlib-1.11-i586-1.txz:  Upgraded.\nap/vim-8.1.0727-i586-1.txz:  Upgraded.\n  Fixed vimrc to work with "crontab -e" again now that cron\'s files have been\n  moved into /run/cron/. Thanks to Andreas V\xc3\xb6gel.\nd/subversion-1.11.1-i586-1.txz:  Upgraded.\nn/irssi-1.1.2-i586-1.txz:  Upgraded.\n  This update addresses bugs including security and stability issues:\n  A NULL pointer dereference occurs for an "empty" nick.\n  Certain nick names could result in out-of-bounds access when printing\n  theme strings.\n  Crash due to a NULL pointer dereference w hen the number of windows\n  exceeds the available space.\n  Use-after-free when SASL messages are received in an unexpected order.\n  Use-after-free when a server is disconnected during netsplits.\n  Use-after-free when hidden lines were expired from the scroll buffer.\n  For more information, see:\n    https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-7050\n    https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-7051\n    https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-7052\n    https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-7053\n    https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-7054\n    https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-5882\n  (* Security fix *)\nxap/vim-gvim-8.1.0727-i586-1.txz:  Upgraded.\n',
        )
    )
    cl.add_entry(
        ChangeLogEntry(
            "Thu Jul 28 19:44:25 UTC 2016",
            "a/kernel-generic-4.4.16-i586-1.txz:  Upgraded.\na/kernel-generic-smp-4.4.16_smp-i686-1.txz:  Upgraded.\na/kernel-huge-4.4.16-i586-1.txz:  Upgraded.\na/kernel-huge-smp-4.4.16_smp-i686-1.txz:  Upgraded.\na/kernel-modules-4.4.16-i586-1.txz:  Upgraded.\na/kernel-modules-smp-4.4.16_smp-i686-1.txz:  Upgraded.\nd/kernel-headers-4.4.16_smp-x86-1.txz:  Upgraded.\nk/kernel-source-4.4.16_smp-noarch-1.txz:  Upgraded.\nl/libidn-1.33-i586-1.txz:  Upgraded.\n  Fixed out-of-bounds read bugs.  Fixed crashes on invalid UTF-8.\n  Thanks to Hanno B\xc3\xb6ck.\n  For more information, see:\n    http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-8948\n    http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-6261\n    http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-6262\n    http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-6263\n  (* Security fix *)\nl/libtasn1-4.9-i586-1.txz:  Upgraded.\nn/bluez-5.41-i586-1.txz:  Upgraded.\nextra/linux-4.4.16-nosmp-sdk/*:  Upgraded.\nextra/tigervnc/tigervnc-1.6.0-i586-4.txz:  Rebuilt.\n  Recompiled for xorg-server-1.18.4.\nisolinux/initrd.img:  Rebuilt.\nkernels/*:  Upgraded.\nusb-and-pxe-installers/usbboot.img:  Rebuilt.\n",
        )
    )
    return cl


def test_deserialise_py2_bl(blacklist):
    # type: (List[str]) -> None
    """Checks if we can deserialise a known good file."""

    data_file = os.path.join(
        os.path.dirname(__file__), "..", "data", "py2_blacklist.db"
    )

    assert blacklist == try_load(data_file)


def test_round_trip_serialisation_bl(blacklist):
    # type: (List[str]) -> None
    """Checks if we can round trip serialise then deserialise a value."""

    f = NamedTemporaryFile(delete=True)

    try_dump(blacklist, f.name)

    assert blacklist == try_load(f.name)

    f.close()


def test_deserialise_py2_repos(repos):
    # type: (List[str]) -> None
    """Checks if we can deserialise a known good file."""

    data_file = os.path.join(os.path.dirname(__file__), "..", "data", "py2_repos.db")

    assert repos == try_load(data_file)


def test_round_trip_serialisation_repos(repos):
    # type: (List[str]) -> None
    """Checks if we can round trip serialise then deserialise a value."""

    f = NamedTemporaryFile(delete=True)

    try_dump(repos, f.name)

    assert repos == try_load(f.name)

    f.close()


def test_deserialise_py2_manifestlist(manifestlist):
    # type: (List[str]) -> None
    """Checks if we can deserialise a known good file."""

    data_file = os.path.join(
        os.path.dirname(__file__), "..", "data", "py2_manifestlist.db"
    )

    assert manifestlist == try_load(data_file)


def test_round_trip_serialisation_manifestlist(manifestlist):
    # type: (List[str]) -> None
    """Checks if we can round trip serialise then deserialise a value."""

    f = NamedTemporaryFile(delete=True)

    try_dump(manifestlist, f.name)

    assert manifestlist == try_load(f.name)

    f.close()


def test_deserialise_py2_changelog(changelog):
    # type: (ChangeLog) -> None
    """Checks if we can deserialise a known good file."""

    data_file = os.path.join(
        os.path.dirname(__file__), "..", "data", "py2_changelog.db"
    )

    loaded = try_load(data_file)  # type: ChangeLog

    assert loaded.num_batches() == 1
    assert loaded.num_batches() == changelog.num_batches()
    assert loaded.last_batch() == changelog.last_batch()


def test_round_trip_changelog(changelog):
    # type: (ChangeLog) -> None
    """Checks if we can round trip serialise then deserialise a value."""

    f = NamedTemporaryFile(delete=True)

    try_dump(changelog, f.name)

    loaded = try_load(f.name)  # type: ChangeLog
    assert loaded.num_batches() == 1
    assert loaded.num_batches() == changelog.num_batches()
    assert loaded.last_batch() == changelog.last_batch()

    f.close()


def test_deserialise_py2_changelog_non_ascii(changelog_non_ascii):
    # type: (ChangeLog) -> None
    """Checks if we can deserialise a known good file."""

    data_file = os.path.join(
        os.path.dirname(__file__), "..", "data", "py2_changelog_non_ascii.db"
    )

    loaded = try_load(data_file)  # type: ChangeLog

    assert loaded.num_batches() == 1
    assert loaded.num_batches() == changelog_non_ascii.num_batches()
    assert loaded.last_batch() == changelog_non_ascii.last_batch()


def test_round_trip_changelog_non_ascii(changelog_non_ascii):
    # type: (ChangeLog) -> None
    """Checks if we can round trip serialise then deserialise a value."""

    f = NamedTemporaryFile(delete=True)

    try_dump(changelog_non_ascii, f.name)

    loaded = try_load(f.name)  # type: ChangeLog
    assert loaded.num_batches() == 1
    assert loaded.num_batches() == changelog_non_ascii.num_batches()
    assert loaded.last_batch() == changelog_non_ascii.last_batch()

    f.close()
