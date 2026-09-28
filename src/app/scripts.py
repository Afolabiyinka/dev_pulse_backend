import subprocess
import sys

from . import main


def dev() -> None:
    main()


def build() -> None:
    subprocess.run(["uv", "build"], check=True)


def test() -> None:
    subprocess.run([sys.executable, "-m", "pytest"], check=True)