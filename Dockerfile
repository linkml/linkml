# set base image (host OS)
FROM python:3.9

# https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.13

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# set the working directory in the container
WORKDIR /work

RUN pip install linkml

# command to run on container start
CMD [ "bash" ]
