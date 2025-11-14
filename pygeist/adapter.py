from pygeist.exceptions import AdapterNotCompiled


try:
    from . import _adapter
except (ModuleNotFoundError, ImportError):
    raise AdapterNotCompiled('build the adapter to use it')
