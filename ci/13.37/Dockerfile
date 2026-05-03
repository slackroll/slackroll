# syntax=docker/dockerfile:1.23.0@sha256:2780b5c3bab67f1f76c781860de469442999ed1a0d7992a5efdf2cffc0e3d769

FROM aclemons/slackware:13.37@sha256:46bf582fc4683f88bf4468c05b9f58158e1eec1d5eb42cf759bf14afd1880adf AS base

# install python2
RUN export TERSE=0 && \
    sed -i '/^WGETFLAGS/s/"$/ -q"/' /etc/slackpkg/slackpkg.conf && \
    slackpkg -default_answer=yes -batch=on update && \
    EXIT_CODE=0 && { slackpkg -default_answer=yes -batch=on upgrade-all || EXIT_CODE=$? ; } && \
    if [ "$EXIT_CODE" -ne 0 ] && [ "$EXIT_CODE" -ne 20 ] ; then exit "$EXIT_CODE" ; fi && \
    EXIT_CODE=0 && { slackpkg -default_answer=yes -batch=on install aaa_elflibs bzip2 db44 expat gdbm openssl openssl-solibs python-2 readline setuptools sqlite zlib || EXIT_CODE=$? ; } && \
    if [ "$EXIT_CODE" -ne 0 ] && [ "$EXIT_CODE" -ne 20 ] ; then exit "$EXIT_CODE" ; fi && \
    EXIT_CODE=0 && { slackpkg -default_answer=yes -batch=on install ca-certificates dcron perl || EXIT_CODE=$? ; } && \
    if [ "$EXIT_CODE" -ne 0 ] && [ "$EXIT_CODE" -ne 20 ] ; then exit "$EXIT_CODE" ; fi && \
    c_rehash && update-ca-certificates && \
    rm -rf /var/cache/packages/* && rm -rf /var/lib/slackpkg/*


# use modern host to download, since we cannot use https to talk to these hosts on 13.37
FROM alpine:3.23.3@sha256:25109184c71bdad752c8312a8623239686a9a2071e8825f20acb8f2198c3f659 AS downloader

WORKDIR /tmp

SHELL ["/bin/ash", "-o", "pipefail", "-c"]
RUN wget -q https://slackbuilds.org/slackbuilds/13.37/python/pysetuptools.tar.gz && \
    echo "fc6f1c55fc000411832c813de5804d3f  pysetuptools.tar.gz" | md5sum -c && \
    wget -q https://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz && \
    echo "7df2a529a074f613b509fb44feefe74e  setuptools-0.6c11.tar.gz" | md5sum -c && \
    tar -xf pysetuptools.tar.gz && rm pysetuptools.tar.gz && mv setuptools-0.6c11.tar.gz pysetuptools && \
    wget -q https://slackbuilds.org/slackbuilds/13.37/python/mock.tar.gz && \
    echo "8966f86d83ad8e26a11cd6eb9bf745ad  mock.tar.gz" | md5sum -c && \
    wget -q https://pypi.python.org/packages/source/m/mock/mock-0.8.0.tar.gz && \
    echo "b1ac87a1ceab295aef11dcfc104a7a4a  mock-0.8.0.tar.gz" | md5sum -c && \
    tar -xf mock.tar.gz && rm mock.tar.gz && mv mock-0.8.0.tar.gz mock && \
    wget -q https://slackbuilds.org/slackbuilds/14.1/python/pytest.tar.gz && \
    echo "566fc2f987a050c21096fbc7bc1977c7  pytest.tar.gz" | md5sum -c && \
    wget -q https://pypi.python.org/packages/source/p/pytest/pytest-2.8.7.tar.gz && \
    echo "685e2137062c9821b1b74a4814795514  pytest-2.8.7.tar.gz" | md5sum -c && \
    tar -xf pytest.tar.gz && rm pytest.tar.gz && mv pytest-2.8.7.tar.gz pytest && \
    sed -i -e '/^unzip /s/\.zip/.tar.gz/' -e '/^unzip /s/unzip/tar -xf/' pytest/pytest.SlackBuild && \
    wget -q https://slackbuilds.org/slackbuilds/14.1/python/py.tar.gz && \
    echo "db569d63d3133166e06e67a412d00c2e  py.tar.gz" | md5sum -c && \
    wget -q https://pypi.python.org/packages/source/p/py/py-1.4.34.tar.gz && \
    echo "d9c3d8f734b0819ff48e355d77bf1730  py-1.4.34.tar.gz" | md5sum -c && \
    tar -xf py.tar.gz && rm py.tar.gz && mv py-1.4.34.tar.gz py && \
    sed -i -e 's/README\.txt/README.rst/' py/py.SlackBuild && \
    wget -q https://slackbuilds.org/slackbuilds/13.37/libraries/argparse.tar.gz && \
    echo "841e347d054d653fbbe40d14265b7e8c  argparse.tar.gz" | md5sum -c && \
    wget -q https://files.pythonhosted.org/packages/6f/ad/86448942ad49c5fe05bfdf7ebc874807f521dfcca5ee543afaca2974ad5a/argparse-1.2.1.tar.gz && \
    echo "2fbef8cb61e506c706957ab6e135840c  argparse-1.2.1.tar.gz" | md5sum -c && \
    tar -xf argparse.tar.gz && rm argparse.tar.gz && mv argparse-1.2.1.tar.gz argparse && \
    wget -q https://slackbuilds.org/slackbuilds/14.2/python/python-toml.tar.gz && \
    echo "217438eb0e0afb4f9b9712a9ea20623a  python-toml.tar.gz" | md5sum -c && \
    wget -q https://files.pythonhosted.org/packages/be/ba/1f744cdc819428fc6b5084ec34d9b30660f6f9daaf70eead706e3203ec3c/toml-0.10.2.tar.gz && \
    echo "59bce5d8d67e858735ec3f399ec90253  toml-0.10.2.tar.gz" | md5sum -c && \
    tar -xf python-toml.tar.gz && rm python-toml.tar.gz && mv toml-0.10.2.tar.gz python-toml


FROM base AS deps

# hadolint ignore=DL3003
RUN --mount=from=downloader,source=/tmp,target=/builder \
    cd /builder/mock && \
    bash mock.SlackBuild && \
    rm -rf /tmp/SBo && \
    cd /builder/pysetuptools && \
    bash pysetuptools.SlackBuild && \
    rm -rf /tmp/SBo && \
    installpkg /tmp/*tgz && \
    cd /builder/argparse && \
    bash argparse.SlackBuild && \
    rm -rf /tmp/SBo && \
    cd /builder/py && \
    VERSION=1.4.34 bash py.SlackBuild && \
    rm -rf /tmp/SBo && \
    cd /builder/pytest && \
    VERSION=2.8.7 bash pytest.SlackBuild && \
    rm -rf /tmp/SBo && \
    cd /builder/python-toml && \
    bash python-toml.SlackBuild && \
    rm -rf /tmp/SBo


FROM base

# install pytest
RUN --mount=from=deps,source=/tmp,target=/pkgs \
    TERSE=0 installpkg /pkgs/*tgz
