import os
import sys
import toml

slackroll_file = os.path.join(os.path.dirname(__file__), "..", "slackroll")

if sys.version_info[0] <= 2:
    import imp
    slackroll = imp.load_source('slackroll', slackroll_file)
else:
    from importlib.util import spec_from_loader, module_from_spec
    from importlib.machinery import SourceFileLoader

    spec = spec_from_loader("slackroll", SourceFileLoader("slackroll", slackroll_file))
    slackroll = module_from_spec(spec)
    spec.loader.exec_module(slackroll)


from slackroll import slackroll_version

def test_versions_match():
    """Checks if the version in pyproject.toml and slackroll_version in `slackroll` match."""

    pyproject_file = os.path.join(os.path.dirname(__file__), "..", "pyproject.toml")
    pyproject_version = toml.loads(open(str(pyproject_file)).read())["tool"]["poetry"][
        "version"
    ]

    assert int(pyproject_version) == slackroll_version
