import os
import sys


def _import_fem_tools():
    femtools_libs = [
        "/usr/local/Mod/Fem/femtools",
        "/usr/share/freecad/Mod/Fem/femtools",
    ]
    for lib in femtools_libs:
        if os.path.exists(lib):
            path = os.path.dirname(lib)
            if path not in sys.path:
                sys.path.append(path)
            path = os.path.abspath(os.path.join(lib, "..", ".."))
            if path not in sys.path:
                sys.path.append(path)
            path = os.path.abspath(os.path.join(lib, "..", "..", "..", "Ext"))
            if path not in sys.path:
                sys.path.append(path)
            break
    else:
        raise ValueError("femtools library was not found!")


def _import_freecad_lib():
    freecad_libs = [
        "/usr/local/lib/FreeCAD.so",
        "/usr/lib/freecad-python3/lib/FreeCAD.so",
    ]
    for lib in freecad_libs:
        if os.path.exists(lib):
            path = os.path.dirname(lib)
            if path not in sys.path:
                sys.path.append(path)
            break
    else:
        raise ValueError("FreeCAD library was not found!")


def add_freecad_libs_to_path():
    _import_freecad_lib()
    _import_fem_tools()
