from __future__ import annotations

from pathlib import Path
import platform

import nox

nox.options.default_venv_backend = "venv"
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = False
nox.options.error_on_missing_interpreters = False
# nox.options.report = True

## Define sessions to run when no session is specified
nox.sessions = ["lint", "export", "tests"]

## Get tuple of Python ver ('maj', 'min', 'mic')
PY_VER_TUPLE = platform.python_version_tuple()
## Dynamically set Python version
DEFAULT_PYTHON: str = f"{PY_VER_TUPLE[0]}.{PY_VER_TUPLE[1]}"
## Define versions to test
PY_VERSIONS: list[str] = ["3.12", "3.11"]
## Set PDM version to install throughout
PDM_VER: str = "2.11"
## Set paths to lint with the lint session
LINT_PATHS: list[str] = ["src", "tests", "./noxfile.py"]
## Set directory for requirements.txt file output
REQUIREMENTS_OUTPUT_DIR: Path = Path("./requirements")
## Ensure REQUIREMENTS_OUTPUT_DIR path exists
if not REQUIREMENTS_OUTPUT_DIR.exists():
    try:
        REQUIREMENTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        msg = Exception(
            f"Unable to create requirements export directory: '{REQUIREMENTS_OUTPUT_DIR}'. Details: {exc}"
        )
        print(msg)

        REQUIREMENTS_OUTPUT_DIR: Path = Path(".")


@nox.session(python=PY_VERSIONS, name="build-env")
@nox.parametrize("pdm_ver", [PDM_VER])
def setup_base_testenv(session: nox.Session, pdm_ver: str):
    print(f"Default Python: {DEFAULT_PYTHON}")
    session.install(f"pdm>={pdm_ver}")

    print("Installing dependencies with PDM")
    session.run("pdm", "sync")
    session.run("pdm", "install")


@nox.session(python=[DEFAULT_PYTHON], name="lint")
def run_linter(session: nox.Session):
    session.install("ruff", "black")

    for d in LINT_PATHS:
        if not Path(d).exists():
            print(f"Skipping lint path '{d}', could not find path")
            pass
        else:
            lint_path: Path = Path(d)
            print(f"Running ruff imports sort on '{d}'")
            session.run(
                "ruff",
                "--select",
                "I",
                "--fix",
                lint_path,
            )

            print(f"Formatting '{d}' with Black")
            session.run(
                "black",
                lint_path,
            )

            print(f"Running ruff checks on '{d}' with --fix")
            session.run(
                "ruff",
                "--config",
                "ruff.ci.toml",
                lint_path,
                "--fix",
            )


@nox.session(python=[DEFAULT_PYTHON], name="export")
@nox.parametrize("pdm_ver", [PDM_VER])
def export_requirements(session: nox.Session, pdm_ver: str):
    session.install(f"pdm>={pdm_ver}")

    print("Exporting production requirements")
    session.run(
        "pdm",
        "export",
        "--prod",
        "-o",
        f"{REQUIREMENTS_OUTPUT_DIR}/requirements.txt",
        "--without-hashes",
    )

    print("Exporting development requirements")
    session.run(
        "pdm",
        "export",
        "-d",
        "-o",
        f"{REQUIREMENTS_OUTPUT_DIR}/requirements.dev.txt",
        "--without-hashes",
    )

    # print("Exporting CI requirements")
    # session.run(
    #     "pdm",
    #     "export",
    #     "--group",
    #     "ci",
    #     "-o",
    #     f"{REQUIREMENTS_OUTPUT_DIR}/requirements.ci.txt",
    #     "--without-hashes",
    # )


@nox.session(python=PY_VERSIONS, name="tests")
@nox.parametrize("pdm_ver", [PDM_VER])
def run_tests(session: nox.Session, pdm_ver: str):
    session.install(f"pdm>={pdm_ver}")
    session.run("pdm", "install")

    print("Running Pytest tests")
    session.run(
        "pdm",
        "run",
        "pytest",
        "-n",
        "auto",
        "--tb=auto",
        "-v",
        "-rsXxfP",
    )


@nox.session(python=PY_VERSIONS, name="pre-commit-all")
def run_pre_commit_all(session: nox.Session):
    session.install("pre-commit")
    session.run("pre-commit")

    print("Running all pre-commit hooks")
    session.run("pre-commit", "run")


@nox.session(python=PY_VERSIONS, name="pre-commit-update")
def run_pre_commit_autoupdate(session: nox.Session):
    session.install(f"pre-commit")

    print("Running pre-commit update hook")
    session.run("pre-commit", "run", "pre-commit-update")


@nox.session(python=PY_VERSIONS, name="pre-commit-nbstripout")
def run_pre_commit_nbstripout(session: nox.Session):
    session.install(f"pre-commit")

    print("Running nbstripout pre-commit hook")
    session.run("pre-commit", "run", "nbstripout")
