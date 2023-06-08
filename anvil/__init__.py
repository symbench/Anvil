__version__ = "0.0.1"

from anvil._logger import configure_logging
from anvil.cad import add_freecad_libs_to_path

add_freecad_libs_to_path()
configure_logging()
