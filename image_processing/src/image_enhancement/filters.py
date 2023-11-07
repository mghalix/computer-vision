import numpy as np

from ..image_props.image import Image


class Filter:
    @classmethod
    def box_map(cls, matrix: np.ndarray, pos: tuple, box_size: int = 3):
        box = np.zeros((box_size, box_size)).astype(np.uint8)
        d = list(range(-(box_size // 2), box_size // 2 + 1))

        for i, dx in enumerate(d):
            for j, dy in enumerate(d):
                new_pos = tuple(np.add(pos, (dx, dy)))
                box[i, j] = matrix[new_pos]

        return box

    @classmethod
    def box_average(cls, box: np.ndarray) -> np.uint8:
        return round(np.average(box))

    @classmethod
    def averaging(cls, img: Image) -> Image:
        m, n = img.resolution

        for pos, _ in np.ndenumerate(img.matrix):
            if 0 in pos or 1 in pos or m - 1 in pos or n - 1 in pos:
                continue

            box = cls.box_map(img.matrix, pos, box_size=3)
            img.matrix[pos] = cls.box_average(box)

        img.update()
        return img


class BorderTreatment:
    def ignore(self):
        """That is to copy the borders pixels as to the enhanced matrix"""

        ...

    def repeat(self):
        """Consider as if the images continue the last row /column without changes"""
        ...

    def reflect(self):
        """Mirror The row/column across boarder"""
        ...
