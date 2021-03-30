class Node:
    def __init__(self, uri_str, product=None, super_cls=None):
        self.uri_str = uri_str
        self.product = product
        self.super_cls = super_cls or []

        if len(uri_str.split("/")) == 5:
            self.internal = False
            self.external = True
        else:
            self.internal = True
            self.external = False

        self.modname = self.callable = ""

        splitted = self.uri_str.split("/")
        if self.internal:
            self.modname = splitted[1]
            self.callable = splitted[2]
        else:
            self.product = splitted[2]
            self.callable = splitted[4]

        self.is_class = super_cls != None
        self.is_func = False
        if self.callable.endswith("()"):
            self.is_func = True
            self.callable = self.callable[:-2]

    def get_product(self):
        return self.product

    def get_modname(self):
        return self.modname

    def get_callable(self):
        return self.callable

    def get_class_hier(self):
        return self.super_cls

    def to_string(self):
        uri = "//" + self.product + "/" + self.modname + "/" + self.callable
        if self.is_func:
            uri += "()"
        return uri
