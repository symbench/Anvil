###Original source of this code##
# DexOF - DEXter openfoam interface.
# Stevens Institute of Technology
# Pitz & Pochiraju
# December 13 - 2021
# Release 0.1
####################################
#Edited and modifed by Vardhan Harsh (as part of Symbench project)

import numpy as np
import stl
from stl import mesh
import math
import sys
import os
import json
import kajiki
import logging
import subprocess
import re
import argparse
from dexof_config_getsetter import *

class run_openfoam():
  """
  A class to configure and run openfoam for computational fluid dynamic analysis.

  ...

  Attributes
  ----------
  dexfile : str
         first name of the person
  
  Methods
  -------
  dex2dict(filename=""):
      Prints the person's name and age.
  """

  
  def __init__(self, dexfile):
    """
    Constructs the necessary attributes for the openfoam object.

    Parameters
    ----------
    dexfile : str, the location of dexof file 
               
    """ 
   
    self.dexfile= dexfile 
   

  def dex2dict(self,filename):
    """
    Parse the dexof file to find relevant paramters and store in dictionary

    Parameters
    ----------
    filename : str, the dexof file name (No default value, user must provide it)

    Returns
    -------
    dictionary representation of relevant dex parameters
    """

    # lame version of dex parser to extract what's needed
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    dexdict = {}
    for line in lines:
        if not line.startswith('*'):
            words = line.split(',')
            dexdict[words[0]]=words[-1]
    return dexdict

  def find_mins_maxs(self,obj):
    minx = obj.x.min()
    maxx = obj.x.max()
    miny = obj.y.min()
    maxy = obj.y.max()
    minz = obj.z.min()
    maxz = obj.z.max()
    return minx, maxx, miny, maxy, minz, maxz

  def translate(self,_solid, xt, yt, zt):
    xitems = 0, 3, 6
    yitems = 1, 4, 7
    zitems = 2, 5, 8
    # _solid.points.shape == [:, ((x, y, z), (x, y, z), (x, y, z))]
    _solid.points[:, xitems] += xt
    _solid.points[:, yitems] += yt
    _solid.points[:, zitems] += zt

  def scale(self,_solid, xs, ys, zs):
    xitems = 0, 3, 6
    yitems = 1, 4, 7
    zitems = 2, 5, 8
    # _solid.points.shape == [:, ((x, y, z), (x, y, z), (x, y, z))]
    _solid.points[:, xitems] *= xs
    _solid.points[:, yitems] *= ys
    _solid.points[:, zitems] *= zs


  def getSSTparams(self,problemdict):
    # Parameter estimates according to E R. Menter, ZONAL TWO EQUATION k-omega TURBULENCE MODELS
    # FOR AERODYNAMIC FLOWS, AIAA, 1993
    kinematic_viscosity = float(problemdict['kinematic_viscosity'])
    freestream_velocity = float(problemdict['Uinlet'])
    char_length = float(problemdict['lref'])
    domain_size = abs(float(problemdict['xmin'])) + abs(float(problemdict['xmax']))
    cell_size = max(float(problemdict['cellSizeX']), float(problemdict['cellSizeY']), float(problemdict['cellSizeZ']))
    refinement_level = min([int(n) for n in problemdict['refinementLevel'].replace('(', '').replace(')', '').split(' ')])

    beta_1 = 0.075

    Re_L = freestream_velocity * char_length / kinematic_viscosity
    cell_size_min = cell_size / 2 ** refinement_level

    # omega inlet should be between these two values
    omega_farfield_min = freestream_velocity / domain_size
    omega_farfield_max = 10 * omega_farfield_min

    # k_farfield should be between these two values
    k_farfield_min = 10 ** -5 * freestream_velocity ** 2 / Re_L
    k_farfield_max = 10 ** 4 * k_farfield_min

    omega_wall = 10 * 6 * kinematic_viscosity / (beta_1 * cell_size_min ** 2)
    # k_wall should be zero, for numerical stability set to very small value
    k_wall = 1e-10

    outdict = {}
    if 'kInlet' not in problemdict:
        outdict['kInlet'] = max(1e-10, (k_farfield_min + k_farfield_max) / 2.)
    if 'omegaInlet' not in problemdict:
        outdict['omegaInlet'] = (omega_farfield_min + omega_farfield_max) / 2.
    if 'kWall' not in problemdict:
        outdict['kWall'] = k_wall
    if 'omegaWall' not in problemdict:
        outdict['omegaWall'] = omega_wall

    return outdict





# Arg1 is the original file, arg 2 is the AOA, Arg 3 is the final file

  def stlPrep(self,configdict):
    outdict = {}
#    print("usage python stlPrep.py orig.stl aoa_degrees final.stl ")
    infile = configdict['infile']
    aoa = float(configdict['aoa'])
    outfile = configdict['outfile']
    scalex = float(configdict['scalex'])
    scaley = float(configdict['scaley'])
    scalez = float(configdict['scalez'])
    print('present working dir:',os.getcwd(),'Infile is:',infile)
    your_mesh = mesh.Mesh.from_file(infile)
    # decrease loglevel
    your_mesh.logger.setLevel(logging.ERROR)

    volume, cog, inertia = your_mesh.get_mass_properties()
    # print("Volume                                  = {0}".format(volume))
    # print("Position of the center of gravity (COG) = {0}".format(cog))
    # print("Inertia matrix at expressed at the COG  = {0}".format(inertia[0,:]))
    # print("                                          {0}".format(inertia[1,:]))
    # print("                                          {0}".format(inertia[2,:]))
    # print("Bounding Box")
    # print (find_mins_maxs(your_mesh))

    # scale and translate the mesh
    self.translate(your_mesh,-cog[0],-cog[1],-cog[2])
    self.scale(your_mesh,scalex,scaley,scalez)

    your_mesh.save("temp.stl", mode=stl.Mode.ASCII)
    # calculate projected areas at 0deg AOA
    if 'aref_lift' not in configdict:
        cmd = "parea -xz -stl " + "temp.stl"
        outpa = os.popen(cmd).read()
        print("****outpa:",outpa)
        # print(lref)
        aref_lift = float(outpa.split(":")[1])
        outdict['aref_lift'] = aref_lift

    if 'aref_drag' not in configdict:
        cmd = "parea -yz -stl " + "temp.stl"
        outpa = os.popen(cmd).read()
        print("^^^^outpa:",outpa, 'splitted outpa:',outpa.split(":"))
        aref_drag = float(outpa.split(":")[1])
        outdict['aref_drag'] = aref_drag

    volume, cog, inertia = your_mesh.get_mass_properties()
    # print("Volume                                  = {0}".format(volume))
    # print("Position of the center of gravity (COG) = {0}".format(cog))
    # print("Inertia matrix at expressed at the COG  = {0}".format(inertia[0,:]))
    # print("                                          {0}".format(inertia[1,:]))
    # print("                                          {0}".format(inertia[2,:]))
    # print("Bounding Box")
    # print (find_mins_maxs(your_mesh))
    minx, maxx, miny, maxy, minz, maxz = self.find_mins_maxs(your_mesh)
    bbox = [minx,maxx,miny,maxy,minz,maxz]

    if 'lref' not in configdict:
        lref = maxx-minx
        outdict['lref'] = lref

    # rotate the mesh
    your_mesh.rotate([0,0,1],math.radians(float(aoa)))

    # save the mesh
    your_mesh.save(outfile, mode=stl.Mode.ASCII)

    outdict.update({'outfile':outfile,'volume':volume,
        'cog':cog,'inertia':inertia,'boundingbox':bbox})
    return outdict

  def kajiki_it(self,templfile,outfile,problemdict):
    with open(templfile) as templ:
        data=templ.read()
    #print('data is:',data)
    Template = kajiki.TextTemplate(data)
    outlines = Template(problemdict).render()
    with open(outfile,'w') as outfile:
        outfile.write(outlines)
    return outlines

  def computational_domain(self,problemdict):
    bb = problemdict['boundingbox']
    xlength = bb[1]-bb[0]
    ylength = bb[3]-bb[2]
    zlength = bb[5]-bb[4]
    #
    DomainSizeXFront = float(problemdict['DomainSizeXFront'])
    DomainSizeXBack = float(problemdict['DomainSizeXBack'])
    xmin = -xlength*DomainSizeXFront
    xmax = xlength*DomainSizeXBack
    #
    DomainSizeYTop= float(problemdict['DomainSizeYTop'])
    DomainSizeYBot = float(problemdict['DomainSizeYBot'])
    ymin = -ylength*DomainSizeYTop
    ymax = ylength*DomainSizeYBot
    #
    DomainSizeZLeft = float(problemdict['DomainSizeZLeft'])
    DomainSizeZRight = float(problemdict['DomainSizeZRight'])
    zmin = -zlength*DomainSizeZLeft
    zmax = zlength*DomainSizeZRight
    # set up domain grid
    nxgrid = int((xmax-xmin)/float(problemdict['cellSizeX']))
    nygrid = int((ymax-ymin)/float(problemdict['cellSizeY']))
    nzgrid = int((zmax-zmin)/float(problemdict['cellSizeZ']))
    #
    xlocinside = xmax - 0.01*(xmax-xmin)
    ylocinside = ymax - 0.01*(ymax-ymin)
    zlocinside = zmax - 0.01*(zmax-zmin)

    return {'xmin':xmin, 'xmax':xmax,
            'ymin':ymin,'ymax':ymax,'zmin':zmin,'zmax':zmax,
            'nxgrid':nxgrid,'nygrid':nygrid,'nzgrid':nzgrid,
            'xlocinside':xlocinside,'ylocinside':ylocinside,'zlocinside':zlocinside}


# Run stl2ascii on this.
  def setup_of(self,problemdict):
    # check if casefolder exists if not create it.
    casefolder = problemdict['current_dir']+"/OF_default_casefolder"
    if 'casefoldername' in problemdict:
        casefolder = problemdict['current_dir']+"/"+problemdict['casefoldername']
    if not os.path.exists(casefolder):
        os.makedirs(casefolder)
    else:
        print("Warning: Casefolder already exists, files will be overwritten")

    # create files that need to be templated
    ofcopycmd  = 'cp -r ' + problemdict['dexof_path']+"/ofTemplate/* " + casefolder
    print("Copying::",ofcopycmd)
    #os.system('cp -r ofTemplate/* '+ casefolder)
    os.system(ofcopycmd)
    # move stl file into the casefolder
    outfile = problemdict['current_dir']+"/"+problemdict['outfile']
    stlmovecmd = 'cp '+outfile+' ' + casefolder+'/constant/triSurface/UUV.stl'
    os.system(stlmovecmd)
    # First copy the STL File in the right place
    templatesdict={'0.orig/k_templ.txt':'0.orig/k','0.orig/omega_templ.txt':'0.orig/omega','0.orig/U_templ.txt':'0.orig/U',
    'system/blockMeshDict_templ.txt': 'system/blockMeshDict','system/decomposeParDict.6_templ.txt': 'system/decomposeParDict.6',
    'system/snappyHexMeshDict_templ.txt':'system/snappyHexMeshDict',
    'system/forceCoeffs_templ.txt':'system/forceCoeffs','system/fvSolution_templ.txt':'system/fvSolution',
                   'system/controlDict_templ.txt':'system/controlDict', 'system/forceCoeffs_templ.txt':'system/forceCoeffs',
                   'constant/transportProperties_templ.txt':'constant/transportProperties'}
    for key in templatesdict:
        #print('Key is:',key)
        self.kajiki_it(casefolder+"/"+key,casefolder+"/"+templatesdict[key],problemdict)
    # write input definition json into the casefolder
    with open(casefolder+"/problem_def.json", "w") as outfile:
        keys_values = problemdict.items()
        new_d = {str(key): str(value) for key, value in keys_values}
        json.dump(new_d, outfile,indent=4)
    print("Case folder (%s) has been created " % casefolder)
    print("Problem definition %s/problem_def.json is written into the case folder"%casefolder)
    return casefolder



  def run(self):
    dexof_path = os.path.dirname(os.path.realpath(__file__))
    print("Path: ",dexof_path)
    current_dir = os.path.abspath(os.getcwd())

    # dex file is postional 0
    configdict = self.dex2dict(self.dexfile)
    configdict['dexof_path'] = dexof_path
    configdict['current_dir']= current_dir

    problemdict = self.stlPrep(configdict)
    problemdict.update(configdict)
    problemdict.update(self.computational_domain(problemdict))

    if 'refinementLevel' not in problemdict:
     print('WARNING - The mesh surface refinement level is not specified. Default values of (5 7) will be used.')
     problemdict['refinementLevel'] = '(5 7)'

    # calculate turbulence properties
    problemdict.update(self.getSSTparams(problemdict))
    case_folder=self.setup_of(problemdict)
    print("**** ALL DONE ****")
    # do the overwrite.
    cfd_dir= os.getcwd()
    os.chdir(case_folder)
    print('present working dir:',os.getcwd())
    subprocess.run('./Allclean')
    print('cleaning done')
    sim_out = subprocess.run('./Allrun', capture_output=True, text=True)


    logfile= 'simulation_log.log'
    with open(logfile, 'w') as f:
     f.write(sim_out.stdout)
 
    print("*****Postprocessing***")

    simple_foam=case_folder+'/log.simpleFoam'

    cmd='''
    echo "*** Results ***" >> results.log
    echo " ----- LIFT AND DRAG FORCES ---- " >> results.log
    tail -13 log.simpleFoam |head -8 >> results.log
    echo " ----- LIFT AND DRAG COEFFICIENTS ---- " >> results.log
    tail -50 log.simpleFoam | grep "Cd       :" |tail -1 >> results.log
    tail -50 log.simpleFoam | grep "Cl       :" |head -1 >> results.log
    tail -50 log.simpleFoam | grep "Cs       :" |head -1 >> results.log
    '''
    subprocess.check_output(cmd, shell=True)
    os.chdir(cfd_dir)
    return case_folder


class prepare_dexfile(getset_dex_file):
    def __init__(self,dexfile_loc):
        super().__init__(dexfile_loc)
    
    def set_dexof_parameters(self,config_data):
       for key, value in config_data["foam_config"].items():
           print("--> key is:",key,"values is:",value)
           if key =="meshing":
             if value=='self':
               self.setall_mesh(config_data["foam_config"]["meshsize"])
           elif key=="meshsize":
               continue
           else:
             method_name= 'set_'+str(key)
             method=getattr(self,method_name)
             method(value)
       with open(self.filename, 'w') as f:
           f.write(self.contents)
   
    def set_dexof_parameters_mesh(self,config_data,mesh):
       for key, value in config_data["foam_config"].items():
           print("--> key is:",key,"values is:",value)
           if key =="meshing":
              if value=='auto':
                self.setall_mesh(mesh)
           elif key=="meshsize":
               continue
           else:
             method_name= 'set_'+str(key)
             method=getattr(self,method_name)
             method(value)
       with open(self.filename, 'w') as f:
           f.write(self.contents)

 
   
        
class read_results():
     def __init__(self,directory):
          self.default_max=1e6
          self.result_dir= directory
     
     def read_force(self):
       try:
         #reading results from folder
         src_resultfile=self.result_dir+'/results.log'
         with open(src_resultfile, 'r') as f:
           result_output=f.read()
    
         F_out= re.search(r"Total\s+:\s*-*\(\s*\d*\.\d*\s*-*\d*\.\d*",result_output) 
         print('forces are:', F_out)
         if F_out: 
           F_found = F_out.group(0).split(': (')[1].split(" ")
           print('List of forces:',F_found)
           drag=float(F_found[0]); lift= float(F_found[1])
           
         else: 
           drag= self.default_max; lift= self.default_max
         if drag==0: 
           drag= self.default_max; lift= self.default_max
         return [drag,lift]
       except:
         print("!An exception occurred- Missing result file!") 





if __name__ == "__main__":
    default_max=1e6
    with open('input_config.json', 'r') as f:
      data = json.load(f)
    
    for key, value in data["foam_config"].items():
           if key =="meshing":
             if value=='self':
                   pass
             elif value=='auto':
                   pass
             #to do : add convergence based adaptive meshing ---- if we need mesh-independent result
 
    parser = argparse.ArgumentParser(description="CFD simulation using openFoam")
    parser.add_argument("-d","--dexfile", type=str, default='rough_mesh_8cores.dex',help="dex of config file location")
    #parser.add_argument("-s","--stl", type=str, default='seaglider.stl', help="stl file location")
    args = parser.parse_args()    
    dex_source_loc = args.dexfile
    print('dex source loc:', dex_source_loc)
    dex_file_editor= prepare_dexfile(dex_source_loc)
    foam_sim= run_openfoam(dex_source_loc)
    
    for key, value in data["foam_config"].items():
           if key =="meshing":
             if value=='self':
                dex_file_editor.set_dexof_parameters(data)
                result_folder=foam_sim.run()
                _result_reader_= read_results(result_folder)
                F= _result_reader_.read_force()
             elif value=='auto':
                alt_mesh=[0.5,0.4, 0.3,0.25,0.2,0.15,0.1,0.08,0.06,0.05,0.02,0.01,0.005] 
                for _mesh_ in alt_mesh:
                    print('mesh is:',_mesh_)       
                    dex_file_editor.set_dexof_parameters_mesh(data,_mesh_)                    
                    result_folder=foam_sim.run()
                    _result_reader_= read_results(result_folder)
                    F= _result_reader_.read_force()
                    print('mesh size is {} and found drag force is {}'.format(_mesh_,Fd))
                    if (F[0]<default_max):
                       break

             #to do : add convergence based adaptive meshing ---- if we need mesh-independent result
   
