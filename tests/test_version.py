import os
import re

from slackroll import slackroll_version


def test_versions_match():
    # type: () -> None
    """Checks if the version in pyproject.toml and slackroll_version in `slackroll` match."""

    pyproject_file = os.path.join(os.path.dirname(__file__), "..", "pyproject.toml")
    contents = open(str(pyproject_file)).read()

    # No TOML parser: the toml releases available for old pythons can't handle project authors
    project = re.search(r"^\[project\]\s*$(.*?)(?=^\[)", contents, re.M | re.S)
    assert project is not None
    version = re.search(r'^version\s*=\s*"(\d+)"', project.group(1), re.M)
    assert version is not None

    assert int(version.group(1)) == slackroll_version
