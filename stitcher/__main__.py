import sys
import json
import argparse

from stitcher.stitcher import Stitcher

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("call_graph",
        nargs="*",
        help="Paths to call graphs to be stitched together in JSON format")
    parser.add_argument(
        "-o",
        "--output",
        help="Output path",
        default=None
    )

    args = parser.parse_args()

    stitcher = Stitcher(args.call_graph)
    stitcher.stitch()

    output = json.dumps(stitcher.output())
    if args.output:
        with open(args.output, "w+") as f:
            f.write(output)
    else:
        print (output)

if __name__ == "__main__":
    main()
