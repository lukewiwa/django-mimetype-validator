# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.177.0/containers/python-3/.devcontainer/base.Dockerfile

FROM lukewiwa/pythons:latest

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    libmagic-dev nano openssh-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN ln -sf /usr/local/bin/python3.6 /usr/local/bin/python
RUN ln -sf /usr/local/bin/pip3.6 /usr/local/bin/pip
ENV POETRY_VIRTUALENVS_CREATE="false"
RUN python -m pip install poetry


# Install project deps
COPY poetry.lock pyproject.toml /tmp/pip-tmp/
RUN cd /tmp/pip-tmp && poetry install && rm -rf /tmp/pip-tmp
