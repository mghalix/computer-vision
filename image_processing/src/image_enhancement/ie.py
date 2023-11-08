from __future__ import annotations

import logging
from typing import Any

import cv2
import numpy as np

from src.utils.files.file_utils import FileUtils as uti

from ..image_props.image import Image
from ..image_props.image_stats import ImageStatistics as stats
from .filters.filters import Filter

log = logging.getLogger(__name__)


class ImageEnhancement:
    def __init__(self, img: Image) -> None:
        self.img = img
        self.filters: list[str] = []

    def filters_applied(self) -> int:
        """filters amount

        Keyword arguments:
        Return: the amount of filters applied on the image
        """

        return len(self.filters)

    def add_filter(self, filter_name):
        self.filters.append(filter_name)
        self.img.name += "_" + filter_name

    def pop_filter(self) -> None:
        x = self.img.name.split("_")[:-1]
        self.img.name = "_".join(x)

    def stretch_contrast(self, percent: int) -> ImageEnhancement:
        self.img = Contrast.stretch_contrast(self.img, percent)
        self.add_filter("contrast_stretch")

        return self

    def contract_contrast(self, percent: int) -> ImageEnhancement:
        self.img = Contrast.contract_contrast(self.img, percent)
        self.add_filter("contrast_contracted")
        return self

    def gray_level_slicing(
        self, range: tuple[np.uint8, np.uint8], boost_type: str = "up"
    ) -> ImageEnhancement:
        """
        Apply gray level slicing to the image.

        :param range: A tuple of two integers representing the range of gray levels to enhance.
        :param boost_type: A string indicating the type of boost to apply. Can be "up" or "down".
        :return: An instance of the ImageEnhancement class with the gray level slicing applied.
        Args:
            range (tuple[int, int]): The range of gray levels to enhance.
            boost_type (str, optional): The type of boost to apply. Defaults to "up".
        >>> up -> highlights
        >>> down -> darkens

        Returns:
            ImageEnhancement: The updated ImageEnhancement object.
        """
        self.img = Contrast.gray_level_slicing(self.img, range, boost_type)
        self.add_filter("gray_level_slicing")
        return self

    def bit_plane_slicing(self, plane: np.uint8) -> ImageEnhancement:
        self.img = Contrast.bit_plane_slicing(self.img, plane)
        self.add_filter("bit_plane_slicing")
        return self

    def averaging(self) -> ImageEnhancement:
        self.img = Filter.averaging(self.img)
        self.add_filter("averaged")
        return self

    def histogram_equalization(
        self, range: tuple[np.uint8, np.uint8] = (np.uint8(0), np.uint8(255))
    ) -> ImageEnhancement:
        self.img = Contrast.apply_hist_equalization(self.img, range=range)
        self.add_filter("histogram_equalized")
        return self

    def show(self) -> None:
        """Displays the image on a named window.

        Returns:
            None
        """
        name = uti.image_title(self.img.name)
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        window = cv2.getWindowImageRect(name)
        cv2.moveWindow(name, *uti.get_center_screen(window))  # bug
        cv2.imshow(name, self.img.matrix)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save_img(self) -> None:
        """Saves the filtered image to a file.

        Returns:
            None
        """
        _, extension = uti.get_basename_extension(self.img.path)
        loc = "res/filt/"
        EXPORT_DIR = uti.get_absolute_path(loc)

        uti.create_folder(EXPORT_DIR)

        img_path = EXPORT_DIR + self.img.name + extension
        log.info(f"Saving image {self.img.name} to -> {loc} 💾 ...")
        cv2.imwrite(img_path, self.img.matrix)

    def reset(self) -> ImageEnhancement:
        """Resets the image back to the original

        Return: None
        """
        self.img = Image(self.img.path, self.img.open_type)
        return self

    # A great use for this is the airport's baggage check-in conveyor which sees
    def image_negative(self) -> ImageEnhancement:
        L = self.img.levels
        for row in range(len(self.img.matrix)):
            for col in range(len(self.img.matrix[row])):
                self.img.matrix[row][col] = (L - 1) - self.img.matrix[row][col]

        self.img.update()
        flag = "negative"
        # if the previous filter was the same filter as this
        # then they're just going to cancel each other
        if self.filters_applied() and self.filters[-1] == flag:
            self.pop_filter()

        else:
            self.add_filter(flag)

        return self

    def image_subtracting(self, img: Image) -> ImageEnhancement:
        if self.img.resolution != img.resolution:
            raise TypeError(
                "Both images should be of the same resolution & scenery, and only differ in motion"
            )

        # for (row, col), _ in np.ndenumerate(img.matrix):
        #     diff = int(self.img.matrix[row, col]) - int(img.matrix[row, col])
        #     # saturated technique (like in cv2) instead of taking abs
        #     self.img.matrix[row, col] = max(0, diff)

        diff = self.img.matrix.astype(int) - img.matrix.astype(int)
        self.img.matrix = np.clip(diff, 0, 255).astype(np.uint8)

        self.img.update()
        return self


class Contrast:
    @classmethod
    # r1 > s1 & r2 < s2
    def stretch_contrast(cls, img: Image, percent: int) -> Image:
        r1, r2, s1, s2 = cls._get_r_s(img, percent, "stretch")

        for row in range(len(img.matrix)):
            for col in range(len(img.matrix[0])):
                curr = img.matrix[row][col]
                if curr <= r1:
                    img.matrix[row][col] = curr * s1 / r1

                elif curr <= r2:
                    m = (s2 - s1) / (r2 - r1)
                    img.matrix[row][col] = curr * m + s1 - r1 * m

                else:
                    L = img.levels  # 256
                    m = ((L - 1) - s2) / ((L - 1) - r2)
                    img.matrix[row][col] = (
                        curr * m + (L - 1) - (L - 1) * (L - s2) / (L - r2)
                    )

        img.update()
        return img

    # r1 < s1 & r2 > s2
    @classmethod
    def contract_contrast(cls, img: Image, percent: int) -> Image:
        r1, r2, s1, s2 = cls._get_r_s(img, percent, "contract")

        for row in range(len(img.matrix)):
            for col in range(len(img.matrix[0])):
                curr = img.matrix[row][col]
                if curr <= r1:
                    img.matrix[row][col] = curr * s1 / r1

                elif curr <= r2:
                    m = (s2 - s1) / (r2 - r1)
                    img.matrix[row][col] = curr * m + s1 - r1 * m

                else:
                    L = img.levels
                    m = ((L - 1) - s2) / ((L - 1) - r2)
                    img.matrix[row][col] = (
                        curr * m + (L - 1) - (L - 1) * (L - s2) / (L - r2)
                    )

        img.update()
        return img

    @classmethod
    def _get_r_s(
        cls, img: Image, percent: int, type: str
    ) -> tuple[float, float, float, float]:
        if type not in ["stretch", "contract"]:
            raise TypeError('Contrast manipulation type must be "stretch" or "contract')

        r1 = img.matrix.min()
        r2 = img.matrix.max()

        if type == "stretch":
            s1 = r1 - (r1 * percent / 100 % (img.levels))
            s2 = r2 - (r2 * percent / 100 % (img.levels))
        else:
            s1 = r1 + (r1 * percent / 100 % (img.levels))
            s2 = r2 + (r2 * percent / 100) % (img.levels)

        r2 = max(0.2, r2)
        r1 = max(0.1, r1)
        s1 = max(0.1, s1)
        s2 = max(0.1, s2)
        return (r1, r2, s1, s2)

    @classmethod
    def _inside_range(cls, number, range: tuple) -> bool:
        """Checks if a number is inside a given range.

        Args:
            number (int): The number to check.
            range (tuple): A tuple representing the range to check.

        Returns:
            bool: True if the number is inside the range, False otherwise.
        """
        # return number > range[0] and number < range[1]
        return range[0] < number < range[1]

    @classmethod
    def gray_level_slicing(
        cls, img: Image, range: tuple[np.uint8, np.uint8], boost_type: str = "up"
    ) -> Image:
        """Gray level slicing is used to boost a certain color in an image
        by setting all other colors to black

        Keyword arguments:
        range -- the range of colors to boost
        type -- the type of boosting, either "up" or "down"
        """
        color = 0 if boost_type == "down" else img.levels - 1
        for (row, col), pixel in np.ndenumerate(img.matrix):
            if not cls._inside_range(pixel, range):
                continue
            img.matrix[row][col] = color

        img.update()
        return img

    @classmethod
    def _plane(cls, number: np.uint8) -> np.uint8:
        """Returns the plane of a number.

        Args:
            number (int): The number to get the plane of.

        Returns:
            int: The plane of the number.
        """

        return np.bitwise_not(1 << number)
        result = ~(1 << number)

    @classmethod
    def apply_plane(cls, pixel: np.uint8, planes: list[np.uint8]) -> np.uint8:
        """Applies a mask to a pixel.

        Args:
            pixel (int): The pixel to apply the mask to.
            planes (list): A list of planes to apply to the pixel.

        Returns:
            None
        """

        for plane in planes:
            pixel &= cls._plane(plane)

        return pixel

    @classmethod
    def bit_plane_slicing(cls, img: Image, plane: np.uint8) -> Image:
        """Bit plane slicing is used to highlight a certain bit in an image
        by setting all other bits to black

        Keyword arguments:
        bit -- the bit to highlight
        """
        if plane <= 0 or plane > 8:
            raise ValueError("Bit plane must be between 1 and 8")

        planes = [np.uint8(plane) for plane in range(plane - 1, 8)]
        print(planes)
        for (row, col), pixel in np.ndenumerate(img.matrix):
            img.matrix[row][col] = cls.apply_plane(pixel, planes)

        img.update()
        return img

    @classmethod
    def full_range(cls, img: Image, range: tuple[np.uint8, np.uint8]) -> bool:
        img_range = (0, img.levels - 1)
        return img_range == range

    @classmethod
    def get_hist_dic(
        cls, img: Image, range: tuple[np.uint8, np.uint8]
    ) -> dict[int, dict[str, (int | float)]]:
        m, n = img.resolution
        res = m * n
        L = img.levels

        # in case it was in_range
        min_val = max_val = delta = 0

        full_range = cls.full_range(img, range)

        if not full_range:
            min_val, max_val = range
            delta = max_val - min_val

        hist_dic: dict = {}
        for _, pixel in np.ndenumerate(img.matrix):
            if not full_range and (pixel < min_val or pixel > max_val):
                continue

            if pixel not in hist_dic:
                prob = 1 / res
                hist_dic[pixel] = {
                    "count": 1,
                    "probability": prob,
                    "cumulative": prob,
                    "lcumulative": (L - 1) * prob,
                    "new_gray": (
                        np.uint8(
                            ((L - 1) * prob) if full_range else (min_val + prob * delta)
                        )
                    ),
                }
                continue

            hist_dic[pixel]["count"] += 1
            prob = hist_dic[pixel]["count"] / res
            hist_dic[pixel]["probability"] = prob
            hist_dic[pixel]["cumulative"] += prob
            hist_dic[pixel]["lcumulative"] = (L - 1) * hist_dic[pixel]["cumulative"]
            hist_dic[pixel]["new_gray"] = np.uint8(
                ((L - 1) * hist_dic[pixel]["cumulative"])
                if full_range
                else (min_val + hist_dic[pixel]["cumulative"] * delta)
            )

        return hist_dic

    @classmethod
    def apply_hist_equalization(
        cls, img: Image, range: tuple[np.uint8, np.uint8]
    ) -> Image:
        hist_dic = cls.get_hist_dic(img, range)
        for (row, col), pixel in np.ndenumerate(img.matrix):
            try:
                img.matrix[row][col] = hist_dic[pixel]["new_gray"]
            except KeyError:
                pass

        img.update()
        return img
