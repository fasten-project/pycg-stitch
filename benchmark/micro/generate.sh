#! /bin/bash

function generate()
{
    pycg --fasten --product $1 --version "1.0" --forge "PyPI" --timestamp $(date +%s) --package packages/$1 $(find packages/$1 -type f -name "*.py") --output "tmp.json"
    python3 convert.py tmp.json call-graphs/$1.json
    rm tmp.json
}

generate "root"
generate "dep1"
generate "dep2"
generate "trans-dep1"
generate "trans-dep2"
