import os
import sys

import pytest
import toml

from slackroll import (
    add_blacklist_exprs,
    del_blacklist_exprs,
    print_blacklist,
    slackroll_blacklist_filename,
)

PY2 = sys.version_info[0] <= 2

if PY2:
    from mock import patch, MagicMock
else:
    from unittest.mock import patch, MagicMock


@pytest.fixture
def blacklist():
    return ["entry1", "entry2", "entry3"]


def test_print_blacklist(blacklist):
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("slackroll.print_list_or") as print_list_or_mock:
            print_blacklist()

            print_list_or_mock.assert_called_with(
                ["0     entry1", "1     entry2", "2     entry3"],
                "Blacklisted expressions:",
                "No blacklisted expressions",
            )


def test_add_blacklist_exprs(blacklist):
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("slackroll.try_dump") as try_dump_mock:
            add_blacklist_exprs(["newentry1", "newentry2"])

            try_dump_mock.assert_called_with(
                ["entry1", "entry2", "entry3", "newentry1", "newentry2"],
                slackroll_blacklist_filename,
            )


def test_add_blacklist_exprs_invalid(blacklist):
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("sys.exit") as exit_mock:
            exit_mock.side_effect = ValueError

            try:
                add_blacklist_exprs(["test@[\\]"])
                raise ValueError()
            except:
                pass

            exit_mock.assert_called_with(
                'ERROR: "test@[\\]" is an invalid regular expression'
            )


def test_add_blacklist_exprs_invalid_url_regex(blacklist):
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("sys.exit") as exit_mock:
            exit_mock.side_effect = ValueError

            try:
                add_blacklist_exprs(["[\\]"])
                raise ValueError()
            except:
                pass

            exit_mock.assert_called_with(
                'ERROR: "[\\]" is an invalid regular expression'
            )


def test_del_blacklist_exprs(blacklist):
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("slackroll.try_dump") as try_dump_mock:
            del_blacklist_exprs([0])

            try_dump_mock.assert_called_with(
                ["entry2", "entry3"], slackroll_blacklist_filename
            )


def test_del_blacklist_exprs_multiple(blacklist):
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("slackroll.try_dump") as try_dump_mock:
            del_blacklist_exprs([0, 1])

            try_dump_mock.assert_called_with(["entry3"], slackroll_blacklist_filename)


def test_del_blacklist_exprs_invalid_index_negative(blacklist):
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("sys.exit") as exit_mock:
            exit_mock.side_effect = ValueError

            try:
                del_blacklist_exprs([-1])
                raise ValueError()
            except:
                pass

            exit_mock.assert_called_with("ERROR: invalid blacklist entry index: -1")


def test_del_blacklist_exprs_invalid_index_exceeds_length(blacklist):
    with patch("slackroll.get_blacklist") as get_blacklist_mock:
        get_blacklist_mock.return_value = blacklist

        with patch("sys.exit") as exit_mock:
            exit_mock.side_effect = ValueError

            try:
                del_blacklist_exprs([3])
                raise ValueError()
            except:
                pass

            exit_mock.assert_called_with("ERROR: invalid blacklist entry index: 3")
