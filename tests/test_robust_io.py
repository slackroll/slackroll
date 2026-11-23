import os
import sys

import pytest
from slackroll import (
    SlackrollError,
    SlackrollOutputInterceptor,
    download_file,
    try_dump,
    try_load,
)

import tests

if tests.PY2:
    import cPickle as pickle
    import httplib as http_client
else:
    import http.client as http_client
    import pickle


def test_try_load_truncated_file_exits_cleanly(temp_dir):
    # type: (str) -> None
    path = os.path.join(temp_dir, "truncated.db")
    handle = open(path, "wb")
    handle.write(tests.bytes_literal("(dp0\nS'pkg'\np1\n"))  # cut off before the value
    handle.close()

    pytest.raises(SystemExit, try_load, path)


class _Unpicklable(object):
    def __reduce__(self):
        # type: () -> str
        raise pickle.PicklingError("refusing to pickle")


def test_try_dump_failure_keeps_previous_file(temp_dir):
    # type: (str) -> None
    path = os.path.join(temp_dir, "data.db")
    try_dump({"pkg": 2}, path)

    pytest.raises(SystemExit, try_dump, {"pkg": _Unpicklable()}, path)

    assert try_load(path) == {"pkg": 2}
    assert os.listdir(temp_dir) == ["data.db"]


def test_download_file_wraps_http_exception(temp_dir, request):
    # type: (str, pytest.FixtureRequest) -> None
    def fail(*args):
        # type: (*object) -> None
        raise http_client.HTTPException("connection went away")

    tests.start_patch(request, "slackroll.urlretrieve", fail)
    tests.start_patch(request, "slackroll.print_flush", lambda message: None)

    pytest.raises(
        SlackrollError,
        download_file,
        "http://mirror.example/",
        "FILELIST.TXT",
        os.path.join(temp_dir, "tmp"),
        os.path.join(temp_dir, "final"),
    )


def test_output_interceptor_restores_stdout_when_block_raises(request):
    # type: (pytest.FixtureRequest) -> None
    fake_stdout = tests.Mock()
    fake_stdout.isatty.return_value = True
    tests.start_patch(request, "slackroll.sys.stdout", fake_stdout)
    tests.start_patch(request, "slackroll.write_raw_output", lambda output: None)

    try:
        interceptor = SlackrollOutputInterceptor()
        try:
            raise ValueError("boom")
        finally:
            interceptor.stop()
    except ValueError:
        pass

    assert sys.stdout is fake_stdout
