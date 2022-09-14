# cmem-plugin-template

This repository contains a [copier](https://copier.readthedocs.io/) template, which can be used to bootstrap an eccenca Corporate Memory python plugin.

## Features

- [python / poetry](https://python-poetry.org/) project with [pylint](https://pylint.pycqa.org/), [pytest](https://www.pytest.org/), [flake8](https://flake8.pycqa.org/), [mypy](http://mypy-lang.org/), [bandit](https://bandit.readthedocs.io/) and [safety](https://pyup.io/safety/) integration
- local build plan with [task](https://taskfile.dev/)
- [github build plan](https://github.com/eccenca/cmem-plugin-template/tree/main/src/.github/workflows)
- [gitlab build plan](https://github.com/eccenca/cmem-plugin-template/blob/main/src/.gitlab-ci.yml)
- badges, junit XML files and coverage stat generation

## Setup and Usage

### Project Initialization

The following command will create a new project directory:
```
$ copier gh:eccenca/cmem-plugin-template cmem-plugin-my
```

After that, you can initialize the repository and install git hooks:
```
$ cd cmem-plugin-my
$ git init
$ git add .
$ git commit -m "init"
$ pre-commit install
```

Then you can run the local test suite an build a first deployment artifact:
```
$ task check build
```

### Project Update

From time to time, this template will be upgraded, so you can update your repository as well:
```
$ copier update
```

Please have a look at the [copier documentation](https://copier.readthedocs.io/en/stable/updating/).

### Other Tasks

Available tasks for your project can be listed like this:
```
$ task
task: Available tasks for this project:
* build:          Build tarball and a wheel package.
* check:          Run whole test suite.
* check:bandit:   Check source code with bandit.
* check:flake8:   Check source code with flake8.
* check:mypy:     Check source code with mypy.
* check:pylint:   Check source code with pylint.
* check:pytest:   Run pytest suite.
* check:safety:   Check source code with safety.
* clean:          Removes dist, *.pyc and some caches
* deploy: 		  Install plugin package in Corporate Memory
* poetry:init:    Initialze poetry env and add dev dependencies used in this taskfile.
* poetry:install: Install dependencies managed by Poetry.
* poetry:shell:   Open a poetry shell.
* poetry:update:  Update dependencies managed by Poetry to their newest versions.
* python:format:  Format Python files.
```

You can extend this by creating a custom tasks file in your repository root:

```
$ cat TaskfileCustom.yaml
---
version: '3'

tasks:

  ttt:
    desc: just a test
    cmds:
      - task --list
```


### Setup Integration Tests

This template uses pytest for testing. Testing your plugin is crucial and should be done locally and integrated with eccenca Corporate Memory.

In order to provide access to a Corporate Memory deployment, you need to provide correct environment variables.
Without these variables, only tests without integration can be executed (see `1 skipped`):

```
$ task check:pytest
...
... ===== 3 passed, 1 skipped in 0.09s =====
```

By giving the correct [cmemc](https://eccenca.com/go/cmemc) [environment variables](https://documentation.eccenca.com/latest/automate/cmemc-command-line-interface/installation-and-configuration/file-based-configuration#id-.FilebasedConfigurationv22.1-Reference), your plugin can be tested in an integrated way:

```
$ export CMEM_BASE_URI="https://cmem.example.org"
$ export OAUTH_CLIENT_ID="cmem-service-account"
$ export OAUTH_CLIENT_SECRET="..."
$ export OAUTH_GRANT_TYPE="client_credentials"
$ task check:pytest
...
... ===== 4 passed in 1.71s =====

```

### Setup Build Plan

The gitlab workflow / github action pipelines need the same environment variables as secrets:

- For github, go to Settings > Secret > Actions > [New Repository Secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- For gitlab, go to Settings > CI/CD > Variables (Expand) > [Add Variable (protected, masked, all environments)](https://docs.gitlab.com/ee/ci/variables/)

Example github pipelines can be seen [here](https://github.com/eccenca/cmem-plugin-kafka/actions) and [here](https://github.com/eccenca/cmem-plugin-graphql/actions).

In addition to the eccenca Corporate Memory credential secrets, a `PYPI_TOKEN` secret can be set in order to use the `publish` task/workflow.

### Install Local Requirements

The following tools are needed for local task execution:

- Python 3.9
- [copier](https://copier.readthedocs.io/) (>= v6) for project template rendering
- [poetry](https://python-poetry.org/) (>= v1.1) for packaging and dependency managing (+ [dynamic versioning plugin](https://github.com/mtkennerly/poetry-dynamic-versioning))
- [pre-commit](https://pre-commit.com/) (>= v2.20) - managing and maintaining pre-commit hooks
- [task](https://taskfile.dev/) (>= v3) for build task running (make sure to follow the installation instructions to avoid confusion with taskwarrior)
- [cmemc](https://eccenca.com/go/cmemc) (>= v22.1) for interacting with eccenca Corporate Memory

Example installation of the requirements with [pipx](https://pypa.github.io/pipx/) on Ubuntu:

```
$ sudo sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin
$ python3 -m pip install --user pipx
$ python3 -m pipx ensurepath
$ pipx install copier
$ pipx install poetry
$ poetry self add "poetry-dynamic-versioning[plugin]"
$ pipx install pre-commit
$ pipx install cmem-cmemc
```

