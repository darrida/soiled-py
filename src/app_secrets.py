import os
from pathlib import Path

from loguru import logger
from pydantic import SecretStr

from _shared.env_file import dot_env_loader

#####################################################################################
# CURRENT PRE-LOADED SECRETS:
# 1. DJANGO_SECRET_KEY (baseline django requirement
# 2. SECRETS_KEEPASS_PW (opens wccsecrets keepass)
# 3. GitHub Auth values (enables GitHub org authentication):
#   - GITHUB_OAUTH_KEY
#   - GITHUB_OAUTH_SECRET
#
# Load Options:
# 1. Docker swarm secrets
#   - Environment variables matching names above with values set to the swarm secret file path inside a container
# 2. Standard environment variables
#   - Environment variables matches names above with value directly set to the relevant secret/information
# 3. ".env" file at root of project (outside of `src` directory)
#   - Environment variable set: ENV_FILE="true"
#   - `.env` file contains same values as option 2
#   - Example:
#   ```
#   ENVAR1=value1
#   ENVAR2=value2
#   ```
#
# NOTE
# - Secrets loaded are specified at bottom of this module
# - Utility functions are included here, rather than better organized somewhere else,
#   because all of this code needs to load before the django "application", django
#   "settings, etc
#####################################################################################


def get_docker_secret(name: str, full_path: bool = False) -> SecretStr | None:
    """
    Reads docker swarm secret file and returns value
    Args:
        name (str): docker swarm secret name
        full_path (bool): if True, `name` is opened; if False `/run/secrets/{name}` is opened

    Returns:
        swarm secret (SecretStr)
    """
    if full_path:
        secret_path = name
    else:
        secret_path = Path("/run") / "secrets" / name
    try:
        with open(secret_path) as f:
            secret = f.read()
    except FileNotFoundError:
        return None
    if not secret or secret == "":
        return None
    logger.info(f"Imported Docker Swarm Secret from `{name}`")
    return SecretStr(secret_value=secret)


def get_secret(name: str) -> SecretStr | None:
    """
    LOADS PARAMETERIZED SECRETS BEFORE ANY PART OF THE DJANGO APPLICATION IS STARTED

    Optional environment variable injection:
    - If ENV_FILE environment variable is set to "true", then environment variables specified in
      a local dev file named `.env` at the root of this git project (i.e., outside of `src` directory)
      are loaded into the environment variables when starting the application.

    Process loading environment variables
    - Uses environment variables
    - If value is `None`:
      - RETURNED: an error is raised
    - If value loaded includes `/run/secrets/`
      - envar value is treated as a path to a docker swarm secret file inside a container
      - RETURNED: the value inside the secret file
    - If envar value is `not None`, and does not include "/run/secrets":
      - RETURNED: the envar value

    Args:
        name (str): environment variable name associated with secret

    Returns:
        secret value (SecretStr)
    """
    value = os.environ.get(name)
    if value is None:
        print(value)
        raise ValueError(f"Environment variable or secret value {name} is None or doesn't exist.")
    if "/run/secrets/" in value:
        return get_docker_secret(value, full_path=True)
    logger.info(f"Imported secret {name} from environment variable.")
    return SecretStr(value)


if os.environ.get("ENV_FILE") == "true":
    dot_env_loader(Path(__file__).resolve().parent.parent / ".env")

APP_MODE = os.environ.get("APP_MODE")

logger.info("Loading secrets")
if os.environ.get("DJANGO_ENV") in ("local", "dev", "dev_tasks", "local_oracle"):
    SECRET_KEY = SecretStr(secret_value="this-is-not-a-safe-key")  # noqa: S106
else:
    SECRET_KEY = get_secret("DJANGO_SECRET_KEY")
ONEPASSWORD_TOKEN = get_secret("ONEPASSWORD_SERVICE_ACCOUNT_TOKEN")
