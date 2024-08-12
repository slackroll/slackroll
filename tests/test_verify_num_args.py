from typing import ValuesView

from mock import patch  # type: ignore
from slackroll import verify_num_args


def test_verify_num_args_zero_or_one():
    # type: () -> None

    verify_num_args(-2, "myop", [])
    verify_num_args(-2, "myop", ["test"])

    with patch("sys.exit") as exit_mock:
        exit_mock.side_effect = ValueError

        try:
            verify_num_args(-2, "myop", ["test", "after"])
        except ValueError:
            pass
        else:
            raise ValueError("failed")

        exit_mock.assert_called_with("ERROR: myop expects one argument or no arguments")


def test_verify_num_args_any_nonzero():
    # type: () -> None

    verify_num_args(-1, "myop", ["test"])
    verify_num_args(-1, "myop", ["test", "after"])

    with patch("sys.exit") as exit_mock:
        exit_mock.side_effect = ValueError

        try:
            verify_num_args(-1, "myop", [])
        except ValueError:
            pass
        else:
            raise ValueError("failed")

        exit_mock.assert_called_with("ERROR: myop expects more arguments")


def test_verify_num_args_exect():
    # type: () -> None

    verify_num_args(0, "myop", [])
    verify_num_args(1, "myop", ["after"])
    verify_num_args(2, "myop", ["after", "before"])

    with patch("sys.exit") as exit_mock:
        exit_mock.side_effect = ValueError

        try:
            verify_num_args(0, "myop", ["arg"])
        except ValueError:
            pass
        else:
            raise ValueError("failed")

        exit_mock.assert_called_with("ERROR: myop expects no arguments")

    with patch("sys.exit") as exit_mock:
        exit_mock.side_effect = ValueError

        try:
            verify_num_args(1, "myop", [])
        except ValueError:
            pass
        else:
            raise ValueError("failed")

        exit_mock.assert_called_with("ERROR: myop expects 1 argument")

    with patch("sys.exit") as exit_mock:
        exit_mock.side_effect = ValueError

        try:
            verify_num_args(2, "myop", ["arg"])
        except ValueError:
            pass
        else:
            raise ValueError("failed")

        exit_mock.assert_called_with("ERROR: myop expects 2 arguments")
