import sys
import os
import pathlib
import shutil
import subprocess as sp

def download(pkg_name):
    print ("Downloading {} and its dependencies".format(pkg_name))
    opts = ["pip3", "download", pkg_name]
    cmd = sp.Popen(opts, stdout=sp.PIPE, stderr=sp.PIPE)
    return cmd.communicate()

def unzip_files():
    print ("Extracting source code from .whl files")
    # currently only supports whl files
    files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f) and f.endswith(".whl")]
    for f in files:
        splitted = f.split("-")
        name = splitted[0]
        version = splitted[1]
        new_dir = os.path.join(os.getcwd(), name+"-"+version)
        os.mkdir(new_dir)

        opts = ["unzip", f, "-d", new_dir]
        cmd = sp.Popen(opts, stdout=sp.PIPE, stderr=sp.PIPE)
        cmd.communicate()

    for f in files:
        os.remove(f)

def generate_call_graphs():
    packages = [f for f in os.listdir(os.getcwd()) if os.path.isdir(f)]
    cg_dir = "call-graphs"
    if not os.path.exists(cg_dir):
        os.mkdir(cg_dir)

    for pkg in packages:
        print ("Generating call graph for {}...".format(pkg))
        files = [f.as_posix() for f in pathlib.Path(pkg).glob('**/*.py')]
        tmp_name = "tmp.json"
        sp.run(["pycg",
                "--fasten",
                "--product", pkg.split("-")[0],
                "--version", pkg.split("-")[1],
                "--forge", "PyPI",
                "--max-iter", "3",
                "--package", pkg] + files + [
                "--output", tmp_name])
        if os.path.exists(tmp_name):
            sp.run(["python3", "convert.py", tmp_name, os.path.join(cg_dir, pkg + ".json")])
            os.remove(tmp_name)
        else:
            print ("Call graph generation for package {} failed".format(pkg))

    print ("Cleaning up downloaded source code")
    for pkg in packages:
        shutil.rmtree(pkg)

    print ("Done! Call graphs are stored in {}".format(cg_dir))

def main():
    if len(sys.argv) < 2:
        print ("Usage: collect.py package_name")
        sys.exit(1)

    pkg_name = sys.argv[1]
    download(pkg_name)
    unzip_files()
    generate_call_graphs()

if __name__ == "__main__":
    main()
