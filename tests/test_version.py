import imp
import os
import toml

slackroll = imp.load_source('slackroll', os.path.join(os.path.dirname(__file__), "..", "slackroll"))

from slackroll import slackroll_version

def test_versions_match():
    """Checks if the version in pyproject.toml and slackroll_version in `slackroll` match."""

    pyproject_file = os.path.join(os.path.dirname(__file__), "..", "pyproject.toml")
    pyproject_version = toml.loads(open(str(pyproject_file)).read())["tool"]["poetry"][
        "version"
    ]

    assert int(pyproject_version) == slackroll_version
