import sys
from pathlib import Path
from typing import Dict, Union

import FreeCAD
import Mesh

from anvil._logger import get_logger

logger = get_logger(__name__)

SPREADSHEET_LABEL = "Spreadsheet"


class CADAsset(object):
    """The base class to work with parametric pressure vessel models.

    This class creates a CAD asset that can be used to run multiple simulations
    for the given design template by changing its parameters.

    Parameters
    ----------
    filename: str
        The path to the CAD file.
    param_dictionary: Dict[str, float]
        The dictionary of parameters to use for the CAD file.
    """

    def __init__(
        self, filename: str, param_dictionary: Dict[str, float]
    ) -> None:
        self.filename = filename

        self.doc = FreeCAD.open(filename)
        self.sheet = self.doc.getObjectsByLabel(SPREADSHEET_LABEL)[0]

        par_variables = list(vars(self.sheet).keys())

        # genrating list of variables A1-A100.
        placeholder_cells = ["A" + str(n + 1) for n in range(100)]

        # finding how many are there in CAD drawing
        self.cells = list(set(placeholder_cells).intersection(par_variables))
        self.cad_variables_name = [self.sheet.get(cell) for cell in self.cells]
        logger.debug(f"Parametric properties are: {self.cad_variables_name}")

        self.input_config_dic = param_dictionary
        logger.debug(f"param dict: {param_dictionary}")
        self.input_config_key = list(param_dictionary.keys())
        logger.debug(f"input keys: {self.input_config_key}")

        try:
            assert all(
                x in self.cad_variables_name for x in self.input_config_key
            )
        except AssertionError:
            logger.error(
                "!!!! Variable name mismatch between config file and CAD seed design !!!"
            )
            logger.error(
                "CAD parameters are:{},\n Config file variables are:{}".format(
                    self.cad_variables, self.input_param
                )
            )
            sys.exit()

    def check_cells(self, column: str):
        pass

    def set_parameter(self):
        for cell in self.cells:
            try:
                param_name = self.sheet.get(cell)
                if param_name in self.input_config_key:
                    value = self.input_config_dic[param_name]
                    value = str(value) + "mm"
                    value_cell = "B" + cell[1:]
                    logger.debug(
                        f"setting {param_name}({value_cell}) to {value}"
                    )
                    self.sheet.set(value_cell, value)
                else:
                    pass
            except:  # noqa E722
                logger.error("failed in setting parameter values")
        logger.info("Finished setting parameters, recomputing...")
        self.doc.recompute()

    def set_parameter_by_value(self, variables_to_optimize, X):
        for cell in self.cells:
            try:
                param_name = self.sheet.get(cell)
                if param_name in self.input_config_key:
                    value = X[0][variables_to_optimize.index(param_name)]
                    value = str(value) + "mm"
                    value_cell = "B" + cell[1:]
                    self.sheet.set(value_cell, value)
                else:
                    pass
            except:  # noqa E722
                logger.error("failed in setting parameter values")
        self.doc.recompute()

    def print_info(self):
        # to do-recomute to verify if changing the parameters took place.
        self.recompute()

    def recompute(self):
        """
        Recompute the design after setting all parametric values of design
        """
        self.clean()
        self.doc.recompute()

    def create_stl(self, location: Union[str, Path] = "./stl_repo/"):
        """Generate stl file from the current design"""
        location = Path(location)
        location.mkdir(parents=True, exist_ok=True)

        try:
            __objs__ = self.doc.getObject("Body")
            stl_name = f"{location}/design.stl"
            Mesh.export([__objs__], stl_name)
            logger.info(f"STL file created at {stl_name}")
            del __objs__
        except:  # noqa E722
            logger.error("An error occurred while creating stl file")


def create_stl(filename, params, destination="./stl_repo/"):
    """Create stl file from the parametric CAD file."""
    cad_obj = CADAsset(filename, params)
    cad_obj.set_parameter()
    cad_obj.create_stl(destination)
