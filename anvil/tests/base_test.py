import pytest


class BaseTest:
    @pytest.fixture(autouse=True)
    def chdir(self, tmpdir):
        tmpdir.chdir()
