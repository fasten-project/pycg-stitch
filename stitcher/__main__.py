import sys
import json
import argparse

from stitcher.stitcher import Stitcher
from stitcher.api import deploy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("call_graph",
        nargs="*",
        help="Paths to call graphs to be stitched together in JSON format")
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Output in simple format",
        default=False
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output path",
        default=None
    )
    parser.add_argument(
        "-a",
        "--api",
        action="store_true",
        help="Deploy the server",
        default=None
    )

    args = parser.parse_args()

    if args.api:
        deploy()
        return

    stitcher = Stitcher(args.call_graph, args.simple)
    stitcher.stitch()

    output = json.dumps(stitcher.output(), indent=2)
    if args.output:
        with open(args.output, "w+") as f:
            f.write(output)
    else:
        print (output)

if __name__ == "__main__":
    main()
