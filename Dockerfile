FROM python:3.12-bookworm as builder

# https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.6.0

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry self add "poetry-dynamic-versioning[plugin]"

WORKDIR /code

# Build project. The .git directory is needed for poetry-dynamic-versioning
COPY . .
RUN poetry build

#######################################
FROM python:3.12-slim-bookworm as runner

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt update && apt install -y gcc musl-dev python3-dev && rm -rf /var/lib/apt/lists/*

COPY --from=builder /code/dist/*.whl /tmp/linkml-whl/
RUN pip install /tmp/linkml-whl/*.whl

RUN useradd --create-home linkmluser
WORKDIR /home/linkmluser
USER linkmluser

# command to run on container start
CMD [ "bash" ]
