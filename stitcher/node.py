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
class Node:
    def __init__(self, uri_str, product=None, super_cls=None, version=None):
        self.uri_str = uri_str
        self.product = product
        self.version = version
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

    def get_version(self):
        return self.version

    def get_modname(self):
        return self.modname

    def get_callable(self):
        return self.callable

    def get_class_hier(self):
        return self.super_cls

    def to_string(self, simple=False):
        uri = ""
        if not simple:
            uri += "fasten:"
        uri += "//" + "PyPI!" +self.product
        if self.version and not simple:
            uri += "$" + self.version
        uri += "/" + self.modname + "/" + self.callable

        if self.is_func:
            uri += "()"
        return uri
