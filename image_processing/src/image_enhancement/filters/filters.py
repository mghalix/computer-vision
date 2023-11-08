from abc import ABC, abstractmethod

import numpy as np

from ...image_props.image import Image
from ...utils.image_enhancement.filters.border_treatment import (
    BorderTreatment,
    BorderType,
)
from ...utils.image_enhancement.filters.linear.kernels import KERNEL_DICT, KernelName


class Filter(ABC):
    def __init__(self, img: Image, BorderType: BorderType = BorderType.IGNORE):
        self.img = img
        self._border_type = BorderType

    @property
    def border_type(self):
        return self._border_type

    @border_type.setter
    def set_border_type(self, border_type: BorderType):
        self._border_type = border_type


class LinearFilter(Filter):
    def __init__(self, img: Image, kernel: KernelName, border_type: BorderType):
        """
        Initializes a Filters object with the given image, kernel, and border type.

        Args:
            img (Image): The input image.
            kernel (KernelName): The name of the kernel to be used for filtering.
            border_type (BorderType): The type of border to be used for filtering.

        Returns:
            None
        """
        super().__init__(img, border_type)
        self._border_type = border_type
        self._kernel_name = kernel
        self._kernel = KERNEL_DICT[kernel]

    @property
    def filter_type(self) -> str:
        return self._kernel_name.value.capitalize()

    @filter_type.setter
    def set_filter_type(self, kernel: KernelName):
        self._kernel_name = kernel
        self._kernel = KERNEL_DICT[kernel]


class NonLinearFilter(Filter):
    def __init__(
        self,
        img: Image,
    ):
        """
        Initializes a Filters object with an image and a kernel.

        Args:
            img (Image): The input image.
        """
        super().__init__(img)

    def median(self):
        pass

    def kuwahara(self):
        pass

    def _region_split(self):
        pass

    def _region_variance(self):
        pass


# class Filter:
#     @classmethod
#     def box_map(cls, matrix: np.ndarray, pos: tuple, box_size: int = 3):
#         box = np.zeros((box_size, box_size)).astype(np.uint8)
#         d = list(range(-(box_size // 2), box_size // 2 + 1))

#         for i, dx in enumerate(d):
#             for j, dy in enumerate(d):
#                 new_pos = tuple(np.add(pos, (dx, dy)))
#                 box[i, j] = matrix[new_pos]

#         return box

#     @classmethod
#     def box_average(cls, box: np.ndarray) -> np.uint8:
#         return round(np.average(box))

#     @classmethod
#     def averaging(cls, img: Image) -> Image:
#         m, n = img.resolution

#         for pos, _ in np.ndenumerate(img.matrix):
#             if 0 in pos or 1 in pos or m - 1 in pos or n - 1 in pos:
#                 continue

#             box = cls.box_map(img.matrix, pos, box_size=3)
#             img.matrix[pos] = cls.box_average(box)

#         img.update()
#         return img
