convergence_data=[]

def listOfTuples(l1, l2):
    return list(map(lambda x, y:(x,y), l1, l2))

def capture_datumerror(crush_pressure,thickness_d,radius_d,length_d):
    try: 
     vessel.set_pressure(crush_pressure)
     vessel.set('thickness', thickness_d)
     vessel.set('radius', radius_d)
     vessel.set('length', length_d)
     return 0
    except:
     print("Something went wrong in setting value")
     return 1

def check_convergence(predictions,ml,experiment_id):
    if len(predictions)<window_len :
        return False
    else: 
       windowed_prediction = predictions[-window_len:]
       windowed_ml = ml[-window_len:]
       print('windowed result is:',windowed_prediction)
       mean_w=statistics.mean(windowed_prediction)
       prediction_np=np.array(windowed_prediction)
       mad= 0.2*np.sum(np.abs(prediction_np-mean_w))
       print('*MAD is :',mad,'mean is:',mean_w,'mad/mean is:',(mad/mean_w)) 
       if (mad/mean_w)>threshold:
          return False
       else:
          return True
    
def check_convergence_by_majority(predictions,ml,experiment_id):
    if len(predictions)<window_len :
        return False
    else:
      a = predictions[-window_len:]
      diff_array=[]
      for i in range(len(a)):
        for j in range(len(a)):
          if i!=j:
             diff=abs(a[i]-a[j])
             diff_array.append(diff)
      diff_np=np.array(diff_array)
      broken_list=np.array_split(diff_np, 5)       
      for k in range(len(broken_list)):
        #print('list is',broken_list[k],'comparison value is:',0.02*a[k])
        truth= np.less_equal(broken_list[k],0.02*np.ones_like(broken_list[k])*a[k])
        #print('truth is:',truth)
        num_of_approx_equals=np.sum(truth)
        #print(num_of_approx_equals)
        if num_of_approx_equals<3:
          return False
        else:
          return True


mesh_options=np.arange(0.001,0.2,0.004)[::-1]
print('mesh option is :',mesh_options)


skipped=[]

mesh_options=[0.3,0.2,0.1,0.08,0.05,0.04,0.035,0.030,0.025,0.020,0.01,0.005]

for i in range(design_set.shape[0]):
     start=time.time()
     experiment_id=design_set[i][0]
     length_d= design_set[i][1] *0.001 
     radius_d= design_set[i][2]/2 *0.001 
     thickness_d= design_set[i][3] *0.001 
     depth= design_set[i][4] 
     
        
     crush_pressure= rhog_safety*depth*0.000001
     print('---> Exp indx:',experiment_id,'depth is:',depth,'length is:',length_d,'thickness is:',thickness_d, 'radius is:',radius_d,'cp:',crush_pressure )
    
     de=capture_datumerror(crush_pressure,thickness_d,radius_d,length_d)
     vessel.set_exp_index(experiment_id)
     predicted_vonmises=[]; mesh_lengths=[]
     if de==0:
      k=0 
      for j in range(len(mesh_options)):
        #step=np.random.randint(2)
        ml= mesh_options[j]
        #print('\n ml is:',ml,'.|')
        vessel.set('mesh_length', ml)
        try:
          k=vessel.run_gmsh()                #k =1 : create mesh error, k=0: No error
        except RuntimeError:
          break
        if k==0:
         nodes=vessel.get_node_count()
         print('nodes are:',nodes)
         if nodes >150000:
            break
         k=vessel.run_fem_analysis()        #k =1 : fem analysis error, k=0: No error
         print('experiment id is:',i,',k is:',k, ',ml is:',ml)
        if k==0:  
            mesh_lengths.append(ml)
            predicted_vonmises.append(vessel.get_vonmises_stress())
            print('predicted vonmises is:',predicted_vonmises)
            #convergence1=check_convergence(predicted_vonmises,mesh_lengths,experiment_id)
            #convergence2=    (predicted_vonmises,mesh_lengths,experiment_id)
            #convergence= convergence1 or convergence2
            convergence=True
                        
            if convergence==True: 
             end_time=time.time()
             sim_time=end_time-start
             vessel.set_sim_time(sim_time)    
             vessel.csv_write_row(csvwriter)
            
            
vessel.csv_close_output(csvwriter)



 def sketch_set_length(self, param: str, value: float):
        """
        Sets a length constraint of the sketch object in meters. This method
        may throw an exception if an internal constraint cannot be satisfied.
        """
        obj = self.doc.getObject('Sketch')
        obj.setDatum(param, Units.Quantity(
            value * 1e3, Units.Unit('mm')))

    def sketch_get_length(self, param: str) -> float:
        obj = self.doc.getObject('Sketch')
        return obj.getDatum(param).getValueAs('mm') * 1e-3

    def set_pressure(self, value: float):
        """
        Sets the outside pressure acting on the vessel in mega pascals.
        """
        obj = self.doc.getObject('ConstraintPressure')
        obj.Pressure = float(value)

    def get_pressure(self) -> float:
        obj = self.doc.getObject('ConstraintPressure')
        return float(obj.Pressure)

    def set_mesh_length(self, value: float):
        """
        Sets the maximum edge length for the meshing algorithm in meters.
        """
        obj = self.doc.getObject('FEMMeshGmsh')
        obj.CharacteristicLengthMax = Units.Quantity(
            value * 1e3, Units.Unit('mm'))

    def get_mesh_length(self) -> float:
        obj = self.doc.getObject('FEMMeshGmsh')
        return obj.CharacteristicLengthMax.getValueAs('mm') * 1e-3

    def set_youngs_modulus(self, value: float):
        """
        Sets the Youngs modulus of the material in mega pascals.
        """
        obj = self.doc.getObject('MaterialSolid')
        mat = dict(obj.Material)
        mat['YoungsModulus'] = str(value) + ' MPa'
        obj.Material = mat

    def get_youngs_modulus(self) -> float:
        obj = self.doc.getObject('MaterialSolid')
        return Units.Quantity(obj.Material['YoungsModulus']).getValueAs('MPa')

    def set_poisson_ratio(self, value: float):
        """
        Sets the poisson ratio of the material.
        """
        obj = self.doc.getObject('MaterialSolid')
        mat = dict(obj.Material)
        mat['PoissonRatio'] = str(value)
        obj.Material = mat

    def get_poisson_ratio(self):
        obj = self.doc.getObject('MaterialSolid')
        return float(obj.Material['PoissonRatio'])

    def set_tensile_strength(self, value: float):
        """
        Sets the ultimate tensile strength of the material in mega pascals.
        """
        obj = self.doc.getObject('MaterialSolid')
        mat = dict(obj.Material)
        mat['UltimateTensileStrength'] = str(value) + ' MPa'
        obj.Material = mat

    def get_tensile_strength(self) -> float:
        obj = self.doc.getObject('MaterialSolid')
        return Units.Quantity(obj.Material['UltimateTensileStrength']).getValueAs('MPa')

    def set_density(self, value: float):
        """
        Sets the density of the material in kg/m3.
        """
        obj = self.doc.getObject('MaterialSolid')
        mat = dict(obj.Material)
        mat['Density'] = str(value) + ' kg/m^3'
        obj.Material = mat

    def get_density(self):
        obj = self.doc.getObject('MaterialSolid')
        return float(Units.Quantity(obj.Material['Density']).getValueAs('kg/m^3'))



 def run_analysis(self):
        """
        Set the various parameters, then call this method and query the results.
        """
        self.clean()
        self.doc.recompute()
        self.print_info()
        
        if self.debug:
            print("Running GMSH mesher ...", end=' ', flush=True)
        mesher = GmshTools(self.doc.getObject('FEMMeshGmsh'))
        err = mesher.create_mesh()
        #print('err is:',type(err))
        if err:
            #raise ValueError(err)
            return 0
        obj = self.doc.getObject('FEMMeshGmsh').FemMesh
        if self.debug:
            print(obj.NodeCount, "nodes,",
                  obj.EdgeCount, "edges,",
                  obj.FaceCount, "faces,",
                  obj.VolumeCount, "volumes")

        if self.debug:
            print("Running FEM analysis ...", end=' ', flush=True)
        fea = FemToolsCcx(
            self.doc.getObject('Analysis'),
            self.doc.getObject('SolverCcxTools'))
        fea.purge_results()
        fea.update_objects()
        fea.setup_working_dir()
        fea.setup_ccx()
        err = fea.check_prerequisites()
        if err:
            #raise ValueError("FEM error: " + err)
            return 1
        fea.write_inp_file()
        fea.ccx_run()
        fea.load_results()
        obj = self.doc.getObject('CCX_Results')
        assert obj.ResultType == 'Fem::ResultMechanical'
        if self.debug:
            print("vonMises stress: {:.2f} MPa".format(max(obj.vonMises)))
        return 2

    def has_mesh_properties(self):
        obj = self.doc.getObject('FEMMeshGmsh').FemMesh
        return True if obj and obj.NodeCount else False

    def get_node_count(self):
        obj = self.doc.getObject('FEMMeshGmsh').FemMesh
        return obj.NodeCount

    def get_edge_count(self):
        obj = self.doc.getObject('FEMMeshGmsh').FemMesh
        return obj.EdgeCount

    def get_face_count(self):
        obj = self.doc.getObject('FEMMeshGmsh').FemMesh
        return obj.FaceCount

    def get_volume_count(self):
        obj = self.doc.getObject('FEMMeshGmsh').FemMesh
        return obj.VolumeCount

    def has_fem_properties(self):
        obj = self.doc.getObject('CCX_Results')
        return True if obj else False

    def get_vonmises_stress(self) -> float:
        """
        Returns the maximum vonMises stress in mega pascals.
        """
        obj = self.doc.getObject('CCX_Results')
        return max(obj.vonMises)

    def get_tresca_stress(self) -> float:
        """
        Returns the maximum tresca (shear) stress in mega pascals.
        """
        obj = self.doc.getObject('CCX_Results')
        return max(obj.MaxShear)

    def get_max_displacement(self) -> float:
        """
        Returns the maximum displacement in meters.
        """
        obj = self.doc.getObject('CCX_Results')
        return max(obj.DisplacementLengths) * 1e-3

    def get_has_failed(self) -> bool:
        """
        Returns if the maximum vonMises stress is larger than the tensile strength.
        """
        return self.get_vonmises_stress() >= self.get_tensile_strength()
    
