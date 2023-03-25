import os

import tests

slackroll_file = os.path.join(os.path.dirname(__file__), "..", "slackroll")

if tests.PY2:
    import imp

    imp.load_source("slackroll", slackroll_file)
else:
    import imp

    imp.load_source("slackroll", slackroll_file)
