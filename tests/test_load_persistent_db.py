import os
import shutil
from tempfile import NamedTemporaryFile, mkdtemp

import pytest

import tests
from slackroll import load_persistent_db, slackroll_state_installed


@pytest.fixture
def temp_dir():
    dir = mkdtemp()

    yield dir

    shutil.rmtree(dir)


if tests.PY2:

    def test_switch_format(temp_dir):
        """Checks if we can open a known good file."""

        data_file = os.path.join(temp_dir, "persistence.db")

        shutil.copy2(
            os.path.join(os.path.dirname(__file__), "..", "data", "py2_persistent.db"),
            data_file,
        )

        data = load_persistent_db(data_file)

        assert dict(data) == {
            "python2": slackroll_state_installed,
            "python3": slackroll_state_installed,
        }

        data.close()


def test_round_trip_serialisation(temp_dir):
    """Checks if we can round trip serialise then deserialise a value."""

    data_file = os.path.join(temp_dir, "persistence.db")

    data = load_persistent_db(data_file)

    data["package1"] = slackroll_state_installed
    data["package2"] = slackroll_state_installed

    data.close()

    data = load_persistent_db(data_file)

    assert dict(data) == {
        "package1": slackroll_state_installed,
        "package2": slackroll_state_installed,
    }

    data.close()
