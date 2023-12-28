from __future__ import annotations

from pathlib import Path
import pkgutil

import nox

PYVER: str = "3.11"
TEST_PYVERS: list[str] = ["3.12", "3.11"]

PDM_VER: str = "2.11"

LINT_PATHS: list[str] = ["src", "tests", "./noxfile.py"]

REQUIREMENTS_OUTPUT_DIR: Path = Path("./requirements")

if not REQUIREMENTS_OUTPUT_DIR.exists():
    try:
        REQUIREMENTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        msg = Exception(
            f"Unable to create requirements export directory: '{REQUIREMENTS_OUTPUT_DIR}'. Details: {exc}"
        )
        print(msg)

        REQUIREMENTS_OUTPUT_DIR: Path = Path(".")

nox.options.error_on_external_run = False
nox.options.error_on_missing_interpreters = False

if pkgutil.find_loader("pdm"):
    PDM_EXTERNAL: bool = False
else:
    PDM_EXTERNAL: bool = True

print(f"Detected PDM in environment: {PDM_EXTERNAL}")


@nox.session(python=TEST_PYVERS, name="testenv", reuse_venv=True)
@nox.parametrize("pdm_ver", [PDM_VER])
def setup_base_testenv(session: nox.Session, pdm_ver: str):
    session.install(f"pdm>={pdm_ver}")

    print("Installing development dependencies with PDM")
    session.run("pdm", "install", "-d", external=True)


@nox.session(python=[PYVER], name="lint", reuse_venv=True)
def run_linter(session: nox.Session):
    for d in LINT_PATHS:
        lint_path: Path = Path(d)
        print(f"Running ruff imports sort on '{d}'")
        session.run(
            "pdm", "run", "ruff", "--select", "I", "--fix", lint_path, external=True
        )

        print(f"Formatting '{d}' with Black")
        session.run("pdm", "run", "black", lint_path, external=True)

        print(f"Running ruff checks on '{d}' with --fix")
        session.run(
            "pdm",
            "run",
            "ruff",
            "--config",
            "ruff.ci.toml",
            lint_path,
            "--fix",
            external=True,
        )


@nox.session(python=[PYVER], name="export", reuse_venv=True)
def export_requirements(session: nox.Session):
    print("Exporting production requirements")
    session.run(
        "pdm",
        "export",
        "--prod",
        "-o",
        f"{REQUIREMENTS_OUTPUT_DIR}/requirements.txt",
        "--without-hashes",
        external=True,
    )
    print("Exporting development requirements")
    session.run(
        "pdm",
        "export",
        "-d",
        "-o",
        f"{REQUIREMENTS_OUTPUT_DIR}/requirements.dev.txt",
        "--without-hashes",
        external=True,
    )
    print("Exporting CI requirements")
    session.run(
        "pdm",
        "export",
        "--group",
        "ci",
        "-o",
        f"{REQUIREMENTS_OUTPUT_DIR}/requirements.ci.txt",
        "--without-hashes",
        external=True,
    )


@nox.session(python=TEST_PYVERS, name="tests", reuse_venv=True)
def run_tests(session: nox.Session):
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
        external=True,
    )
