#Installation requirement:
Ubuntu : 20.04

Appropriateversion of openFOAM version must be installed . It can be found here:
https://develop.openfoam.com/Development/openfoam/-/wikis/precompiled/debian

Freecad:
Must have version : FreeCAD 0.20.1 Revision. It generate STL file from given CAD seed and input configuration file.



# Anvil
An open-source automated evaluation &amp; optimization tool for FEA &amp; CFD
## Folders of interest:
### FEA:
 - This folder consist of class and method to run freecad to generate stl file on given seed design and input config parameter file.

Usage: python cad_to_stl.py

### CFD:
  - Contains classes and methods that runs to simulate CFD on given input config file.

Usage: python dexof.py

### cad_seed:
 storage of parametric cad seed design
### stl_repo:
  store the generated stl file from freeCAD.

### Experiments:
 Demonstration of the tool's capability by different experiments
