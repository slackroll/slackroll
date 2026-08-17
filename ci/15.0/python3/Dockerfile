# syntax=docker/dockerfile:1.26.0@sha256:ecfaec9ed6d810b56388c508f4121597bfbba70d41a6dfeee4d8cad5f295fc32

FROM aclemons/slackware:15.0@sha256:35ab2753646cc08476f550b3b4a0221de0d34ed23e69f2a6a3152074ebe9243d AS base

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

# renovate: datasource=pypi depName=pytest
ENV PYTEST_VERSION=8.4.2
# renovate: datasource=pypi depName=pytest_cov
ENV PYTEST_COV_VERSION=7.1.0
# renovate: datasource=pypi depName=toml
ENV TOML_VERSION=0.10.2

# setup running tests
RUN pip3 --no-cache-dir install "pytest==$PYTEST_VERSION" "pytest_cov==$PYTEST_COV_VERSION" "toml==$TOML_VERSION" && rm -rf /root/.cache
