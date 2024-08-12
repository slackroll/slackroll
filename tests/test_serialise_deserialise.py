import os
from tempfile import NamedTemporaryFile

import pytest
from slackroll import try_dump, try_load

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import List


@pytest.fixture  # type: ignore
def blacklist():
    # type: () -> List[str]
    return [
        "^\\.\\/(?!chromium|libreoffice|vlc).*$@\\/sbrepos\\/",
        "^\\./testing.*",
        "glibc-(?!zoneinfo)@^(?!http)",
    ]


def test_deserialise(blacklist):
    # type: (List[str]) -> None
    """Checks if we can deserialise a known good file."""

    data_file = os.path.join(os.path.dirname(__file__), "..", "data", "blacklist.db")

    assert blacklist == try_load(data_file)


def test_round_trip_serialisation(blacklist):
    # type: (List[str]) -> None
    """Checks if we can round trip serialise then deserialise a value."""

    f = NamedTemporaryFile(delete=True)

    try_dump(blacklist, f.name)

    assert blacklist == try_load(f.name)

    f.close()
