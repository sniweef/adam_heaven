from flask import Blueprint
import types


class BluePrintProxy(Blueprint):
    def __init__(self, real_bp, *args, **kwargs):
        assert isinstance(real_bp, Blueprint)
        self.real_bp = real_bp
        super(BluePrintProxy, self).__init__(*args, **kwargs)

    def route(self, rule, **options):
        if self.url_prefix:
            rule = self.url_prefix + rule

        return self.real_bp.route(rule, **options)

    def __getattribute__(self, item):
        attr = object.__getattribute__(self, item)

        if (isinstance(attr, types.MethodType) or isinstance(attr, types.FunctionType)) and item != 'route':
            # only proxy methods or functions
            return object.__getattribute__(self.real_bp, item)

        return attr
