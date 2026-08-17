#!/bin/sh

set -e

if ! command -v uv > /dev/null 2>&1 ; then
  >&2 printf "uv is required.\n"
  exit 1
fi

# python 2.5
printf 'Building Slackware 12.0 with Python 2.5...\n'
docker buildx build --platform linux/386 --load --progress=none -t slackroll-ci:12.0-python2 -f ci/12.0/Dockerfile .

# python 2.6
printf 'Building Slackware 13.37 with Python 2.6...\n'
docker buildx build --platform linux/amd64 --load --progress=none -t slackroll-ci:13.37-python2 -f ci/13.37/Dockerfile .

# python 2.7
printf 'Building Slackware 15.0 with Python 2.7...\n'
docker buildx build --platform linux/amd64 --load --progress=none -t slackroll-ci:15.0-python2 -f ci/15.0/python2/Dockerfile .

# python 3.9
printf 'Building Slackware 15.0 with Python 3.9...\n'
docker buildx build --platform linux/amd64 --load --progress=none -t slackroll-ci:15.0-python3 -f ci/15.0/python3/Dockerfile .

printf '\n'

docker run --rm -it --user "$(id -u):$(id -g)" -v "$(pwd):/data" -w /data slackroll-ci:12.0-python2 py.test
docker run --rm -it --user "$(id -u):$(id -g)" -v "$(pwd):/data" -w /data slackroll-ci:13.37-python2 py.test
docker run --rm -it --user "$(id -u):$(id -g)" -v "$(pwd):/data" -w /data slackroll-ci:15.0-python2 pytest
docker run --rm -it --user "$(id -u):$(id -g)" -v "$(pwd):/data" -w /data slackroll-ci:15.0-python3 pytest

# for now, on the host for python3 (-current)
uv run --python-preference only-managed --python 3.12 pytest
