import os

from invoke import Context, task

WINDOWS = os.name == "nt"
REPO_NAME = "{{ cookiecutter.repo_name }}"
PYTHON_VERSION = "{{ cookiecutter.python_version }}"

# Setup commands
@task
def create_environment(ctx):
    """Create a new conda environment for repo and install up-to-date invoke."""
    ctx.run(
        f"conda create --name {REPO_NAME} python={PYTHON_VERSION} pip --no-default-packages --yes",
        echo=True,
        pty=not WINDOWS,
    )

    ctx.run(
        f"conda run -n {REPO_NAME} pip install invoke setuptools wheel",
        echo=True,
        pty=not WINDOWS,
    )
    print(
        f"To activate it, run: conda activate {REPO_NAME}\n"
    )

@task
def requirements(ctx) -> None:
    """Install project requirements. You must install PyTorch manually depending on your system."""
    print(
        "\nPyTorch is not installed automatically.\n"
        "Please visit: https://pytorch.org/get-started/locally/ to choose the correct version.\n"
        "Then paste the install command below (or press Enter to skip):\n"
    )

    user_cmd = input(">>> ")
    if user_cmd.strip():
        ctx.run(user_cmd, echo=True, pty=not WINDOWS)
    else:
        print("Skipping PyTorch install. Be sure to install it manually before using GPU features.")


    # ctx.run("python -m pip install -U pip setuptools wheel", echo=True, pty=not WINDOWS)
    ctx.run("python -m pip install -e .", echo=True, pty=not WINDOWS)



@task
def docker_build(ctx, tag="train:latest", progress: str = "plain") -> None:
    """Build docker images."""
    ctx.run(
        f"docker build -t {tag} . -f dockerfiles/train.dockerfile --progress={progress}",
        echo=True,
        pty=not WINDOWS
    )



