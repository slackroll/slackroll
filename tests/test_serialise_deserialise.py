import os
import sys
import tempfile
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


from slackroll import try_load

def test_deserialise():
    """Checks if we can round deserialise a known good file.."""

    data_file = os.path.join(os.path.dirname(__file__), "..", "data", "blacklist.db")
    expected_data = ['^\\.\\/(?!chromium|libreoffice|vlc).*$@\\/sbrepos\\/', '^\\./testing.*', 'glibc-(?!zoneinfo)@^(?!http)']

    assert expected_data == try_load(data_file)
