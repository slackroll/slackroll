# syntax=docker/dockerfile:1.22.0@sha256:4a43a54dd1fedceb30ba47e76cfcf2b47304f4161c0caeac2db1c61804ea3c91

FROM aclemons/slackware:12.0@sha256:9fa0f283a885f0353cdb6cb0c61b9aa611abe6dc516754ddb6ad7a86692912e7 AS base

# install python2
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN export TERSE=0 && \
    sed -i '/^WGETFLAGS/s/"$/ -q"/' /etc/slackpkg/slackpkg.conf && \
    EXIT_CODE=0 && { yes | slackpkg update || EXIT_CODE=$? ; } && \
    if [ "$EXIT_CODE" -ne 0 ] && [ "$EXIT_CODE" -ne 141 ] ; then exit "$EXIT_CODE" ; fi && \
    EXIT_CODE=0 && { yes | slackpkg upgrade-all || EXIT_CODE=$? ; } && \
    if [ "$EXIT_CODE" -ne 0 ] && [ "$EXIT_CODE" -ne 20 ] && [ "$EXIT_CODE" -ne 141 ] ; then exit "$EXIT_CODE" ; fi && \
    EXIT_CODE=0 && { yes | slackpkg install aaa_elflibs bzip2 db44 expat gdbm openssl readline python zlib || EXIT_CODE=$? ; } && \
    if [ "$EXIT_CODE" -ne 0 ] && [ "$EXIT_CODE" -ne 20 ] && [ "$EXIT_CODE" -ne 141 ] ; then exit "$EXIT_CODE" ; fi && \
    EXIT_CODE=0 && { yes | slackpkg install dcron perl || EXIT_CODE=$? ; } && \
    if [ "$EXIT_CODE" -ne 0 ] && [ "$EXIT_CODE" -ne 20 ] && [ "$EXIT_CODE" -ne 141 ] ; then exit "$EXIT_CODE" ; fi && \
    rm -rf /var/cache/packages/* && rm -rf /var/lib/slackpkg/*


# use modern host to download, since we cannot use https to talk to pypi on 12.0
FROM alpine:3.23.3@sha256:25109184c71bdad752c8312a8623239686a9a2071e8825f20acb8f2198c3f659 AS downloader

WORKDIR /tmp

SHELL ["/bin/ash", "-o", "pipefail", "-c"]
RUN wget -q https://files.pythonhosted.org/packages/8b/62/baf1e2c2b02de7898dcacd1d1a41e323b79d25be5c88d2805c89fb424835/setuptools-0.6c11.tar.gz && \
    echo "7df2a529a074f613b509fb44feefe74e  setuptools-0.6c11.tar.gz" | md5sum -c && \
    tar -xf setuptools-0.6c11.tar.gz && rm setuptools-0.6c11.tar.gz && \
    wget -q https://files.pythonhosted.org/packages/52/22/05f0fb67c51e86b485914b1da519b2df6afd36c41f81a21328bc69a2e3b1/mock-0.8.0.tar.gz && \
    echo "b1ac87a1ceab295aef11dcfc104a7a4a  mock-0.8.0.tar.gz" | md5sum -c && \
    tar -xf mock-0.8.0.tar.gz && rm mock-0.8.0.tar.gz && \
    wget -q https://files.pythonhosted.org/packages/6f/ad/86448942ad49c5fe05bfdf7ebc874807f521dfcca5ee543afaca2974ad5a/argparse-1.2.1.tar.gz && \
    echo "2fbef8cb61e506c706957ab6e135840c  argparse-1.2.1.tar.gz" | md5sum -c && \
    tar -xf argparse-1.2.1.tar.gz && rm argparse-1.2.1.tar.gz && \
    wget -q https://files.pythonhosted.org/packages/85/10/2da35967cb3280f505d1b8f22f7e2d3c3e00de27dcb097c39a3e26a08da4/py-1.4.17.tar.gz && \
    echo "1dba4de9f1ac9b3e025895a0b6ad5a91  py-1.4.17.tar.gz" | md5sum -c && \
    tar -xf py-1.4.17.tar.gz && rm py-1.4.17.tar.gz && \
    wget -q https://files.pythonhosted.org/packages/a7/6e/2580c06b2c0a3afa1376e731a1cfa32888be03de5c59cf9a0408347de727/pytest-2.3.5.tar.gz && \
    echo "18f150e7be96b5fe3c388b0e817b8087  pytest-2.3.5.tar.gz" | md5sum -c && \
    tar -xf pytest-2.3.5.tar.gz && rm pytest-2.3.5.tar.gz && \
    wget -q https://files.pythonhosted.org/packages/a2/98/a1b3df99dfe03b7a9cf9ccfd8fb53957cb882c5d25110f9852cb119a92d9/toml-0.7.1.tar.gz && \
    echo "730580bcdac17185bd3af35525ada1e7  toml-0.7.1.tar.gz" | md5sum -c && \
    tar -xf toml-0.7.1.tar.gz && rm toml-0.7.1.tar.gz && \
    sed -i '1s/^/from __future__ import with_statement\n/' toml-0.7.1/setup.py toml-0.7.1/toml.py


FROM base

# hadolint ignore=DL3003
RUN --mount=from=downloader,source=/tmp,target=/builder \
    cp -r /builder/setuptools-0.6c11 /builder/mock-0.8.0 /builder/argparse-1.2.1 /builder/py-1.4.17 /builder/pytest-2.3.5 /builder/toml-0.7.1 /tmp/ && \
    cd /tmp/setuptools-0.6c11 && \
    /usr/bin/python setup.py install && \
    cd /tmp/mock-0.8.0 && \
    /usr/bin/python setup.py install && \
    cd /tmp/argparse-1.2.1 && \
    /usr/bin/python setup.py install && \
    cd /tmp/py-1.4.17 && \
    /usr/bin/python setup.py install && \
    cd /tmp/pytest-2.3.5 && \
    /usr/bin/python setup.py install && \
    cd /tmp/toml-0.7.1 && \
    /usr/bin/python setup.py install && \
    rm -rf /tmp/setuptools-0.6c11 /tmp/mock-0.8.0 /tmp/argparse-1.2.1 /tmp/py-1.4.17 /tmp/pytest-2.3.5 /tmp/toml-0.7.1
