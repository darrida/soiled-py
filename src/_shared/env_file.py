import os
from pathlib import Path

from _shared.pretty_cli import color_text


class DotEnvLoaderError(Exception):
    pass


def dot_env_loader(filename_path: str | Path, ignore_warnings: bool = False):
    """Reads file to set environment variables for working session when script or app starts
    - Intended to be used for development
    - `.env` should be at root of project
    - `.env` should be excluded for commits by `.gitignore`
    """
    if not isinstance(filename_path, Path):
        filename_path = Path(filename_path)

    if not filename_path.exists():
        print(
            f"{color_text('WARNING:', 'yellow')} environment variable ENV_FILE=true was passed and no .env file exists at the provided path"
        )
        return

    try:
        with open(filename_path) as f:
            env_l = f.readlines()
    except FileNotFoundError as e:
        if "Not a directory" in str(e):
            raise DotEnvLoaderError("`dot_env_loader` failed to read .env file." "Ensure ")

    if not ignore_warnings:
        if not file_in_git_project_root(filename_path):
            print(
                f"{color_text('WARNING:', 'yellow')} {filename_path.name} not in the git project root (project path with .git directory)"
            )
        if not file_in_gitignore(filename_path):
            print(
                f"{color_text('WARNING:', 'yellow')} {filename_path.name} development configuration file not detected in .gitignore (ensure it's not committed to version control)"
            )

    for envar in env_l:
        envar = envar.strip()
        if envar.startswith("#"):
            continue
        if not envar:
            continue
        try:
            name, value = envar.split("=")
        except ValueError as e:
            if "too many values to unpack" in str(e) or "not enough values to unpack" in str(e):
                raise DotEnvLoaderError(
                    f"`dot_env_loader` failed on .env file line: >>> '{envar}' <<<"
                    f"\n{envar} does not meet .env file requirements."
                    "\nKey/value lines must be formatted as 'KEY1=value1' (one word key + '=' value)"
                )
            raise ValueError(e)
        os.environ[name] = value


def file_in_git_project_root(filename_path: str | Path) -> bool:
    if not isinstance(filename_path, Path):
        filename_path = Path(filename_path)

    git_dir = filename_path.parent / ".git"
    if not git_dir.is_dir():
        return False
    return True


def file_in_gitignore(filename_path: str | Path) -> bool:
    if not isinstance(filename_path, Path):
        filename_path = Path(filename_path)

    env_filename = filename_path.name
    gitignore_file = filename_path.parent / ".gitignore"
    if gitignore_file.exists():
        with open(gitignore_file) as f:
            gitignore_lines = [x.strip() for x in f.readlines() if not x.startswith("#")]
            if env_filename in gitignore_lines:
                return True
    return False
