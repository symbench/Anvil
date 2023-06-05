from anvil.config import AnvilConfig
from anvil.tests.base_test import BaseTest
from anvil.tests.utils import get_test_file_path


class TestConfig(BaseTest):
    def test_basic_data_generation_config(self):
        datagen_config = get_test_file_path("datagen.json")
        config = AnvilConfig.from_file(datagen_config)
        assert config.mode == "data_generation"
        assert config.seed_cad == "../usr_input/param_UUV_hull.FCStd"
        assert config.cad_param == {
            "nose": 200,
            "first_y": 95,
            "second_y": 200,
            "third_y": 1000,
            "fourth_y": 10,
            "fifth_y": 100,
            "sixth_y": 10,
        }
        assert config.simulator == "OpenFOAM"
        assert config.simulator_config == {
            "casefoldername": "UUVhull",
            "maxiter": 500,
            "infile": "./stl_repo/design.stl",
            "aoa": 0,
            "Uinlet": 20.0,
            "kinematic_viscosity": 0.000362,
            "kInlet": 0.06,
            "density": 1.225,
            "omegaInlet": 25.55,
            "meshing": "auto",
            "meshsize": 0.2,
        }

        assert config.design_space["nose"].min == 100
        assert config.design_space["nose"].max == 800

        assert config.design_space["first_y"].min == 5
        assert config.design_space["first_y"].max == 100

        assert config.design_space["second_y"].min == 5
        assert config.design_space["second_y"].max == 100

        assert config.design_space["third_y"].min == 5
        assert config.design_space["third_y"].max == 100

        assert config.design_space["fourth_y"].min == 5
        assert config.design_space["fourth_y"].max == 100

        assert config.design_space["fifth_y"].min == 5
        assert config.design_space["fifth_y"].max == 100

        assert config.design_space["sixth_y"].min == 5
        assert config.design_space["sixth_y"].max == 100

        assert config.sampling_method == "random"
        assert config.budget == 8

        assert config.optimizer.method == "BayesOpt"
        assert config.optimizer.aquisition == "LCB"
