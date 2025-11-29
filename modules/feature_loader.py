"""Dynamic feature loader for plug-and-play modules."""
import os, importlib

def load_module(module_path):
    # module_path like 'modules.some_feature'
    try:
        mod = importlib.import_module(module_path)
        return mod
    except Exception:
        return None
