import argparse

from submodule.checker_board import SparseCheckerBoard

parser = argparse.ArgumentParser(description="Creat a checker board for "
                                             "camera calibration.",
                                 )

parser.add_argument("--screen_size",
                    type=float, default=23.8,
                    help="Screen size, ie. 23.8.",
                    )
parser.add_argument("--screen_resolution",
                    type=int, default=[1080, 1920], nargs=2,
                    help="Screen ratio, ie. 1080 1920.",
                    )
parser.add_argument("-n", "--number",
                    type=int, default=8,
                    help="Number of black boxes per line.",
                    )
parser.add_argument("-r", "--ratio",
                    type=float, default=0.6,
                    help="Duty ratio of the width of black, ie. 0.8.",
                    )
parser.add_argument("-o", "--output",
                    type=str, default="",
                    help="Output path.",
                    )

if __name__ == "__main__":
    parse = parser.parse_args()

    checker = SparseCheckerBoard(screen_size=parse.screen_size,
                                 screen_resolution=parse.screen_resolution,
                                 number=parse.number,
                                 ratio=parse.ratio,
                                 )
    checker.write(parse.output)
