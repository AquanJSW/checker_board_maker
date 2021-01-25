import argparse

from submodule.checker_board import CrossCheckerBoard

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
                    help="Number of boxes per line.",
                    )
parser.add_argument("-m", "--margin",
                    type=int, default=20,
                    help="Width of white margin(pixel).",
                    )
parser.add_argument("-o", "--output",
                    type=str, default="",
                    help="Output directory.",
                    )

if __name__ == "__main__":
    parse = parser.parse_args()

    checker = CrossCheckerBoard(screen_size=parse.screen_size,
                                screen_resolution=parse.screen_resolution,
                                n=parse.number,
                                margin=parse.margin,
                                )
    checker.write(parse.output)
