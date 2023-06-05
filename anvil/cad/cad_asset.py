import sys
from typing import Dict

import FreeCAD
import Mesh

from anvil._logger import get_logger

logger = get_logger(__name__)


class CADAsset(object):
    """
    The base class to work with parametric pressure vessel models.
    """

    def __init__(self, filename: str, param_dictionary: Dict[str, float]):
        """
        Creates a CAD asset that can be used to run
        multiple simulations for the given design template by changing its
        parameters.
        """
        self.filename = filename

        self.doc = FreeCAD.open(filename)
        self.sheet = self.doc.getObjectsByLabel("Spreadsheet")[0]

        logger.info(f"***Parametric properties are:***, {dir(self.sheet)}")

        par_variables = list(vars(self.sheet).keys())

        # genrating list of variables A1-A100.
        placeholder_cells = ["A" + str(n + 1) for n in range(100)]

        # finding how many are there in CAD drawing
        self.cells = list(set(placeholder_cells).intersection(par_variables))
        logger.info("-->cells:", self.cells)
        self.cad_variables_name = [self.sheet.get(cell) for cell in self.cells]

        self.input_config_dic = param_dictionary
        logger.info(f"param dict: {param_dictionary}")
        self.input_config_key = list(param_dictionary.keys())
        logger.info(f"input keys: {self.input_config_key}")

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
                    self.sheet.set(value_cell, value)
                else:
                    pass
            except:  # noqa E722
                logger.error("failed in setting parameter values")

        self.doc.recompute()

    def set_parameter_by_value(self, variables_to_optimize, X):
        for cell in self.cells:
            try:
                # print('------------->cell is:',cell)
                param_name = self.sheet.get(cell)
                # print('param name is:',param_name,'input config param:',self.input_config_key)
                # print('Variable to optimize:',variables_to_optimize,'value:',X)
                if param_name in self.input_config_key:
                    # print('param name is:',param_name)
                    value = X[0][variables_to_optimize.index(param_name)]
                    # value= self.input_config_dic[param_name]
                    value = str(value) + "mm"
                    # print('value is:',value)
                    # print('--------------------------------------')
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
        pass

        """
        print("------Body properties:-------")
        print("  body_area = {:.6f} m^2".format(self.get_outer_area()))
        print("  body_volume = {:.9f} m^3".format(self.get_outer_volume()))
        print("------------------------------")
        """

    def recompute(self):
        """
        Recompute the design after setting all parametric values of design
        """
        self.clean()
        self.doc.recompute()

    def create_stl(self, location="./stl_repo/"):
        # To Do :direct stl file to right directory
        """
        Generate stl file from the current design

        """
        # print('In stl')
        try:
            __objs__ = self.doc.getObject("Body")
            print(__objs__.Name, self.doc.Name)
            stl_name = "./stl_repo/design.stl"
            Mesh.export([__objs__], stl_name)
            del __objs__
        except:  # noqa E722
            logger.error("An error occurred while creating stl file")


def create_stl(config, filename):
    cad_obj = CADAsset(filename, config)
    cad_obj.set_parameter()
    cad_obj.create_stl()
