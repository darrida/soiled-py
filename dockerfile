#######################################################################
# INSTALL PYTHON DEPENDENCIES
#######################################################################
# --platform=linux/amd64 
FROM    ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS dependencies

RUN     uv venv

COPY    pyproject.toml pyproject.toml
COPY    uv.lock uv.lock
# If script crashes here, it's probably because you need to comment out "pywin32-308" in requirements.txt
RUN     uv sync --no-install-project

#######################################################################
# BUILD FINAL IMAGE
#######################################################################
FROM    python:3.12-slim-bookworm

COPY    --from=dependencies "/.venv" "/.venv"

ENV     PATH="/.venv/bin:$PATH"
ENV     PYTHONPATH="/.venv/bin:$PATH"

RUN     useradd --create-home nonroot
WORKDIR "/home/nonroot"

# CREATE DIRECTORIES TO SHARE PREFECT TASK DATA AND APP DATA
RUN     mkdir soiled-storage

# APP CODE
COPY    src src
WORKDIR "/home/nonroot/src"
COPY    service_start.sh /home/nonroot/service_start.sh
# COPY    deployment/scripts/start_worker.sh /home/nonroot/start_worker.sh

# MAKE NONROOT USER OWNER OF NEEDED DIRECTORIES
USER    root
RUN     chown nonroot:nonroot /home/nonroot/src -R
RUN     chown nonroot:nonroot /home/nonroot/soiled-storage -R

# SET DEFAULT USER FOR RUNNING CONTAINER AS NONROOT
USER    nonroot