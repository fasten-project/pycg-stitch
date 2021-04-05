# Stiching for FASTEN Python Call Graphs

In this repository you can find the implementation of a stitcher for Python
call graphs written in Python along with a benchmark to test its functionality.

Contents:
* [stitcher](stitcher): The source code for the stitcher.
* [benchmark](benchmark): A minimal benchmark to test the stitcher's
  functionality.

## Installation

Installation requires an installation of Python3.
From the root directory, run:
```
>>> python3 setup.py install
```

## Usage

```
>>> pycg-stitch --help
usage: pycg-stitch [-h] [-o OUTPUT] [call_graph ...]

positional arguments:
  call_graph            Paths to call graphs to be stitched together in JSON format

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output path
```

* `call_graph`: A list of paths containing FASTEN Python call graphs in JSON
  format.
* `output`: (Optional) parameter specifying where the stitched call graph will
  be stored.


## Benchmark

The benchmark directory consists of a micro- and a macro-benchmark.

### Micro-benchmark

The micro-benchmark is stored under `benchmark/micro` and contains the
following:

* `packages`: Contains the source code of 5 packages. Specifically it contains
  the source code of a `root` package which depends on the `dep1` and `dep2`
  packages. In turn, `dep1` depends on the `trans-dep1` and `trans-dep2`
  packages.
* `call-graphs`: Contains [PyCG](https://github.com/vitsalis/pycg) generated
  call graphs for the aforementioned packages.
* `convert.py`: Converts call graphs of the [version
  1](https://github.com/fasten-project/fasten/wiki/Revision-Call-Graph-format#version-1-1)
  FASTEN Python format to [version
  2](https://github.com/fasten-project/fasten/wiki/Revision-Call-Graph-format#version-2-1).
* `generate.sh`: Script that uses `PyCG` to generate Python call graphs, and
  store them under the `call-graphs` directory.

In order to execute the benchmark:

```
>>> pycg-stitch benchmark/micro/call-graphs/* --output out.json
```

The `out.json` file should contain the following output:

```
{
  "edges": [
    [
      "//dep1/dep1.dep1/Cls.dep_fn()",
      "//trans-dep2/trans_dep2.trans_dep2/smth()"
    ],
    [
      "//root/root.root/",
      "//root/root.root/A.fn()"
    ],
    [
      "//root/root.root/",
      "//root/root.root/func2()"
    ],
    [
      "//root/root.root/",
      "//trans-dep1/trans_dep1.trans_dep1/ClsPar.__init__()"
    ],
    [
      "//root/root.root/A.fn()",
      "//dep1/dep1.dep1/Cls.dep_fn()"
    ],
    [
      "//root/root.root/func2()",
      "//dep2/dep2.dep2/func()"
    ],
    [
      "//trans-dep1/trans_dep1.trans_dep1/ClsPar.__init__()",
      "//trans-dep1/trans_dep1.trans_dep1/fun()"
    ]
  ]
}
```

### Macro-benchmark

The macro-benchmark is stored under the `benchmark/macro` directory. It contains
the call graphs for the [fabric](https://github.com/fabric/fabric) package and
its dependencies. The macro-benchmark contains the following items:

* `call-graphs`: The call-graphs for fabric and its dependencies.
* `collect.py`: A Python script that takes as a parameter a package and
  downloads it along with its dependencies. Then it generates their call graphs
  using PyCG and stores them under the `call-graphs` directory.
* `stitched.json`: The expected stitched call graph for fabric and its
  dependencies.
