import os

import toml

from slackroll import transient_key, slackroll_state_new, slackroll_state_outdated


def test_transient_cmp_normal_pkg_same_state():
    left = ("python2", slackroll_state_outdated)
    right = ("python3", slackroll_state_outdated)

    assert transient_key(left) < transient_key(right)
    assert transient_key(left) == transient_key(left)


def test_transient_cmp_normal_pkg_different_state():
    left = ("python3", slackroll_state_new)
    right = ("python2", slackroll_state_outdated)

    # BCS: changed test to verify state sorting takes precedence over package name
    assert transient_key(left) < transient_key(right)
    assert transient_key(left) == transient_key(left)


def test_transient_cmp_prioritised_pkg_aaa_glib_solibs():
    left = ("aaa_glibc-solibs", slackroll_state_new)
    right = ("python3", slackroll_state_outdated)

    assert transient_key(left) < transient_key(right)
    assert transient_key(left) == transient_key(left)


def test_transient_cmp_prioritised_pkg_glibc_solibs():
    left = ("glibc-solibs", slackroll_state_new)
    right = ("python3", slackroll_state_outdated)

    assert transient_key(left) < transient_key(right)
    assert transient_key(left) == transient_key(left)


def test_transient_cmp_prioritised_pkg_sed():
    left = ("sed", slackroll_state_new)
    right = ("python3", slackroll_state_outdated)

    assert transient_key(left) < transient_key(right)
    assert transient_key(left) == transient_key(left)


def test_transient_cmp_prioritised_pkg_pkgtools():
    left = ("pkgtools", slackroll_state_new)
    right = ("python3", slackroll_state_outdated)

    assert transient_key(left) < transient_key(right)
    assert transient_key(left) == transient_key(left)
