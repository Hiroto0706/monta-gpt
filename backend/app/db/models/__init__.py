import os
import pkgutil
import importlib

package_dir = os.path.dirname(__file__)

__all__ = []

# ディレクトリ内のすべてのモジュールを探索
for module_loader, name, ispkg in pkgutil.iter_modules([package_dir]):
    if not name.startswith("_"):
        module = importlib.import_module("." + name, package=__name__)
        class_name = "".join(word.capitalize() for word in name.split("_"))
        model_class = getattr(module, class_name, None)
        if model_class:
            globals()[class_name] = model_class
            __all__.append(class_name)
