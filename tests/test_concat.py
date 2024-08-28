from slackroll import concat


def test_concat():
    # type: () -> None

    assert concat([["a", "b"], ["c", "d"]]) == ["a", "b", "c", "d"]
