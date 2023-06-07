from pathlib import Path

from anvil.cad.cad_asset import create_stl
from anvil.tests.base_test import BaseTest
from anvil.tests.utils import get_test_file_path


class TestCAD(BaseTest):
    def test_stl_file_creation(self):
        """Test that the STL file is created."""
        cad_file = get_test_file_path("param_UUV_hull.FCStd")
        create_stl(
            params={
                "nose": 200,
                "first_y": 95,
                "second_y": 200,
                "third_y": 1000,
                "fourth_y": 10,
                "fifth_y": 100,
                "sixth_y": 10,
            },
            filename=cad_file,
            destination="stl_repo",
        )

        assert Path("stl_repo/design.stl").resolve().exists()
