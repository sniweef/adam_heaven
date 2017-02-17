import os
import importlib
import re
from libs.logger import logger


class SourceScanner(object):
    def __init__(self, rel_source_dir, pattern):
        self.base_dir = os.curdir
        assert rel_source_dir and pattern
        assert not rel_source_dir.startswith('..')
        self.rel_source_dir = rel_source_dir
        self.pattern = re.compile(pattern)

    @staticmethod
    def can_be_module(path):
        return os.path.isdir(path) and '__init__.py' in os.listdir(path)

    def apply_scanned_function(self, *args, **kwargs):
        module_objs = []
        for filename in os.listdir(self.rel_source_dir):
            if filename.startswith('.'):
                continue

            dir_path = os.path.join(self.rel_source_dir, filename) if self.rel_source_dir != '.' else filename
            if not SourceScanner.can_be_module(dir_path):
                continue

            module_name = re.sub(r'/|\\', '.', dir_path)
            try:
                module = importlib.import_module(module_name)
                module_objs.append(module)
                logger.info('Import module: {}'.format(module_name))
            except ImportError:
                logger.warn('Name {} is not a module'.format(module_name))

        import inspect
        for module in module_objs:
            all_functions = inspect.getmembers(module, inspect.isfunction)
            logger.debug('Functions: {}'.format(all_functions))

            for func_name, func in all_functions:
                matcher = self.pattern.match(func_name)
                if matcher:
                    result = func(*args, **kwargs)
                    yield (result, ) + matcher.groups()
