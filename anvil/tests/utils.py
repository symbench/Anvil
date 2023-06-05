from pathlib import Path


def get_test_file_path(file_name: str) -> str:
    """Get the path to a test file."""

    return str(Path(__file__).parent.resolve() / "data" / file_name)
