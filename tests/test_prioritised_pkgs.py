from slackroll import transient_key


def test_transient_cmp_normal_pkg_same_state():
    # type: () -> None
    left = ("python2", 6)
    right = ("python3", 6)

    assert transient_key(left) < transient_key(right)
    assert transient_key(left) == transient_key(left)


def test_transient_cmp_normal_pkg_different_state():
    # type: () -> None
    left = ("python2", 0)
    right = ("python3", 6)

    assert transient_key(left) < transient_key(right)
    assert transient_key(left) == transient_key(left)


def test_transient_cmp_prioritised_pkg_aaa_glib_solibs():
    # type: () -> None
    left = ("aaa_glibc-solibs", 0)
    right = ("python3", 6)

    assert transient_key(left) < transient_key(right)
    assert transient_key(left) == transient_key(left)


def test_transient_cmp_prioritised_pkg_glibc_solibs():
    # type: () -> None
    left = ("glibc-solibs", 0)
    right = ("python3", 6)

    assert transient_key(left) < transient_key(right)
    assert transient_key(left) == transient_key(left)


def test_transient_cmp_prioritised_pkg_sed():
    # type: () -> None
    left = ("sed", 0)
    right = ("python3", 6)

    assert transient_key(left) < transient_key(right)
    assert transient_key(left) == transient_key(left)


def test_transient_cmp_prioritised_pkg_pkgtools():
    # type: () -> None
    left = ("pkgtools", 0)
    right = ("python3", 6)

    assert transient_key(left) < transient_key(right)
    assert transient_key(left) == transient_key(left)
