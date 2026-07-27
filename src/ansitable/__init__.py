from importlib.metadata import version, PackageNotFoundError

from .table import ANSITable, Column, Cell, ANSIMatrix, options

try:
    __version__ = version("ansitable")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = [
    "ANSITable",
    "Column",
    "Cell",
    "ANSIMatrix",
    "options",
    "__version__",
]
