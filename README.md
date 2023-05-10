#Installtion required:
Ubuntu : 20.04

proper openFOAM version must be installed . It can be installed from here:
https://develop.openfoam.com/Development/openfoam/-/wikis/precompiled/debian

Freecad:
Must have version : FreeCAD 0.20.1 Revision. It generate STL file from given CAD seed and input configuration file.



# Anvil
An open-source automated evaluation &amp; optimization tool for FEA &amp; CFD

#FEA folder:
 - This folder consist of class and method to run freecad to generate stl file on given seed design and input config parameter file.

Usage: python cad_executor.py

 # CFD folder:
  - Contains classes and methods that runs to simulate CFD on given input config file.

Usage: python dexof.py
