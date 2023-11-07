import logging
from math import sqrt

import cv2
import matplotlib.pyplot as plt

from src.image_props.image import Image
from src.utils.image_utils import ImageUtils as uti

log = logging.getLogger(__name__)


class ImageStatistics:
    def __init__(self, img: Image) -> None:
        self.img = img
        self.length = len(img.matrix) * len(img.matrix[0])

    def sum(self) -> int:
        sum = 0
        for row in self.img.matrix:
            for col in row:
                sum += col

        return sum

    def mean(self) -> float:
        return self.sum() / self.length

    def variance(self) -> float:
        m = self.mean()

        sum = 0
        for row in self.img.matrix:
            for col in row:
                sum += (col - m) ** 2

        return sum / self.length

    def std(self) -> float:
        return sqrt(self.variance())

    def minimum(self) -> int:
        min_pixel = self.img.matrix[0][0]
        for row in self.img.matrix:
            for col in row:
                min_pixel = min(col, min_pixel)

        return min_pixel

    def maximum(self) -> int:
        max_pixel = self.img.matrix[0][0]
        for row in self.img.matrix:
            for col in row:
                max_pixel = max(col, max_pixel)

        return max_pixel

    def _hist(self):
        if self.img.open_type in [uti.ImageType.COLOR, uti.ImageType.UNCHANGED]:
            raise TypeError(
                "Cannot create histogram of color image, Not yet implemented."
            )

        hist = cv2.calcHist([self.img.cv], [0], None, [256], [0, 256])
        plt.figure(uti.image_title(self.img.name))
        plt.title("Grayscale Histogram")
        plt.xlabel("Pixel Value")
        plt.ylabel("Frequency")
        plt.plot(hist, color="black")
        plt.xlim([0, 256])
        return plt

    def save_hist(self) -> None:
        """
        Saves the histogram of the image to a file in the 'res/plt/' directory.
        """
        hist_dir = uti.create_folder("res/plt/")
        _, extension = uti.get_basename_extension(self.img.path)
        add_on = "_hist"
        hist_path = hist_dir + self.img.name + add_on + extension
        log.info(f"Saving histogram {self.img.name}{add_on} to -> {hist_dir} 💾 ...")
        self._hist().savefig(hist_path, format=extension[1:])

    def show_hist(self) -> None:
        """
        Displays the histogram of the image.
        """
        self._hist().show()
