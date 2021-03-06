from pathlib import Path

import nox


HERE = Path(__file__).parent


@nox.session
def test(session: nox.Session) -> None:
    ...


@nox.session
def test(session: nox.Session) -> None:
    """Run the complete test suite"""
    session.install("--upgrade", "pip", "setuptools", "wheel")
    session.notify("test_suite", posargs=session.posargs)
    session.notify("test_style")


@nox.session
def test_suite(session: nox.Session) -> None:
    """Run the Python-based test suite"""
    install_requirements_file(session, "test-env")
    session.install(".")
    session.chdir("")
    session.run("no-tests-yet")


@nox.session
def test_style(session: nox.Session) -> None:
    """Check that style guidelines are being followed"""
    install_requirements_file(session, "check-style")
    session.run("flake8", "src", "tests")
    black_default_exclude = r"\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|\.svn|_build|buck-out|build|dist"
    session.run(
        "black",
        ".",
        "--check",
        "--exclude",
        rf"/({black_default_exclude}|venv)/",
    )
    session.run("isort", ".", "--check-only")


def install_requirements_file(session: nox.Session, name: str) -> None:
    file_path = HERE / "requirements" / (name + ".txt")
    assert file_path.exists(), f"requirements file {file_path} does not exist"
    session.install("-r", str(file_path))
