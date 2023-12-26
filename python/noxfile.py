from __future__ import annotations

import nox

## List of Python versions for nox
#  Note: Interpreters must already be available. Look into pyenv for installing
#  multiple versions of Python at the same time
PYTHON_VERSIONS: list[str] = ["3.11", "3.12"]

## Default Python version to use throughout Nox sessions
PYVER: str = "3.11"

@nox.session(python=[PYVER], name="setup-env", reuse_venv=True)
@nox.parametrize("pdm_ver", ["2.11"])
def setup_env(session: nox.Session, pdm_ver: str):
    """Setup local dev environment with PDM.
    
    Description:
    ------------
    
    **NOTE**: This session assumes you're using PDM. If you are using pip, remove the `@nox.parameterize()` decorator,
        the `pdm: str` parameter in the `setup_env()` function declaration. Then, comment the `install with pdm` code below and
        uncomment `install with pip`.
        
    Setup the local development environment by installing dependencies & running whatever setup operations are needed.
    """
    ## Install with PDM
    session.install(f"pdm>={pdm_ver}")

    session.run("pdm", "install")
    session.run("pdm", "sync")

    ## Install with Pip
    # session.run("pip", "install", "-r", "reequirements.txt")


@nox.session(python=PYTHON_VERSIONS, name="tests", reuse_venv=True)
def tests(session: nox.Session):
    """Run Pytest suite."""
    session.install("pytest")
    session.run("pytest", "tests/")


@nox.session(python=[PYVER], name="lint", reuse_venv=True)
def lint(session: nox.Session):
    """Lint & format code with Ruff, Black."""
    session.install("black", "ruff")
    session.run("ruff", "--select", "I", "--fix", "src")
    session.run("black", "src")
    session.run("ruff", "check", "--config", "ruff.ci.toml", "src", "--fix")


@nox.session(python=[PYVER], name="export", reuse_venv=True)
def export_requirements(session: nox.Session):
    """Export requirements.txt file(s) with PDM."""
    session.install("pdm")
    session.run("pdm", "export", "--prod", "-o", "requirements.txt", "--without-hashes")
    session.run("pdm", "export", "-d", "-o", "requirements.dev.txt", "--without-hashes")
