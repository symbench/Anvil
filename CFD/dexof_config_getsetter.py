import re

class getset_dex_file():
    """
    python wrapper function for set or retreive dexof file
    """
    
    def __init__(self, filename):
        self.filename = filename
    
        with open(self.filename, 'r') as f:
            self.contents=f.read()    
        
    def print_dexfile(self):
        print('dex file is:\n',self.contents)
    

    def get_casefoldername(self):
       return re.split('casefoldername,input,string,',re.findall('casefoldername,input,string,.*',self.contents)[0])[1]

    def set_casefoldername(self,folder_location):
        folder_string= 'casefoldername,input,string,'+ folder_location
        self.contents=re.sub('casefoldername,input,string,.*',folder_string,self.contents)
 
    def get_maxiter(self):
       return re.split('maxiter,input,discrete,',re.findall('maxiter,input,discrete,.*',self.contents)[0])[1]

    def set_maxiter(self,iter):
        max_iter_string= 'maxiter,input,discrete,'+ str(iter)
        self.contents=re.sub('maxiter,input,discrete,.*',max_iter_string,self.contents)
    
    
    def get_infile(self):
       return re.split('infile,input,string,',re.findall('infile,input,string,.*',self.contents)[0])[1]

    def set_infile(self,infilename):
        infile_string= 'infile,input,string,'+ infilename
        self.contents=re.sub('infile,input,string,.*',infile_string,self.contents)

    
    def get_output_file(self):
       return re.split('outfile,input,string,',re.findall('outfile,input,string,.*',self.contents)[0])[1]

    def set_output_file(self,outfilename):
        outfile_string= 'outfile,input,string,'+ outfilename
        self.contents=re.sub('outfile,input,string,.*',outfile_string,self.contents)

    def get_aoa(self):
       return re.split('aoa,input,continuous,',re.findall('aoa,input,continuous,.*',self.contents)[0])[1]

    def set_aoa(self,aoa):
        aoa_string= 'aoa,input,continuous,'+ str(aoa)
        self.contents=re.sub('aoa,input,continuous,.*',aoa_string,self.contents)

    def get_Uinlet(self):
       return re.split('Uinlet,input,continuous,',re.findall('Uinlet,input,continuous,.*',self.contents)[0])[1]

    def set_Uinlet(self,uinlet):
        uin_string= 'Uinlet,input,continuous,'+ str(uinlet)
        self.contents=re.sub('Uinlet,input,continuous,.*',uin_string,self.contents)

    def get_density(self):
       return re.split('density,input,continuous,',re.findall('density,input,continuous,.*',self.contents)[0])[1]

    def set_density(self,density_f):
        dense_string= 'density,input,continuous,'+ str(density_f)
        self.contents=re.sub('density,input,continuous,.*',dense_string,self.contents)
        
    
    def get_kinematic_viscosity(self):
       return re.split('kinematic_viscosity,input,continuous,',re.findall('kinematic_viscosity,input,continuous,.*',self.contents)[0])[1]

    def set_kinematic_viscosity(self,kin_visc):
        kvisc_string= 'kinematic_viscosity,input,continuous,'+ str(kin_visc)
        self.contents=re.sub('kinematic_viscosity,input,continuous,.*',kvisc_string,self.contents)

    def get_kInlet(self):
       return re.split('kInlet,input,continous,',re.findall('kInlet,input,continous,.*',self.contents)[0])[1]

    def set_kInlet(self,kinlet):
        kin_string= 'kInlet,input,continous,'+ str(kinlet)
        self.contents=re.sub('kInlet,input,continous,.*',kin_string,self.contents)
    
    def get_omegaInlet(self):
       return re.split('omegaInlet,input,continuous,',re.findall('omegaInlet,input,continuous,.*',self.contents)[0])[1]


    def set_omegaInlet(self,olet):
        oin_string= 'omegaInlet,input,continuous,'+ str(olet)
        self.contents=re.sub('omegaInlet,input,continuous,.*',oin_string,self.contents)

    def get_xmesh(self):
       return re.split('cellSizeX,input,continuous,',re.findall('cellSizeX,input,continuous,.*',self.contents)[0])[1]

    def set_xmesh(self,xmesh):
        xms_string= 'cellSizeX,input,continuous,'+ str(xmesh)
        self.contents=re.sub('cellSizeX,input,continuous,.*',xms_string,self.contents)


    def get_ymesh(self):
       return re.split('cellSizeY,input,continuous,',re.findall('cellSizeY,input,continuous,.*',self.contents)[0])[1]

    def set_ymesh(self,ymesh):
        yms_string= 'cellSizeY,input,continuous,'+ str(ymesh)
        self.contents=re.sub('cellSizeY,input,continuous,.*',yms_string,self.contents)


    def get_zmesh(self):
       return re.split('cellSizeZ,input,continuous,',re.findall('cellSizeZ,input,continuous,.*',self.contents)[0])[1]

    def set_zmesh(self,zmesh):
        zms_string= 'cellSizeZ,input,continuous,'+ str(zmesh)
        self.contents=re.sub('cellSizeZ,input,continuous,.*',zms_string,self.contents)

    def setall_mesh(self,allmesh):
        xms_string= 'cellSizeX,input,continuous,'+ str(allmesh)
        self.contents=re.sub('cellSizeX,input,continuous,.*',xms_string,self.contents)

        yms_string= 'cellSizeY,input,continuous,'+ str(allmesh)
        self.contents=re.sub('cellSizeY,input,continuous,.*',yms_string,self.contents)

        zms_string= 'cellSizeZ,input,continuous,'+ str(allmesh)
        self.contents=re.sub('cellSizeZ,input,continuous,.*',zms_string,self.contents)



 
