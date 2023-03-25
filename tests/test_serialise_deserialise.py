import os
from tempfile import NamedTemporaryFile

import pytest

from slackroll import try_dump, try_load


@pytest.fixture
def blacklist():
    return [
        "^\\.\\/(?!chromium|libreoffice|vlc).*$@\\/sbrepos\\/",
        "^\\./testing.*",
        "glibc-(?!zoneinfo)@^(?!http)",
    ]


def test_deserialise(blacklist):
    """Checks if we can deserialise a known good file."""

    data_file = os.path.join(os.path.dirname(__file__), "..", "data", "blacklist.db")

    assert blacklist == try_load(data_file)


def test_round_trip_serialisation(blacklist):
    """Checks if we can round trip serialise then deserialise a value."""

    f = NamedTemporaryFile(delete=True)

    try_dump(blacklist, f.name)

    assert blacklist == try_load(f.name)

    f.close()
