from slackroll import slackroll_state_new, slackroll_state_outdated, transient_key


def test_transient_cmp_normal_pkg_same_state():
    # type: () -> None
    left = ("python2", slackroll_state_outdated)
    right = ("python3", slackroll_state_outdated)

    assert transient_key(left) < transient_key(right)
    assert transient_key(left) == transient_key(left)


def test_transient_cmp_normal_pkg_different_state():
    # type: () -> None
    left = ("python3", slackroll_state_new)
    right = ("python2", slackroll_state_outdated)

    # BCS: changed test to verify state sorting takes precedence over package name
    assert transient_key(left) < transient_key(right)
    assert transient_key(left) == transient_key(left)


def test_transient_cmp_prioritised_pkg_aaa_glib_solibs():
    # type: () -> None
    left = ("aaa_glibc-solibs", slackroll_state_new)
    right = ("python3", slackroll_state_outdated)

    assert transient_key(left) < transient_key(right)
    assert transient_key(left) == transient_key(left)


def test_transient_cmp_prioritised_pkg_glibc_solibs():
    # type: () -> None
    left = ("glibc-solibs", slackroll_state_new)
    right = ("python3", slackroll_state_outdated)

    assert transient_key(left) < transient_key(right)
    assert transient_key(left) == transient_key(left)


def test_transient_cmp_prioritised_pkg_sed():
    # type: () -> None
    left = ("sed", slackroll_state_new)
    right = ("python3", slackroll_state_outdated)

    assert transient_key(left) < transient_key(right)
    assert transient_key(left) == transient_key(left)


def test_transient_cmp_prioritised_pkg_pkgtools():
    # type: () -> None
    left = ("pkgtools", slackroll_state_new)
    right = ("python3", slackroll_state_outdated)

    assert transient_key(left) < transient_key(right)
    assert transient_key(left) == transient_key(left)
