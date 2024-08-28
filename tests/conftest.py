import imp
import os

slackroll_file = os.path.join(os.path.dirname(__file__), "..", "slackroll")

imp.load_source("slackroll", slackroll_file)
