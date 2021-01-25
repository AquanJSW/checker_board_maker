import os

import matplotlib.pyplot as plt
import numpy as np


def calc_box_width_mm(screen_size: float,
                      screen_resolution: list,
                      box_width_px: int,
                      ) -> float:
    """Calculate box's width(mm) in real world.

    :param screen_size: Screen size(inch).
    :param screen_resolution: Screen resolution.
    :param box_width_px: Box's width(pixel).

    :return: Box's width(mm) in real world.
    """
    return box_width_px * screen_size * 25.4 \
           / (1 + (max(screen_resolution) / min(screen_resolution)
                   ) ** 2
              ) ** 0.5 \
           / min(screen_resolution)


class SparseCheckerBoard(object):
    def __init__(self,
                 screen_size: float,
                 screen_resolution: list,
                 number: int,
                 ratio: float,
                 ):
        """

        :param screen_size: Screen size(inch).
        :param screen_resolution: Screen resolution.
        :param number: Number of black boxes per line.
        :param ratio: Duty ratio of the width of black box.
        """
        self.__screen_size = screen_size
        self.__resolution = screen_resolution
        self.__number = number
        self.__ratio = ratio

        self.__width_board = min(self.__resolution)

        self.__width_black_px, self.__width_interval_px \
            = self.__calc_box_width_px()

        self.__checker = self.__create_checker()

        self.__width_black_mm \
            = calc_box_width_mm(screen_size=screen_size,
                                screen_resolution=screen_resolution,
                                box_width_px=self.__width_black_px)

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
        ret = np.ones(self.__width_board * self.__width_board,
                      dtype=np.bool
                      ).reshape(self.__width_board, -1)

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


class CrossCheckerBoard(object):
    def __init__(self,
                 screen_size: float,
                 screen_resolution: list,
                 n: int,
                 margin: int,
                 ):
        """

        :param screen_size: Screen size(inch).
        :param screen_resolution: Screen resolution.
        :param n: The number of boxes per line.
        :param margin: White margin width(pixel).
        """
        self.__scr_sz = screen_size
        self.__scr_res = screen_resolution
        self.__n = n
        self.__margin = margin

        self.__checker_board = self.__create_checker_board()

        self.__box_width_mm = \
            calc_box_width_mm(screen_size=screen_size,
                              screen_resolution=screen_resolution,
                              box_width_px=self.__box_width_px)

    def __create_checker_board(self) -> np.ndarray:
        """Create a checker board."""
        ret = np.zeros(shape=min(self.__scr_res) ** 2,
                       dtype=bool,
                       ).reshape(min(self.__scr_res), -1
                                 )
        obj: np.ndarray = ret[self.__margin: -self.__margin,
                              self.__margin: -self.__margin
                              ]
        self.__box_width_px = int(obj.shape[0] / self.__n)

        for c in range(self.__n):
            for r in range(self.__n):
                if (c % 2) ^ (r % 2):
                    continue
                obj[self.__box_width_px * r: self.__box_width_px * (1 + r),
                    self.__box_width_px * c: self.__box_width_px * (1 + c),
                    ] = True
        return ret

    def write(self, directory: str):
        """Save checker board as an image."""
        name = "cross_checker_board_s%.1f_R%dx%d_n%d_m%d_w%f.jpg" \
               % (self.__scr_sz,
                  self.__scr_res[0],
                  self.__scr_res[1],
                  self.__n,
                  self.__margin,
                  self.__box_width_mm,
                  )
        plt.imsave(fname=os.path.join(directory, name),
                   arr=self.__checker_board,
                   cmap="binary",
                   )
