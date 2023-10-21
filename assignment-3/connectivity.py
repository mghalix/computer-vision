import cv2
import numpy as np
from utils import *


class Pixel:
    ...


class Connectivity:
    def __init__(self, matrix: np.array, connectivity_set: np.array) -> None:
        self.matrix = matrix
        self.connectivity_set = connectivity_set

    def nd(self, i, j):
        if i == 0:
            pass

        if j == 0:
            pass

        if j == self.matrix.shape[1] - 1:
            pass

        if i == self.matrix.shape[0] - 1:
            pass

        neighbors = [
            (x - 1, y - 1),
            (x - 1, y + 1),
            (x + 1, y + 1),
            (x + 1, y - 1),
        ]

    def n4(self):
        # x, y = 3, 3
        for row in range(self.matrix.shape[0]):
            for col in range(self.matrix.shape[1]):
                if self.matrix[row, col] == 1
                neighbors = []

    def n8(self):
        return self.n4() + self.nd()


img = np.array(
    [
        [0, 0, 200, 200, 0, 0],
        [0, 200, 200, 201, 0, 0],
        [0, 0, 0, 199, 199, 0],
        [199, 200, 200, 198, 199, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 199, 199, 200],
        [0, 0, 0, 201, 201, 199],
    ]
)
connectivity_set = np.array([198, 199, 200, 201])

Connectivity(img, connectivity_set).n4()
