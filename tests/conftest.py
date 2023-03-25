import os
import sys

PY2 = sys.version_info[0] <= 2

slackroll_file = os.path.join(os.path.dirname(__file__), "..", "slackroll")

if PY2:
    import imp

    imp.load_source("slackroll", slackroll_file)
else:
    import imp

    imp.load_source("slackroll", slackroll_file)
