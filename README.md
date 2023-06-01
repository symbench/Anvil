# Anvil
An open-source SciML tool for CFD-based design evaluator integrated with AI-based optimization algorithms and datageration cability for training and  surrogate modeling.

## Installation requirement:
Operating system: Ubuntu : 20.04

CFD sim: Appropriate version of openFOAM should be installed. Installation instructions of the used version can be found here:
https://develop.openfoam.com/Development/openfoam/-/wikis/precompiled/debian

Freecad: FreeCAD 0.20.1 version. FreeCAD is used to modify the shape and generate STL file from given parametric CAD seed and input parameter. Installation instructions can be found here : https://wiki.freecad.org/Installing_on_Linux

GpyOpt: https://sheffieldml.github.io/GPyOpt/

PyDoE: https://pythonhosted.org/pyDOE/

python_requires='>=3.6',

etc.

The automatic Installation script along with Docker image would be provided soon.


## Folders of interest:
### Automization:
 - This folder consist of class and method to run freecad to generate stl file on given seed design and input config parameter file.
 - Contains classes and methods that runs to simulate CFD on given input foam configuration.

#### Subfolders:
- src : Contain all the source files for running the Experiment.
- usr_input : User artifacts (parametric CAD seed design and configuration file) must be stored here. This is the only folder user need to work on.
- data : simulation data is stored. The name of data file depends upon the parametric seed design name.

For running the code: go to source file and run: python main.py

### Artifacts:
 storage of parametric cad seed design and other STL file used for experimentation in this project.

### Experiments:
 Demonstration of the tool's capability by different experiments.
 Some interesting simulations are:
 ![UUV](artifacts/images/UUV_velocity.png)
 ![cybertruck](artifacts/images/velocity.png)
 ![UAV](artifacts/images/velocity_UAV.png)
 ![USS](artifacts/images/velocity_USS.png)

 For more information about tool functioning, Please refere the wiki of this folder:  https://github.com/symbench/Anvil/wiki
