import FreeCAD  # noqa
import Mesh
import numpy as np
from FreeCAD import Units  # noqa


class GliderVessel(object):
    """
    The base class to work with parametric pressure vessel models.
    """

    def __init__(self, filename: str, debug=True):
        """
        Creates a pressure vessel analysis class that can be used to run
        multiple simulations for the given design template by changing its
        parameters.
        """
        self.filename = filename
        self.debug = debug

        print("Opening:", filename)
        self.doc = FreeCAD.open(filename)
        self.exp_index = None

        self.sketch_params = []
        obj = self.doc.getObject("Sketch")
        """
        print('***Parametric properties are:***')
        print('Sketch is:')
        for c in obj.Constraints:
            if c.Name:
                self.sketch_params.append(str(c.Name))
                print(str(c.Name))
        """

    def set_nose_tail_y(self, y_loc):
        try:
            obj = self.doc.getObject("Sketch")
            obj.setDatum("nose1_y", Units.Quantity(y_loc[0], Units.Unit("mm")))
            obj.setDatum("nose2_y", Units.Quantity(y_loc[1], Units.Unit("mm")))
            obj.setDatum("nose3_y", Units.Quantity(y_loc[2], Units.Unit("mm")))
            obj.setDatum("nose4_y", Units.Quantity(y_loc[3], Units.Unit("mm")))

            obj.setDatum("tail1_y", Units.Quantity(y_loc[4], Units.Unit("mm")))
            obj.setDatum("tail2_y", Units.Quantity(y_loc[5], Units.Unit("mm")))
            obj.setDatum("tail3_y", Units.Quantity(y_loc[6], Units.Unit("mm")))
            obj.setDatum("tail4_y", Units.Quantity(y_loc[7], Units.Unit("mm")))
            self.doc.recompute()
        except:
            print("failed in setting tail y locations")

    def set_tail_len(self, tail_l):
        try:
            obj = self.doc.getObject("Sketch")
            obj.setDatum("myring_c", Units.Quantity(tail_l, Units.Unit("mm")))
            self.doc.recompute()
        except:
            print("failed in setting tail length")

    def set_nose_len(self, nose_l):
        try:
            obj = self.doc.getObject("Sketch")
            obj.setDatum("myring_a", Units.Quantity(nose_l, Units.Unit("mm")))
            self.doc.recompute()
        except:
            print("failed in setting nose length")

    def set_fairing_len(self, body_l):
        try:
            obj = self.doc.getObject("Sketch")
            obj.setDatum("myring_b", Units.Quantity(body_l, Units.Unit("mm")))
            self.doc.recompute()
        except:
            print("failed in setting body length")

    def set_fairing_rad(self, rad_l):
        try:
            obj = self.doc.getObject("Sketch")
            obj.setDatum("myring_r", Units.Quantity(rad_l, Units.Unit("mm")))
            self.doc.recompute()
        except:
            print("failed in setting radius")

    def get_fairing_details(self):
        obj_spz = self.doc.getObject("Sketch")
        my_b = obj_spz.getDatum("myring_b").getValueAs("mm")
        my_r = obj_spz.getDatum("myring_r").getValueAs("mm")
        my_a = obj_spz.getDatum("myring_a").getValueAs("mm")
        my_c = obj_spz.getDatum("myring_c").getValueAs("mm")
        return [my_a, my_b, my_c, my_r]

    def get_nose_x_loc(self):
        obj_spz = self.doc.getObject("Sketch")
        n1x = obj_spz.getDatum("nose1_x").getValueAs("mm")
        n2x = obj_spz.getDatum("nose2_x").getValueAs("mm")
        n3x = obj_spz.getDatum("nose3_x").getValueAs("mm")
        n4x = obj_spz.getDatum("nose4_x").getValueAs("mm")
        return np.array([n1x, n2x, n3x, n4x])

    def get_tail_x_loc(self):
        obj_spz = self.doc.getObject("Sketch")
        t1x = obj_spz.getDatum("tail1_x").getValueAs("mm")
        t2x = obj_spz.getDatum("tail2_x").getValueAs("mm")
        t3x = obj_spz.getDatum("tail3_x").getValueAs("mm")
        t4x = obj_spz.getDatum("tail4_x").getValueAs("mm")
        return np.array([t1x, t2x, t3x, t4x])

    def print_info(self):

        self.recompute()
        obj_spz = self.doc.getObject("Sketch")
        my_b = obj_spz.getDatum("myring_b").getValueAs("mm")
        my_r = obj_spz.getDatum("myring_r").getValueAs("mm")
        my_a = obj_spz.getDatum("myring_a").getValueAs("mm")
        my_c = obj_spz.getDatum("myring_c").getValueAs("mm")

        b1y = obj_spz.getDatum("body1_y").getValueAs("mm")
        b2y = obj_spz.getDatum("body2_y").getValueAs("mm")
        b3y = obj_spz.getDatum("body3_y").getValueAs("mm")
        b4y = obj_spz.getDatum("body4_y").getValueAs("mm")
        b5y = obj_spz.getDatum("body5_y").getValueAs("mm")

        n1y = obj_spz.getDatum("nose1_y").getValueAs("mm")
        n2y = obj_spz.getDatum("nose2_y").getValueAs("mm")
        n3y = obj_spz.getDatum("nose3_y").getValueAs("mm")
        n4y = obj_spz.getDatum("nose4_y").getValueAs("mm")

        t1y = obj_spz.getDatum("tail1_y").getValueAs("mm")
        t2y = obj_spz.getDatum("tail2_y").getValueAs("mm")
        t3y = obj_spz.getDatum("tail3_y").getValueAs("mm")
        t4y = obj_spz.getDatum("tail4_y").getValueAs("mm")

        print("------Body properties:-------")
        print("  body_area = {:.6f} m^2".format(self.get_outer_area()))
        print("  body_volume = {:.9f} m^3".format(self.get_outer_volume()))
        print(" my_a:", my_a, "my_b:", my_b, "my_c:", my_c, "my_r:", my_r)
        print("  b1y:", b1y, "b2y:", b2y, "b3y:", b3y, "b4y:", b4y, "b5y:", b5y)
        print("  n1y:", n1y, "n2y:", n2y, "n3y:", n3y, "n4y:", n4y)
        print("  t1y:", t1y, "t2y:", t2y, "t3y:", t3y, "t4y:", t4y)
        print("------------------------------")

    def recompute(self):
        """
        Recompute the design after setting all parametric values of design
        """
        self.clean()
        self.doc.recompute()

    def create_stl(self, save_name: str) -> None:
        """
        Generate stl file from the current design
        """
        assert save_name.endswith(
            ".stl"
        ), f"The extension {save_name.split('.')[-1]} is not valid."
        try:
            __objs__ = self.doc.getObject("Body")
            # print(__objs__.Name, self.doc.Name)
            Mesh.export([__objs__], save_name)
            del __objs__
        except:
            print("An error occurred while creating stl file")

    def get_exp_index(self) -> int:
        """
        Returns the experiment index of current design.
        """
        print("self index is:", self.exp_index)
        return self.exp_index

    def set_exp_index(self, exp_ind) -> int:
        """
        set the experiment index of current design
        """
        self.exp_index = exp_ind

    def get_body_area(self):
        """
        Returns the body volume in square meters.
        """
        obj = self.doc.getObject("Body")
        return obj.Shape.Area * 1e-6

    def get_body_volume(self):
        """
        Returns the body volume in cubic meters.
        """
        obj = self.doc.getObject("Body")
        return obj.Shape.Volume * 1e-9

    def get_outer_area(self):
        obj = self.doc.getObject("Body")
        return obj.Shape.OuterShell.Area * 1e-6

    def get_outer_volume(self):
        obj = self.doc.getObject("Body")
        return obj.Shape.OuterShell.Volume * 1e-3  # in cubic cm

    def get_inner_area(self):
        obj = self.doc.getObject("Body")
        return self.get_body_area() - self.get_outer_area()

    def get_inner_volume(self):
        obj = self.doc.getObject("Body")
        return self.get_outer_volume() - self.get_body_volume()

    def clean(self):
        """
        Removes all temporary artifacts from the model.
        """
        if self.doc.getObject("CCX_Results"):
            self.doc.removeObject("CCX_Results")
        if self.doc.getObject("ResultMesh"):
            self.doc.removeObject("ResultMesh")
        if self.doc.getObject("ccx_dat_file"):
            self.doc.removeObject("ccx_dat_file")
