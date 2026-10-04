# syntax=docker/dockerfile:1.27.1@sha256:4edf897a3ffa55b89f906fc8cc78afdb3f1834cc9c7083565e611a8a7d5fe99e
# check=error=true

FROM aclemons/slackware:current@sha256:137bf08bcfd70a2706c5637407ba669f8ce5d016b8207de516b3a68510a52485 AS base

# install python2
RUN export TERSE=0 && \
    sed -i '/^WGETFLAGS/s/"$/ -q"/' /etc/slackpkg/slackpkg.conf && \
    slackpkg -default_answer=yes -batch=on update && \
    EXIT_CODE=0 && { slackpkg -default_answer=yes -batch=on upgrade-all || EXIT_CODE=$? ; } && \
    if [ "$EXIT_CODE" -ne 0 ] && [ "$EXIT_CODE" -ne 20 ] ; then exit "$EXIT_CODE" ; fi && \
    EXIT_CODE=0 && { slackpkg -default_answer=yes -batch=on install aaa_libraries brotli bzip2 db48 e2fsprogs expat gcc-11 gcc-g++-11 gdbm glib2 icu4c keyutils krb5-1 libedit libffi libnsl libpng libtirpc ncurses openssl openssl-solibs pcre python2 readline sqlite xz zlib || EXIT_CODE=$? ; } && \
    if [ "$EXIT_CODE" -ne 0 ] && [ "$EXIT_CODE" -ne 20 ] ; then exit "$EXIT_CODE" ; fi && \
    EXIT_CODE=0 && { slackpkg -default_answer=yes -batch=on install ca-certificates dcron perl || EXIT_CODE=$? ; } && \
    if [ "$EXIT_CODE" -ne 0 ] && [ "$EXIT_CODE" -ne 20 ] ; then exit "$EXIT_CODE" ; fi && \
    c_rehash && update-ca-certificates && \
    rm -rf /var/cache/packages/* && rm -rf /var/lib/slackpkg/*

# setup running tests
RUN pip2 --no-cache-dir install mock==3.0.5 pytest==4.6.11 pytest_cov==2.12.1 && rm -rf /root/.cache
