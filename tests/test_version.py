import os

try:
    import tomllib
except ImportError:
    import toml as tomllib  # type: ignore

from slackroll import slackroll_version


def test_versions_match():
    # type: () -> None
    """Checks if the version in pyproject.toml and slackroll_version in `slackroll` match."""

    pyproject_file = os.path.join(os.path.dirname(__file__), "..", "pyproject.toml")
    pyproject_version = tomllib.loads(open(str(pyproject_file)).read())["project"][
        "version"
    ]

    assert int(pyproject_version) == slackroll_version
