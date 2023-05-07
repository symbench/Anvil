from utils import *
add_freecad_libs_to_path()

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
        Creates a CAD asset that can be used to run
        multiple simulations for the given design template by changing its
        parameters.
        """
        self.filename = filename
        print("Opening:", filename)
        self.doc = FreeCAD.open(filename)
        self.sheet = self.doc.getObjectsByLabel('Parameters')[0]
        
        #print('***Parametric properties are:***',dir(self.sheet))
        
        par_variables= list(vars(self.sheet).keys())
        
        #genrating list of variables A1-A100.
        placeholder_cells = ["A"+str(n+1) for n in range(100)] 
        
        #finding how many are there in CAD drawing
        self.cells=list(set(placeholder_cells).intersection(par_variables))
        print('-->cells:',self.cells)
        self.cad_variables_name=[self.sheet.get(cell) for cell in self.cells]
        
        
        
        self.input_config_dic=param_dictionary
        self.input_config_key= list(param_dictionary['fea_param'].keys())
        
        
        try:
         assert  all(x in self.cad_variables_name for x in self.input_config_key)
        except AssertionError:
         print('!!!! Variable name mismatch between config file and CAD seed design !!!')
         print('CAD parameters are:{},\n Config file variables are:{}'.format(self.cad_variables,self.input_param))
         sys.exit()
          
        print('Didnt exit')
        

    def check_cells(self,column:str):
         pass

    def set_parameter(self):
      for cell in self.cells:
       try:
        #print('cell is:',cell)
        param_name=self.sheet.get(cell)
        #print('param name is:',param_name,'input config param:',self.input_config_key)
        if param_name in self.input_config_key:    
         #print('param name is:',param_name)
         value= self.input_config_dic['fea_param'][param_name]
         value= str(value)+"mm"    
         #print('value is:',value)
         value_cell= 'B'+cell[1:]
         self.sheet.set(value_cell,value)
        else:
         pass
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
        #print('In stl')
        try:
         __objs__=self.doc.getObject("Body")
         print(__objs__.Name, self.doc.Name)
         #_name=""
         #for key, value in self.input_config_dic["fea_param"].items():
         #    value= str(value)+"mm"
         #    print('key is:',type(key),key,'value is:',value)
         #    _name=_name+'_'+key+'_'+str(value)
         #stl_dumpfile=location+"anvil"+_name+".stl"
         #print('stl dump is:',stl_dumpfile)
         #print('--> Current working dir:',os.getcwd())
         stl_name= u"../stl_repo/fishiefish.stl"
         #stl_dumpfile= stl_dumpfile
         #print('STL name:',stl_name,'stl-dump file name:',stl_dumpfile)
         #Mesh.export([__objs__], stl_dumpfile)
         Mesh.export([__objs__], stl_name)
         del __objs__    
        except:
          print("An error occurred while creating stl file") 
    






if __name__ == '__main__':
    with open('input_config.json', 'r') as f:
      data = json.load(f)

    cad_obj = CAD_asset('./seed_cad/Myring_hull_spreadsheet.FCStd',data) 
    cad_obj.set_parameter()
    cad_obj.create_stl()
