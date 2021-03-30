from stitcher.node import Node

class CallGraph:
    def __init__(self, cg):
        self.cg = cg
        self.internal_calls = []
        self.external_calls = []
        self.nodes = {}
        self.id_to_node = {}

        self.product = self.cg["product"]

        self._parse_cg()

    def get_node(self, modname, name):
        if not self.nodes.get(modname, None):
            return None
        return self.nodes[modname].get(name, None)

    def get_internal_calls(self):
        return self.internal_calls

    def get_external_calls(self):
        return self.external_calls

    def _parse_cg(self):
        def iterate_mods(d, internal):
            for mod_id, data in d.items():
                if internal:
                    mod_node = Node(mod_id, product=self.product)
                    modname = mod_node.get_modname()
                else:
                    modname = mod_id
                self.nodes[modname] = {}

                for id, info in data["namespaces"].items():
                    super_cls = None
                    if info["metadata"].get("superClasses", None) != None:
                        super_cls = []
                        for cls in info["metadata"]["superClasses"]:
                            super_cls.append(Node(cls, self.product))

                    node = Node(info["namespace"], self.product, super_cls=super_cls)

                    self.id_to_node[id] = node
                    if node.get_modname():
                        self.nodes[node.get_modname()][node.get_callable()] = node

        def iterate_calls(calls):
            res = []
            for src, dst, metadata in calls:
                if self.id_to_node.get(src, None) and self.id_to_node.get(dst, None):
                    res.append([
                        self.id_to_node.get(src),
                        self.id_to_node.get(dst)])
            return res

        iterate_mods(self.cg["modules"]["internal"], True)
        iterate_mods(self.cg["modules"]["external"], False)

        self.internal_calls = iterate_calls(self.cg["graph"]["internalCalls"])
        self.external_calls = iterate_calls(self.cg["graph"]["externalCalls"])
