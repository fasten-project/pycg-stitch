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
    def __init__(self, call_graph_paths, simple):
        self.simple = simple
        self.cgs = {}
        self.id_cnt = 0
        self.node_to_id = {}
        self.stitched = {
            "edges": [],
            "nodes": {}
        }

        self.nodes_cnt = 0
        self.edges_cnt = 0
        self.resolved_cnt = 0
        self.edges_cnt_no_builtin = 0

        self._parse_cgs(call_graph_paths)

    def stitch(self):
        for product, cg in self.cgs.items():
            internal_calls = cg.get_internal_calls()
            external_calls = cg.get_external_calls()
            self.edges_cnt += len(internal_calls) + len(external_calls)
            self.edges_cnt_no_builtin += len(internal_calls) + len(external_calls)
            self.resolved_cnt += len(internal_calls)

            for src, dst in internal_calls:
                self._assign_id(src.to_string(self.simple))
                self._assign_id(dst.to_string(self.simple))
                self.stitched["edges"].append([
                    self.node_to_id[src.to_string(self.simple)],
                    self.node_to_id[dst.to_string(self.simple)],
                ])

            for src, dst in external_calls:
                if ".builtin" in dst.to_string():
                    self.edges_cnt_no_builtin -= 1
                for resolved in self._resolve(dst):
                    self.resolved_cnt += 1
                    self._assign_id(src.to_string(self.simple))
                    self._assign_id(resolved.to_string(self.simple))
                    self.stitched["edges"].append([
                        self.node_to_id[src.to_string(self.simple)],
                        self.node_to_id[resolved.to_string(self.simple)],
                    ])

        self.nodes_cnt = self.id_cnt
        for node, id in self.node_to_id.items():
            self.stitched["nodes"][id] = {"URI": node, "metadata": {}}

    def output(self):
        return self.stitched

    def _parse_cgs(self, paths):
        for p in paths:
            with open(p, "r") as f:
                cg = json.load(f)
                if self.cgs.get(cg["product"], None):
                    continue

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
                            yield fn
            elif actual.is_func or actual.is_class:
                yield actual

    def _resolve_mro(self, product, modname, cls, name):
        if not self.cgs.get(product, None):
            return None

        node = self.cgs[product].get_node(modname, cls)

        resolved = None
        for parent in node.get_class_hier():
            if parent.get_product() == product:
                resolved = self.cgs[product].get_node(
                    parent.get_modname(),
                    parent.get_callable() + "." + name)
            else:
                for parent_resolved in self._resolve(parent, search_parents=False):
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
