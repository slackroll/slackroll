import re

import pytest

import tests
from slackroll import (
    add_blacklist_exprs,
    del_blacklist_exprs,
    get_blacklist_re,
    print_blacklist,
    slackroll_blacklist_filename,
)

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
    return ["entry1", "entry2", "entry3@myrepo"]


def test_get_blacklist_re(blacklist):
    # type: (List[str]) -> None
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        res = get_blacklist_re()

        assert len(res) == 3
        assert (re.compile("entry1"), re.compile("")) == res[0]
        assert (re.compile("entry2"), re.compile("")) == res[1]
        assert (re.compile("entry3"), re.compile("myrepo")) == res[2]


def test_print_blacklist(blacklist):
    # type: (List[str]) -> None
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("slackroll.print_list_or") as print_list_or_mock:
            print_blacklist()

            print_list_or_mock.assert_called_with(
                ["0     entry1", "1     entry2", "2     entry3@myrepo"],
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
                ["entry1", "entry2", "entry3@myrepo", "newentry1", "newentry2"],
                slackroll_blacklist_filename,
            )


def test_add_blacklist_exprs_invalid(blacklist):
    # type: (List[str]) -> None
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("sys.exit") as exit_mock:
            exit_mock.side_effect = ValueError

            try:
                add_blacklist_exprs(["test@[\\]"])
            except:
                pass
            else:
                raise ValueError("failed")

            exit_mock.assert_called_with(
                'ERROR: "test@[\\]" is an invalid regular expression'
            )


def test_add_blacklist_exprs_invalid_url_regex(blacklist):
    # type: (List[str]) -> None
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("sys.exit") as exit_mock:
            exit_mock.side_effect = ValueError

            try:
                add_blacklist_exprs(["[\\]"])
            except:
                pass
            else:
                raise ValueError("failed")

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
                ["entry2", "entry3@myrepo"], slackroll_blacklist_filename
            )


def test_del_blacklist_exprs_multiple(blacklist):
    # type: (List[str]) -> None
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("slackroll.try_dump") as try_dump_mock:
            del_blacklist_exprs(["0", "1"])

            try_dump_mock.assert_called_with(
                ["entry3@myrepo"], slackroll_blacklist_filename
            )


def test_del_blacklist_exprs_invalid_index_negative(blacklist):
    # type: (List[str]) -> None
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("sys.exit") as exit_mock:
            exit_mock.side_effect = ValueError

            try:
                del_blacklist_exprs(["-1"])
            except:
                pass
            else:
                raise ValueError("failed")

            exit_mock.assert_called_with("ERROR: invalid blacklist entry index: -1")


def test_del_blacklist_exprs_invalid_index_exceeds_length(blacklist):
    # type: (List[str]) -> None
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("sys.exit") as exit_mock:
            exit_mock.side_effect = ValueError

            try:
                del_blacklist_exprs(["3"])
            except:
                pass
            else:
                raise ValueError("failed")

            exit_mock.assert_called_with("ERROR: invalid blacklist entry index: 3")
