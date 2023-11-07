from math import sqrt

import cv2
import matplotlib.pyplot as plt
import numpy as np

from utils import *


class ImageStatistics:
    def __init__(
        self, img_path: str, open_type: ImageType = ImageType.GRAYSCALE
    ) -> None:
        self.img_path = img_path
        self.open_type = open_type
        self.img = cv2.imread(img_path, self.open_type.value)
        if self.img is None:
            raise FileNotFoundError(f"Image not found: {img_path}")
        self.matrix = np.array(self.img)
        self.length = len(self.matrix) * len(self.matrix[0])

    def mean(self) -> float:
        sum = 0
        for row in self.matrix:
            for col in row:
                sum += col

        return sum / self.length

    def variance(self) -> float:
        m = self.mean()

        sum = 0
        for row in self.matrix:
            for col in row:
                sum += (col - m) ** 2

        return sum / self.length

    def std(self) -> float:
        return sqrt(self.variance())

    def minimum(self) -> int:
        mini = self.matrix[0][0]
        for row in self.matrix:
            for col in row:
                mini = min(col, mini)

        return mini

    def maximum(self) -> int:
        maxi = self.matrix[0][0]
        for row in self.matrix:
            for col in row:
                maxi = max(col, maxi)

        return maxi

    def hist(self) -> None:
        if self.open_type in [ImageType.COLOR, ImageType.UNCHANGED]:
            raise TypeError(
                "Cannot create histogram of color image, Not yet implemented."
            )

        hist = cv2.calcHist([self.img], [0], None, [256], [0, 256])
        plt.figure()
        # plt.title("Grayscale Histogram")
        # plt.xlabel("Pixel Value")
        # plt.ylabel("Frequency")
        # plt.plot(hist, color="black")
        # plt.xlim([0, 256])
        # hist_path = f"./plots/{Utils.extract_file_name(self.img_path)}_hist.png"
        # plt.savefig(hist_path, format="png")
        # print(f"Histogram figured saved successfully to {hist_path}")


def main():
    stats = ImageStatistics(images[2], ImageType.GRAYSCALE)
    stats.hist()


if __name__ == "__main__":
    main()
