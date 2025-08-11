FROM python:3.12-bookworm AS builder

# https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  UV_VERSION=0.7.13

# Install uv
RUN pip install "uv==$UV_VERSION"


WORKDIR /code

# Build project. The .git directory is needed for uv-dynamic-versioning
COPY . .
RUN uv build

#######################################
FROM python:3.12-slim-bookworm AS runner

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
