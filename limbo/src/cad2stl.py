from .utils import *
add_freecad_libs_to_path()

import FreeCAD  
import Mesh
import numpy as np
from FreeCAD import Units  
import Spreadsheet
import json

import logging
log = logging.getLogger('anvil.log')


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
        log.info("--> Provided parametric CAD file is :{}".format(filename))
        self.doc = FreeCAD.open(filename)
        log.debug("Opened the CAD file***")
        self.sheet = self.doc.getObjectsByLabel('Spreadsheet')[0]
        
        #print('***Parametric properties are:***',dir(self.sheet))
        
        par_variables= list(vars(self.sheet).keys())
        
        #genrating list of variables A1-A100.
        placeholder_cells = ["A"+str(n+1) for n in range(100)] 
        
        #finding how many are there in CAD drawing
        self.cells=list(set(placeholder_cells).intersection(par_variables))
        #print('-->cells:',self.cells)
        self.cad_variables_name=[self.sheet.get(cell) for cell in self.cells]
        
        
        
        self.input_config_dic=param_dictionary
        #print('param dict:',param_dictionary)
        self.input_config_key= list(param_dictionary.keys())
        #print('input keys:',self.input_config_key)
        
        
        try:
         assert  all(x in self.cad_variables_name for x in self.input_config_key)
        except AssertionError:
         log.error('!!!! Variable name mismatch between config file and CAD seed design !!!')
         log.error('CAD parameters are:{},\n Config file variables are:{}'.format(self.cad_variables,self.input_param))
         sys.exit()
          
        log.info('**Everything looks good with CAD set-up***')
        

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
         value= self.input_config_dic[param_name]
         value= str(value)+"mm"    
         #print('value is:',value)
         value_cell= 'B'+cell[1:]
         self.sheet.set(value_cell,value)
        else:
         pass
       except: 
        log.error('failed in setting parameter values') 
      self.doc.recompute()
      
    def set_parameter_by_value(self,variables_to_optimize,X):
      for cell in self.cells:
       try:
        #print('------------->cell is:',cell)
        param_name=self.sheet.get(cell)
        #print('param name is:',param_name,'input config param:',self.input_config_key)
        #print('Variable to optimize:',variables_to_optimize,'value:',X)
        if param_name in self.input_config_key:    
         #print('param name is:',param_name)
         value= X[0][variables_to_optimize.index(param_name)]
         #value= self.input_config_dic[param_name]
         value= str(value)+"mm"    
         #print('value is:',value)
         #print('--------------------------------------')
         value_cell= 'B'+cell[1:]
         self.sheet.set(value_cell,value)
        else:
         pass
       except: 
        log.error('failed in setting parameter values') 
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
        
    
    def create_stl(self, location='./stl_repo/'):   
        #To Do :direct stl file to right directory
        """
        Generate stl file from the current design

        """
        #print('In stl')
        try:
         __objs__=self.doc.getObject("Body")
         log.debug('selected shape is: {} and design name is {}'.format(__objs__.Name, self.doc.Name))
         stl_name= u"./stl_repo/design.stl"
         Mesh.export([__objs__], stl_name)
         del __objs__    
        except:
          log.error("An error occurred while creating stl file") 
    






if __name__ == '__main__':
    with open('input_config.json', 'r') as f:
      data = json.load(f)

    cad_obj = CAD_asset('../cad_seed/Myring_hull_spreadsheet.FCStd',data) 
    cad_obj.set_parameter()
    cad_obj.create_stl()
