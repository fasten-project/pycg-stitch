# Stiching for FASTEN Python Call Graphs

This tool stitches Python
call graphs written in Python produced by [PyCG](https://github.com/vitsalis/PyCG.git) in the Fasten Format.

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

