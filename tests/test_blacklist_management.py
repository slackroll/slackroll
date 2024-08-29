# -*- coding: utf-8 -*-

import os
import re
from tempfile import NamedTemporaryFile

import pytest
from slackroll import (
    add_blacklist_exprs,
    del_blacklist_exprs,
    get_blacklist_re,
    print_blacklist,
    slackroll_blacklist_filename,
    try_dump,
    try_load,
)

import tests

if tests.PY2:
    from mock import patch  # type: ignore
else:
    from unittest.mock import patch

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import List


@pytest.fixture  # type: ignore
def blacklist():
    # type: () -> List[str]
    return ["entry1", "entry2", "entry3@myrepo", "äöü"]


def test_get_blacklist_re(blacklist):
    # type: (List[str]) -> None
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        res = get_blacklist_re()

        assert len(res) == 4
        assert (re.compile("entry1"), re.compile("")) == res[0]
        assert (re.compile("entry2"), re.compile("")) == res[1]
        assert (re.compile("entry3"), re.compile("myrepo")) == res[2]
        assert (re.compile("äöü"), re.compile("")) == res[3]


def test_print_blacklist(blacklist):
    # type: (List[str]) -> None
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("slackroll.print_list_or") as print_list_or_mock:
            print_blacklist()

            print_list_or_mock.assert_called_with(
                ["0     entry1", "1     entry2", "2     entry3@myrepo", "3     äöü"],
                "Blacklisted expressions:",
                "No blacklisted expressions",
            )


def test_add_blacklist_exprs(blacklist):
    # type: (List[str]) -> None
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("slackroll.try_dump") as try_dump_mock:
            add_blacklist_exprs(["newentry1", "newentry2"])

            try_dump_mock.assert_called_with(
                ["entry1", "entry2", "entry3@myrepo", "äöü", "newentry1", "newentry2"],
                slackroll_blacklist_filename,
            )


def test_add_blacklist_exprs_invalid(blacklist):
    # type: (List[str]) -> None
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("sys.exit") as exit_mock:
            exit_mock.side_effect = ValueError("boom")

            with pytest.raises(ValueError):
                add_blacklist_exprs(["test@[\\]"])

            exit_mock.assert_called_with(
                'ERROR: "test@[\\]" is an invalid regular expression'
            )


def test_add_blacklist_exprs_invalid_url_regex(blacklist):
    # type: (List[str]) -> None
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("sys.exit") as exit_mock:
            exit_mock.side_effect = ValueError

            with pytest.raises(ValueError):
                add_blacklist_exprs(["[\\]"])

            exit_mock.assert_called_with(
                'ERROR: "[\\]" is an invalid regular expression'
            )


def test_del_blacklist_exprs(blacklist):
    # type: (List[str]) -> None
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("slackroll.try_dump") as try_dump_mock:
            del_blacklist_exprs(["0"])

            try_dump_mock.assert_called_with(
                ["entry2", "entry3@myrepo", "äöü"], slackroll_blacklist_filename
            )


def test_del_blacklist_exprs_multiple(blacklist):
    # type: (List[str]) -> None
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("slackroll.try_dump") as try_dump_mock:
            del_blacklist_exprs(["0", "1"])

            try_dump_mock.assert_called_with(
                ["entry3@myrepo", "äöü"], slackroll_blacklist_filename
            )


def test_del_blacklist_exprs_invalid_index_negative(blacklist):
    # type: (List[str]) -> None
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("sys.exit") as exit_mock:
            exit_mock.side_effect = ValueError

            with pytest.raises(ValueError):
                del_blacklist_exprs(["-1"])

            exit_mock.assert_called_with("ERROR: invalid blacklist entry index: -1")


def test_del_blacklist_exprs_invalid_index_exceeds_length(blacklist):
    # type: (List[str]) -> None
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("sys.exit") as exit_mock:
            exit_mock.side_effect = ValueError

            with pytest.raises(ValueError):
                del_blacklist_exprs(["4"])

            exit_mock.assert_called_with("ERROR: invalid blacklist entry index: 4")


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
