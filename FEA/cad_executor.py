import FreeCAD  
import Mesh
import numpy as np
from FreeCAD import Units  
import Spreadsheet
import json

class CAD_asset(object):
    """
    The base class to work with parametric pressure vessel models.
    """

    def __init__(self, filename: str, param_dictionary:dict):
        """
        Creates a pressure vessel analysis class that can be used to run
        multiple simulations for the given design template by changing its
        parameters.
        """
        self.filename = filename
       

        print("Opening:", filename)
        self.doc = FreeCAD.open(filename)
        self.sheet = self.doc.getObjectsByLabel('Parameters')[0]
        
        print('***Parametric properties are:***')
        
        par_variables= list(vars(self.sheet).keys())
        input_param= list(param_dictionary['fea_param'].keys())
        print('-> paramters variables are:',par_variables)
        print('-> Input dictionary is:', input_param)
        assert  all(x in par_variables for x in input_param)
        self.param_dict = param_dictionary
        

    def set_parameter(self):
      for key, value in self.param_dict["fea_param"].items():
       try:
        value= str(value)+"mm"
        print('key is:',type(key),key,'value is:',value)
        self.sheet.set(key,value)
       except: 
        print('failed in setting parameter values') 
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
        
    
    def create_stl(self, location='../stl_repo/'):   
        #To Do :direct stl file to right directory
        """
        Generate stl file from the current design

        """
        try:
         __objs__=self.doc.getObject("Body")
         print(__objs__.Name, self.doc.Name)
         _name=""
         for key, value in self.param_dict["fea_param"].items():
             value= str(value)+"mm"
             print('key is:',type(key),key,'value is:',value)
             _name=_name+'_'+key+'_'+str(value)
         stl_dumpfile=location+"anvil"+_name+".stl"
         print('stl dump is:',stl_dumpfile)
         print('--> Current working dir:',os.getcwd())
         stl_name= u"./stl_repo/fishiefish.stl"
         
         Mesh.export([__objs__], 'u'+stl_dumpfile)
         Mesh.export([__objs__], stl_name)
         del __objs__    
        except:
          print("An error occurred while creating stl file") 
    


    def get_body_area(self):
        """
        Returns the body volume in square meters.
        """
        obj = self.doc.getObject('Body')
        return obj.Shape.Area * 1e-6

    def get_body_volume(self):
        """
        Returns the body volume in cubic meters.
        """
        obj = self.doc.getObject('Body')
        return obj.Shape.Volume * 1e-9

    def get_outer_area(self):
        obj = self.doc.getObject('Body')
        return obj.Shape.OuterShell.Area * 1e-6

    def get_outer_volume(self):
        obj = self.doc.getObject('Body')
        return obj.Shape.OuterShell.Volume * 1e-3  # in cubic cm

    def get_inner_area(self):
        obj = self.doc.getObject('Body')
        return self.get_body_area() - self.get_outer_area()

    def get_inner_volume(self):
        obj = self.doc.getObject('Body')
        return self.get_outer_volume() - self.get_body_volume()

    def clean(self):
        """
        Removes all temporary artifacts from the model.
        """
        if self.doc.getObject('CCX_Results'):
            self.doc.removeObject('CCX_Results')
        if self.doc.getObject('ResultMesh'):
            self.doc.removeObject('ResultMesh')
        if self.doc.getObject('ccx_dat_file'):
            self.doc.removeObject('ccx_dat_file')




if __name__ == '__main__':
    with open('input_config.json', 'r') as f:
      data = json.load(f)

    cad_obj = CAD_asset('./seed_cad/Myring_hull_spreadsheet.FCStd',data) 
    cad_obj.set_parameter()
    cad_obj.create_stl()
