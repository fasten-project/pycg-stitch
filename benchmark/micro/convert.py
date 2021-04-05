import urllib.parse
import sys
import json

class CGConverter:
    """
    Converts FASTEN version 1 Call Graphs to Version 2
    """
    def __init__(self, cg):
        self.cg = cg
        self.new_cg = {
            "product": cg["product"],
            "forge": cg["forge"],
            "nodes": None,
            "generator": cg["generator"],
            "depset": cg["depset"],
            "version": cg["version"],
            "modules": {
                "internal": cg["modules"],
                "external": {}
            },
            "graph": {
                "internalCalls": [],
                "externalCalls": [],
                "resolvedCalls": []
            },
            "timestamp": cg["timestamp"],
            "sourcePath": cg.get("sourcePath", ""),
            "metadata": cg.get("metadata", {})
        }
        self.key_to_ns = {}
        self.key_to_super = {}
        self.counter = -1

    def encode(self, item):
        return urllib.parse.quote(item, safe="/().")

    def add_internal_calls(self):
        for src, dst in self.cg["graph"]["internalCalls"]:
            self.new_cg["graph"]["internalCalls"].append([str(src), str(dst), {}])

    def extract_counter(self):
        for mod in self.new_cg["modules"]["internal"].values():
            for key, value in mod["namespaces"].items():
                self.key_to_ns[int(key)] = self.encode(value["namespace"])
                self.counter = max(self.counter, int(key))

    def extract_superclasses(self):
        for key, superclasses in self.cg["cha"].items():
            scs = []
            # convert superClasses items to strings
            for item in superclasses:
                try:
                    mint = int(item)
                    scs.append(self.key_to_ns[mint])
                except ValueError:
                    scs.append(self.encode(item))
                    self.add_external(self.encode(item))
            self.key_to_super[int(key)] = scs

    def add_external(self, item):
        modname = item.split("/")[2]
        if not modname in self.new_cg["modules"]["external"]:
            self.new_cg["modules"]["external"][modname] = {
                "sourceFile": "",
                "namespaces": {}
            }

        # find out if the uri already exists
        found = False
        for k, v in self.new_cg["modules"]["external"][modname]["namespaces"].items():
            if v["namespace"] == item:
                cnt = int(k)
                found = True
                break

        if not found:
            self.counter += 1
            cnt = self.counter
            self.new_cg["modules"]["external"][modname]["namespaces"][str(cnt)] = {
                "namespace": item,
                "metadata": {}
            }

        return cnt

    def add_superclasses(self):
        for mod in self.new_cg["modules"]["internal"].values():
            for key, value in mod["namespaces"].items():
                if int(key) in self.key_to_super:
                    value["metadata"]["superClasses"] = self.key_to_super[int(key)]
                value["namespace"] = self.encode(value["namespace"])

    def add_external_calls(self):
        for src, dst in self.cg["graph"]["externalCalls"]:
            cnt = self.add_external(self.encode(dst))
            self.new_cg["graph"]["externalCalls"].append([str(src), str(cnt), {}])

    def convert(self):
        self.add_internal_calls()
        self.extract_counter()
        self.extract_superclasses()
        self.add_superclasses()
        self.add_external_calls()
        self.new_cg["nodes"] = self.counter + 1

    def output(self):
        return self.new_cg

def main():
    if len(sys.argv) < 3:
        print ("Usage: convert.py input_path output_path")
        sys.exit(1)

    in_path = sys.argv[1]
    out_path = sys.argv[2]

    with open(in_path, "r") as f:
        cg = json.load(f)

    converter = CGConverter(cg)
    converter.convert()

    with open(out_path, "w+") as f:
        f.write(json.dumps(converter.output()))


if __name__ == "__main__":
    main()
