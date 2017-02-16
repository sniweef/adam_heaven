from flask import Blueprint


class RecursiveBluePrint(Blueprint):
    def __init__(self, parent, *args, **kwargs):
        super(RecursiveBluePrint, self).__init__(*args, **kwargs)
        assert isinstance(parent, Blueprint)
        self.parent = parent

    def route(self, rule, **options):
        if self.url_prefix:
            rule = self.url_prefix + rule

        return self.parent.route(rule, **options)
