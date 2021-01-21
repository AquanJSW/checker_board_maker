import os

import matplotlib.pyplot as plt
import numpy as np


class CheckerBoard(object):
    def __init__(self,
                 screen_size: float,
                 resolution: list,
                 number: int,
                 ratio: float,
                 ):
        """

        :param screen_size: Screen size(inch).
        :param resolution: Screen resolution.
        :param number: Number of black boxes per line.
        :param ratio: Duty ratio of the width of black box.
        """
        self.__screen_size = screen_size
        self.__resolution = resolution
        self.__number = number
        self.__ratio = ratio

        self.__width_board = min(self.__resolution)

        self.__width_black_px, self.__width_interval_px \
            = self.__calc_box_width_px()

        self.__checker = self.__create_checker()

        self.__width_black_mm = self.__calc_black_width_mm()

    def get_checker(self) -> np.ndarray:
        """Get checker board."""
        return self.__checker

    def __calc_box_width_px(self) -> (int, int):
        """Calculate box width(pixel).

        :return: (width of black box, width of interval).
        """
        width_black = self.__ratio * self.__width_board \
                      / (self.__number - self.__ratio + 1)
        width_interval = (1 - self.__ratio) * width_black / self.__ratio

        return int(width_black), int(width_interval)

    def __calc_start(self, n: int) -> int:
        return (self.__width_black_px + self.__width_interval_px) * n

    def __calc_end(self, n: int) -> int:
        return self.__calc_start(n) + self.__width_interval_px

    def __create_checker(self) -> np.ndarray:
        """Create a checker board.

        :return: Checker board.
        """
        ret = np.ones(self.__width_board * self.__width_board, dtype=np.bool)
        ret = ret.reshape(self.__width_board, self.__width_board)

        i = 0
        for i in range(self.__number):
            start = self.__calc_start(i)
            end = self.__calc_end(i)

            ret[start: end, :] = False
            ret[:, start: end] = False
        else:
            start = self.__calc_start(i + 1)
            ret[start:, :] = False
            ret[:, start:] = False
            del i

        return ret

    def __calc_black_width_mm(self) -> float:
        """Calculate black box's width in real world.

        :return: Black box's width(mm) in real world.
        """
        return self.__width_black_px * self.__screen_size * 25.4 \
               / (1 + (max(self.__resolution) / min(self.__resolution)
                       ) ** 2
                  ) ** 0.5 \
               / min(self.__resolution)

    def write(self, path):
        name = "checker_board_s%.1f_R%dx%d_n%d_r%.1f_w%fmm.png" \
               % (self.__screen_size,
                  self.__resolution[0],
                  self.__resolution[1],
                  self.__number,
                  self.__ratio,
                  self.__width_black_mm,
                  )
        plt.imsave(fname=os.path.join(path, name),
                   arr=self.__checker,
                   cmap="binary",
                   )
