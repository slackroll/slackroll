import os
import sys

slackroll_file = os.path.join(os.path.dirname(__file__), "..", "slackroll")

if sys.version_info[0] <= 2:
    import imp
    imp.load_source('slackroll', slackroll_file)
else:
    from importlib.util import spec_from_loader, module_from_spec
    from importlib.machinery import SourceFileLoader

    spec = spec_from_loader("slackroll", SourceFileLoader("slackroll", slackroll_file))
    module_from_spec(spec)
    spec.loader.exec_module(slackroll)
