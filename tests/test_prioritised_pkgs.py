import os
import toml

from slackroll import transient_cmp


def test_transient_cmp_normal_pkg_same_state():
    left = ("python2", "slackroll_state_outdated")
    right = ("python3", "slackroll_state_outdated")

    assert transient_cmp(left, right) == -1
    assert transient_cmp(right, left) == 1
    assert transient_cmp(left, left) == 0


def test_transient_cmp_normal_pkg_different_state():
    left = ("python2", "slackroll_state_new")
    right = ("python3", "slackroll_state_outdated")

    assert transient_cmp(left, right) == 0
    assert transient_cmp(right, left) == 0
    assert transient_cmp(left, left) == 0


def test_transient_cmp_prioritised_pkg_aaa_glib_solibs():
    left = ("aaa_glibc-solibs", "slackroll_state_new")
    right = ("python3", "slackroll_state_outdated")

    assert transient_cmp(left, right) == -1
    assert transient_cmp(right, left) == 1
    assert transient_cmp(left, left) == 0


def test_transient_cmp_prioritised_pkg_glibc_solibs():
    left = ("glibc-solibs", "slackroll_state_new")
    right = ("python3", "slackroll_state_outdated")

    assert transient_cmp(left, right) == -1
    assert transient_cmp(right, left) == 1
    assert transient_cmp(left, left) == 0


def test_transient_cmp_prioritised_pkg_sed():
    left = ("sed", "slackroll_state_new")
    right = ("python3", "slackroll_state_outdated")

    assert transient_cmp(left, right) == -1
    assert transient_cmp(right, left) == 1
    assert transient_cmp(left, left) == 0

def test_transient_cmp_prioritised_pkg_pkgtools():
    left = ("pkgtools", "slackroll_state_new")
    right = ("python3", "slackroll_state_outdated")

    assert transient_cmp(left, right) == -1
    assert transient_cmp(right, left) == 1
    assert transient_cmp(left, left) == 0
