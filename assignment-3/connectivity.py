import cv2
import numpy as np
from utils import *


class Pixel:
    ...


class Connectivity:
    def __init__(self, matrix: np.ndarray, connectivity_set: np.ndarray) -> None:
        self.matrix = matrix
        self.connectivity_set = connectivity_set

    def nd(self):
        # if i == 0:
        #     pass

        # if j == 0:
        #     pass

        # if j == self.matrix.shape[1] - 1:
        #     pass

        # if i == self.matrix.shape[0] - 1:
        #     pass

        # neighbors = [
        #     (x - 1, y - 1),
        #     (x - 1, y + 1),
        #     (x + 1, y + 1),
        #     (x + 1, y - 1),
        # ]
        return np.ndarray([])

    def n4(self):
        # x, y = 3, 3
        row_length, col_length = self.matrix.shape
        label = 1
        neighbors = {}

        for row in range(row_length):
            for col in range(col_length):
                pixel = self.matrix[row, col]

                if pixel not in self.connectivity_set:
                    continue

                if row == 0 and col == 0:  # top-left corner
                    # (x+1, y)
                    neighbors[f"lbl{label}"] = [pixel]

                # elif row == 0 and col == col_length - 1:  # top-right corner
                #     # (x-1, y)
                #     ...

                elif row == 0:
                    # (x-1, y)
                    if self.matrix[row, col - 1] in self.connectivity_set:
                        neighbors[f"lbl{label}"] += [pixel]
                    else:
                        label += 1
                        neighbors[f"lbl{label}"] = [pixel]

                elif row == row_length - 1 and col == 0:  # bottom-left corner
                    # (x+1, y) & (x, y-1)
                    ...

                elif (
                    row == row_length - 1 and col == col_length - 1
                ):  # bottom-right corner
                    # (x-1, y) & (x, y-1)
                    ...

                    ...

                elif row == row_length - 1:
                    # (x+1, y) & (x-1, y) & (x, y-1)
                    ...

                elif col == 0:
                    # (x+1, y) & (x, y-1)
                    ...

                elif col == col_length - 1:
                    # (x-1, y) & (x, y-1)
                    ...

                else:
                    label += 1
                    neighbors[f"lbl{label}"] = [pixel]

        return neighbors

    def n8(self):
        return self.n4() + self.nd()


def main():
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

    print(Connectivity(img, connectivity_set).n4())


if __name__ == "__main__":
    main()
