import numpy as np


def create_checker(size: int, number: int, ratio: float) -> np.ndarray:
    """Create a checker board.

    :param size: Size of the entire checker board in pixel.
    :param number: Number of black boxes per line.
    :param ratio: Duty ratio of the width of black.

    :return: Checker board.
    """
    width_black = ratio * size / (number - ratio + 1)
    width_white = (1 - ratio) * width_black / ratio

    width_white = int(width_white)
    width_black = int(width_black)

    ret: np.ndarray = np.ones(size * size, dtype=np.bool).reshape(size, size)

    def calc_start(n: int) -> int:
        return (width_white + width_black) * n

    def calc_end(n: int) -> int:
        return calc_start(n) + width_white

    i = 0
    for i in range(number):
        start = calc_start(i)
        end = calc_end(i)

        ret[start: end, :] = False
        ret[:, start: end] = False
    else:
        start = calc_start(i + 1)
        ret[start:, :] = False
        ret[:, start:] = False
        del i

    return ret


def calc_box_width(size: float, resolution: list, number: int,
                   ratio: float) -> float:
    """Calculate black box's width in real world.

    :param size: Screen size in inch.
    :param resolution: Screen resolution.
    :param number: Number of black boxes per line.
    :param ratio: Duty ratio of the width of black.

    :return: Black box's width(mm) in real world.
    """



def wrt_checker(checker, path):
    pass
