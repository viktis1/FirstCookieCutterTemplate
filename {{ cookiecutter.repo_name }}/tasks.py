import os

from invoke import Context, task

WINDOWS = os.name == "nt"
REPO_NAME = "{{ cookiecutter.repo_name }}"
PYTHON_VERSION = "{{ cookiecutter.python_version }}"

# Setup commands
@task
def create_environment(ctx: Context) -> None:
    """Create a new conda environment for repo."""
    ctx.run(
        f"conda create --name {REPO_NAME} python={PYTHON_VERSION} pip --no-default-packages --yes",
        echo=True,
        pty=not WINDOWS,
    )

@task
def requirements(ctx: Context) -> None:
    """Install project requirements."""
    ctx.run("pip install -U pip setuptools wheel", echo=True, pty=not WINDOWS)
    ctx.run("pip install -r requirements.txt", echo=True, pty=not WINDOWS)
    ctx.run("pip install -e .", echo=True, pty=not WINDOWS)


# Project commands
@task
def train(ctx: Context) -> None:
    """Train model."""
    ctx.run(f"python src/train.py", echo=True, pty=not WINDOWS)

@task
def docker_build(ctx: Context, progress: str = "plain") -> None:
    """Build docker images."""
    ctx.run(
        f"docker build -t train:latest . -f dockerfiles/train.dockerfile --progress={progress}",
        echo=True,
        pty=not WINDOWS
    )
    ctx.run(
        f"docker build -t api:latest . -f dockerfiles/api.dockerfile --progress={progress}",
        echo=True,
        pty=not WINDOWS
    )

