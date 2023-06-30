import argparse
import os
import numpy as np
import pandas as pd
import shutil
import glob 
import subprocess
import time
from cad2stl import *
from foam_runner import *
import sys 
from samplers import *
import GPyOpt
from subprocess import PIPE, run
import random
from numpy.random import seed
import json



def delete_dir(loc):
    print('*Deleted directory:',loc)
    shutil.rmtree(loc)

def copy_dir(src,dst):
	print('*Copied directory from',src,'to destination:',dst)
	shutil.copytree(src, dst)

def deletefiles(loc):
	print('Deleted files from location:',loc)
	file_loc= loc+'/*'
	files = glob.glob(file_loc)
	for f in files:
		os.remove(f)

def copy_file(src,dst):
	print('*Copied file from',src,'to destination:',dst)
	shutil.copy(src, dst)

def save_data(file_name,x):
    with open(file_name, 'a') as f:
      f.write("\n")
      np.savetxt(f,x,newline=", ")


if __name__=='__main__':
     with open('../usr_input/input_config.json', 'r') as f:
       data = json.load(f)
     
     cad_seed_loc= data["seed_cad"]
     cad_configurable_parameter= data["cad_param"]
     data_file_name= '../data/'+cad_seed_loc.split('usr_input/')[1].split('.FCStd')[0]+'.csv'
     with open(data_file_name, "w") as my_empty_csv:
       pass 
     cad_obj = CAD_asset(cad_seed_loc,cad_configurable_parameter) 
            
     #print('Foam config:',data["foam_config"])
     foam_config= data["foam_config"]
     budget=  data["budget"] 
     mode= data["mode"]
     print("**Mode is:",mode)
     
     
     
     def run_cfd():
        '''
        Run CFD sim by using openFOAM and return the result [drag,lift] forces
        '''
        default_max=1e6    
        for key, value in foam_config.items():           
           if key =="meshing":
             if value=='self':
                   pass
             elif value=='auto':
                   pass

        dex_source_loc = 'rough_mesh_8cores.dex'
        print('dex source loc:', dex_source_loc)
        dex_file_editor= prepare_dexfile(dex_source_loc)
        foam_sim= run_openfoam(dex_source_loc)
    
        for key, value in foam_config.items():
           #print('Key is:',key,"value is:",value)
           if key =="meshing":
             if value=='self':
                dex_file_editor.set_dexof_parameters(data)
                result_folder=foam_sim.run()
                _result_reader_= read_results(result_folder)
                F= _result_reader_.read_force()
             elif value=='auto':
                alt_mesh=[0.5,0.4, 0.3,0.25,0.2,0.15,0.1,0.08,0.06,0.05,0.02,0.01,0.005] 
                for _mesh_ in alt_mesh:    
                    dex_file_editor.set_dexof_parameters_mesh(data,_mesh_)                    
                    result_folder=foam_sim.run()
                    _result_reader_= read_results(result_folder)
                    F= _result_reader_.read_force()
                    if (F[0]<default_max):
                       print('--> Mesh size is {} and found forces [drag,lift] are {}'.format(_mesh_,F))
                       break
                    else:
                       print('--> *Mesh size is {} and meshing failed on this mesh size!!!!!!!'.format(_mesh_)) 
        os.remove('seaglider_out.stl')
        os.remove('temp.stl')
        shutil.rmtree(result_folder)
        return F
     
     
     def run_cad_cfd(X):
        '''
        Data generation mode function : Run CAD to generate shape, create STL and 
        finally run CFD sim by using run_cfd() function
        '''
        #print("X is:",X,'variables are:',variables_to_optimize)
        cad_obj.set_parameter_by_value(variables_to_optimize,X)
        cad_obj.create_stl()
        force=run_cfd()
        #force=[1,1]
        save_data(data_file_name,np.append(X,force))
        return force
     
     
     
     def run_cad_cfd_opt_target(X):
        '''
        OPtimizer mode function: Run CAD to generate shape, create STL 
        and finally run CFD sim by using run_cfd() function
        '''
        #print("X is:",X,'variables are:',variables_to_optimize)
        print("Opt target is:",target)
        cad_obj.set_parameter_by_value(variables_to_optimize,X)
        cad_obj.create_stl()
        force=run_cfd()
        #force=[1,1]
        if target=="lift":
          out=-1*force[1]
        elif target=="drag":
          out= force[0]
        elif target=="lift_drag_ratio":
          out= -1*force[1]/force[0]
        save_data(data_file_name,np.append(X,out))
        return out
     
     if mode=="optimization":
        optimization_method= data["optimizer"]["method"]
        aq_func= data["optimizer"]["acquisition"]  
        target= data["optimizer"]["target"]

        print('optimization method is:',optimization_method,'Budget is:',budget,'Aq func:',aq_func,'opt target:',target) 
        
        bound=[]; variables_to_optimize=[]
        for key, value in data["design_space"].items():
           #print('key is:',key,'Value is:',value)
           bound.append({'name': key, 'type': 'continuous', 'domain': (value["min"],value["max"])})
           variables_to_optimize.append(key)
        print('bound is:',bound)
        
     
        
        myBopt2D = GPyOpt.methods.BayesianOptimization(f=run_cad_cfd_opt_target,
                                              domain=bound,
                                              model_type = 'GP',
                                              acquisition_type=aq_func,  normalize_Y=False, 
                                              exact_feval = True) 
                                              
        myBopt2D.run_optimization(budget,verbosity=True)
        
     elif mode=="data_generation":
       sampling_method= data["sampling_method"]
       print("-->Sampling method is:",sampling_method)
       ranges=[]; variables_to_optimize=[]
       for key, value in data["design_space"].items():
           ranges.append(value["min"]); ranges.append(value["max"])
           variables_to_optimize.append(key)
       print('--> Ranges are:',ranges,'list of variables:',variables_to_optimize)
       dim = len(variables_to_optimize)
       if sampling_method=="random":
          ds= random_sampling(dim,budget,ranges)
       elif sampling_method=="lhc_minmaxcorr":
          ds= lhc_samples_corr(dim,budget,ranges)
       elif sampling_method=="lhc_maximin":
          ds= lhc_samples_maximin(dim,budget,ranges)
       else:
         print("!!Unknown sampling method entered!!")
         sys.exit()	
       print('--> Shape of design shape is:',ds.shape[0])
       for i in range(ds.shape[0]): 
          fd=run_cad_cfd(ds[i].reshape(1,-1))	 
     elif mode=="cfd_eval":
        force=run_cfd()
        print('Drag and lift forces respectively are:',force,"Newtons")
     else:
       Print("!!Enter mode of operation is not known!!")
	
