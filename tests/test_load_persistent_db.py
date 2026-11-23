import os
import shutil

import pytest
from slackroll import load_persistent_db, slackroll_state_installed

import tests

if tests.PY2:

    def test_switch_format(temp_dir, request):
        # type: (str, pytest.FixtureRequest) -> None
        """Checks if we can open a known good file."""

        tests.start_patch(request, "slackroll.get_temp_dir", lambda: temp_dir)
        data_file = os.path.join(temp_dir, "test.db")

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


def test_round_trip_serialisation(temp_dir, request):
    # type: (str, pytest.FixtureRequest) -> None
    """Checks if we can round trip serialise then deserialise a value."""

    tests.start_patch(request, "slackroll.get_temp_dir", lambda: temp_dir)
    data_file = os.path.join(temp_dir, "test.db")

    data = load_persistent_db(data_file)

    data["package1"] = slackroll_state_installed
    data["package2"] = slackroll_state_installed

    data.close()

    data = load_persistent_db(data_file)

    assert dict(data) == {
        "package1": slackroll_state_installed,
        "package2": slackroll_state_installed,
    }

    if tests.PY2:
        assert "package1".decode("latin-1") in data
        assert data["package1".decode("latin-1")] == slackroll_state_installed

    data.close()


def test_persistent_db_is_a_single_file(temp_dir, request):
    # type: (str, pytest.FixtureRequest) -> None
    """The database must be one persistent.db file, not the dbm.dumb .dat/.dir/.bak set."""

    tests.start_patch(request, "slackroll.get_temp_dir", lambda: temp_dir)
    data_file = os.path.join(temp_dir, "persistent.db")

    data = load_persistent_db(data_file)
    data["package1"] = slackroll_state_installed
    data.close()

    assert os.listdir(temp_dir) == ["persistent.db"]


if not tests.PY2:

    def test_persistent_db_requires_gdbm(temp_dir, request):
        # type: (str, pytest.FixtureRequest) -> None
        """Without gdbm, fail with a clear error instead of silently using another dbm."""

        tests.start_patch(request, "slackroll.get_temp_dir", lambda: temp_dir)
        tests.start_patch(request, "slackroll.gdbm_module", None)

        pytest.raises(
            SystemExit,
            load_persistent_db,
            os.path.join(temp_dir, "persistent.db"),
        )
