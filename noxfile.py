from pathlib import Path
import nox

ROOT_DIR = Path(__file__).parent

SRC_DIR = ROOT_DIR.joinpath("listings")
TEST_DIR = ROOT_DIR.joinpath("tests")
COV_DIR = ROOT_DIR.joinpath("coverage_report")


def _parse_pos_args(args: list[str]) -> list[str]:
    """Get args to pass into pytest."""

    valid_args = ["--l2"]

    pytest_args = []

    for arg in args:
        if arg in valid_args:
            pytest_args.append(arg)
        else:
            raise ValueError(f"Unknown arg '{arg}'")

    return pytest_args


@nox.session
def tests(session):
    """
    Run test suite.

    Optionally provide `--l2` flag to run application-level tests. Note that these
    require valid config files.
    """

    extra_args = _parse_pos_args(session.posargs)

    session.install("--group", "base", "--group", "test")
    session.run(
        "pytest",
        "-v",
        TEST_DIR,
        f"--cov={SRC_DIR}",
        "--cov-report",
        f"html:{COV_DIR}",
        *extra_args,
    )


@nox.session
def lint(session):
    """Run flake8."""

    session.install("flake8")
    session.run("flake8", SRC_DIR, TEST_DIR)
