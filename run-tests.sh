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

# python 2.7
printf 'Building Slackware -current with Python 2.7...\n'
docker buildx build --platform linux/amd64 --load --progress=none -t slackroll-ci:current-python2 -f ci/current/python2/Dockerfile .

# python 3.12
printf 'Building Slackware -current with Python 3.12...\n'
docker buildx build --platform linux/amd64 --load --progress=none -t slackroll-ci:current-python3 -f ci/current/python3/Dockerfile .

printf '\n'

wheel_dir=$(mktemp -d)
trap 'rm -f "$wheel_dir"/*.whl "$wheel_dir/.gitignore"; rmdir "$wheel_dir"' EXIT
uv build --wheel --out-dir "$wheel_dir"

for python in 2 3; do
  printf 'Testing installed wheel with Python %s...\n' "$python"
  docker run --rm -i -v "$wheel_dir:/wheels:ro" -v "$(pwd)/helpfiles:/expected:ro" -w /tmp \
    "slackroll-ci:current-python$python" sh -es -- "pip$python" <<'EOL'
"$1" install --no-index /wheels/*.whl
PAGER=cat slackroll help > default-help
{ cat /expected/00-default.txt; printf "\n"; } > expected-default
cmp default-help expected-default
PAGER=cat slackroll help update > update-help
{ cat /expected/update.txt; printf "\n"; } > expected-update
cmp update-help expected-update
EOL
done

docker run --rm -it --user "$(id -u):$(id -g)" -v "$(pwd):/data" -w /data slackroll-ci:12.0-python2 py.test
docker run --rm -it --user "$(id -u):$(id -g)" -v "$(pwd):/data" -w /data slackroll-ci:13.37-python2 py.test
docker run --rm -it --user "$(id -u):$(id -g)" -v "$(pwd):/data" -w /data slackroll-ci:15.0-python2 pytest
docker run --rm -it --user "$(id -u):$(id -g)" -v "$(pwd):/data" -w /data slackroll-ci:15.0-python3 pytest

rm -f .coverage .coverage.python2 .coverage.python3

docker run --rm -it --user "$(id -u):$(id -g)" -v "$(pwd):/data" -w /data -e COVERAGE_FILE=.coverage.python2 slackroll-ci:current-python2 sh -c 'pytest --cov=slackroll -vv'
docker run --rm -it --user "$(id -u):$(id -g)" -v "$(pwd):/data" -w /data -e COVERAGE_FILE=.coverage.python3 slackroll-ci:current-python3 sh -c 'pytest --cov=slackroll -vv'

docker run --rm -it --user "$(id -u):$(id -g)" -v "$(pwd):/data" -w /data slackroll-ci:current-python3 sh -c 'coverage combine .coverage.python2 .coverage.python3'
docker run --rm -it --user "$(id -u):$(id -g)" -v "$(pwd):/data" -w /data slackroll-ci:current-python3 sh -c 'coverage html -d htmlcov'
docker run --rm -it --user "$(id -u):$(id -g)" -v "$(pwd):/data" -w /data slackroll-ci:current-python3 sh -c "chown -R $(id -u):$(id -g) /data/htmlcov/"

printf 'Coverage HTML report generated at htmlcov/index.html\n'
