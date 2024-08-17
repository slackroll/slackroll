import os
import shutil
from tempfile import mkdtemp

import pytest
from slackroll import load_persistent_db, slackroll_state_installed

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
    from typing import Generator


@pytest.fixture  # type: ignore
def temp_dir():
    # type: () -> Generator[str, None, None]
    dir = mkdtemp()

    yield dir

    shutil.rmtree(dir)


if tests.PY2:

    def test_switch_format(temp_dir):
        # type: (str) -> None
        """Checks if we can open a known good file."""

        with patch("slackroll.get_temp_dir", lambda: temp_dir):
            data_file = os.path.join(temp_dir, "test.db")

            shutil.copy2(
                os.path.join(
                    os.path.dirname(__file__), "..", "data", "py2_persistent.db"
                ),
                data_file,
            )

            data = load_persistent_db(data_file)

            assert dict(data) == {
                "python2": slackroll_state_installed,
                "python3": slackroll_state_installed,
            }

            data.close()  # type: ignore


def test_round_trip_serialisation(temp_dir):
    # type: (str) -> None
    """Checks if we can round trip serialise then deserialise a value."""

    with patch("slackroll.get_temp_dir", lambda: temp_dir):
        data_file = os.path.join(temp_dir, "test.db")

        data = load_persistent_db(data_file)

        data["package1"] = slackroll_state_installed
        data["package2"] = slackroll_state_installed

        data.close()  # type: ignore

        data = load_persistent_db(data_file)

        assert dict(data) == {
            "package1": slackroll_state_installed,
            "package2": slackroll_state_installed,
        }

        data.close()  # type: ignore
