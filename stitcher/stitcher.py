#
# Copyright (c) 2018-2021 FASTEN.
#
# This file is part of FASTEN
# (see https://www.fasten-project.eu/).
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import sys
import json

from stitcher.cg import CallGraph

class Stitcher:
    def __init__(self, call_graph_paths):
        self.cgs = {}
        self.id_cnt = 0
        self.node_to_id = {}
        self.stitched = {
            "edges": []
        }

        self._parse_cgs(call_graph_paths)

    def stitch(self):
        for product, cg in self.cgs.items():
            for src, dst in cg.get_internal_calls():
                self._assign_id(src.to_string())
                self._assign_id(dst.to_string())
                self.stitched["edges"].append([
                    src.to_string(),
                    dst.to_string()
                ])

            for src, dst in cg.get_external_calls():
                resolved = self._resolve(dst)
                if resolved:
                    self._assign_id(src.to_string())
                    self._assign_id(resolved.to_string())
                    self.stitched["edges"].append([
                        src.to_string(),
                        resolved.to_string()
                    ])

    def output(self):
        return self.stitched

    def _parse_cgs(self, paths):
        for p in paths:
            with open(p, "r") as f:
                cg = json.load(f)
                if self.cgs.get(cg["product"], None):
                    self._err_and_exit("Cannot stitch call graphs of the same product")
                self.cgs[cg["product"]] = CallGraph(cg)

    def _resolve(self, node, search_parents=True):
        product = node.get_product()
        callbl = node.get_callable().split(".")

        # if we don't have the call graph for that product
        # we cannot resolve any calls
        if self.cgs.get(product.replace("_", "-")):
            product = product.replace("_", "-")

        if not self.cgs.get(product):
            return None

        for i in range(1, len(callbl)):
            modname = ".".join(callbl[:i])
            fnname = ".".join(callbl[i:])

            actual = self.cgs[product].get_node(modname, fnname)

            if not actual:
                if search_parents:
                    parent_fnname = ".".join(callbl[i:-1])
                    if self.cgs[product].get_node(modname, parent_fnname):
                        fn = self._resolve_mro(product, modname, parent_fnname, callbl[-1])
                        if fn:
                            return fn
            elif actual.is_func or actual.is_class:
                return actual

        return None

    def _resolve_mro(self, product, modname, cls, name):
        if not self.cgs.get(product, None):
            return None

        node = self.cgs[product].get_node(modname, cls)

        resolved = None
        for parent in node.get_class_hier():
            if parent.get_product() == product:
                resolved = self.cgs[product].get_node(
                    parent.get_modname(),
                    parent.get_callable + "." + name)
            else:
                parent_resolved = self._resolve(parent, search_parents=False)
                if parent_resolved:
                    resolved = self.cgs[parent_resolved.get_product()].get_node(
                        parent_resolved.get_modname(),
                        parent_resolved.get_callable() + "." + name)

            if resolved:
                return resolved

        return None

    def _err_and_exit(self, msg):
        print (msg)
        sys.exit(1)

    def _assign_id(self, node_str):
        if not self.node_to_id.get(node_str, None):
            self.node_to_id[node_str] = self.id_cnt
            self.id_cnt += 1
