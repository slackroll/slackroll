from tempfile import NamedTemporaryFile

from slackroll import get_self_file_version, write_self_file_version

import tests

if tests.PY2:
    from mock import patch  # type: ignore
else:
    from unittest.mock import patch


def test_round_trip_serialisation():
    # type: () -> None
    """Checks if we can round trip write the self file version and then read it again."""

    version = 42

    f = NamedTemporaryFile(delete=True)

    with patch("slackroll.slackroll_version", version):
        with patch("slackroll.slackroll_self_filename", f.name):
            write_self_file_version()

            assert version == get_self_file_version()

    f.close()
