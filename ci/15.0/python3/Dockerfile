# syntax=docker/dockerfile:1.28.0@sha256:bb22d9815c728170f72750f4e5b0d672e06176142e1d602c7e66c050100b7e5b
# check=error=true

FROM aclemons/slackware:15.0@sha256:f3744d806955e2616e9239a5e7c6ae39bbffddb8bc3a9cd3e5f37a5ac8ac1775 AS base

# install python3
RUN export TERSE=0 && \
    sed -i '/^WGETFLAGS/s/"$/ -q"/' /etc/slackpkg/slackpkg.conf && \
    slackpkg -default_answer=yes -batch=on update && \
    EXIT_CODE=0 && { slackpkg -default_answer=yes -batch=on upgrade-all || EXIT_CODE=$? ; } && \
    if [ "$EXIT_CODE" -ne 0 ] && [ "$EXIT_CODE" -ne 20 ] ; then exit "$EXIT_CODE" ; fi && \
    EXIT_CODE=0 && { slackpkg -default_answer=yes -batch=on install aaa_libraries brotli bzip2 db48 e2fsprogs expat gcc-11 gcc-g++-11 gdbm glib2 icu4c keyutils krb5-1 libedit libffi libnsl libpng libtirpc ncurses openssl openssl-solibs pcre python-pip python3 readline sqlite util-linux xz zlib || EXIT_CODE=$? ; } && \
    if [ "$EXIT_CODE" -ne 0 ] && [ "$EXIT_CODE" -ne 20 ] ; then exit "$EXIT_CODE" ; fi && \
    EXIT_CODE=0 && { slackpkg -default_answer=yes -batch=on install ca-certificates dcron perl || EXIT_CODE=$? ; } && \
    if [ "$EXIT_CODE" -ne 0 ] && [ "$EXIT_CODE" -ne 20 ] ; then exit "$EXIT_CODE" ; fi && \
    c_rehash && update-ca-certificates && \
    rm -rf /var/cache/packages/* && rm -rf /var/lib/slackpkg/*

# setup running tests
RUN pip3 --no-cache-dir install "pytest==8.4.2" "pytest_cov==7.1.0" "toml==0.10.2" && rm -rf /root/.cache
