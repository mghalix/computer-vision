from enum import Enum

import numpy as np


class KernelName(Enum):
    GAUSSIAN = "gaussian"
    CIRCULAR = "circular"
    PYRAMIDAL = "pyramidal"
    CONE = "cone"


GAUSSIAN_KERNEL_3x3 = np.array([])
GAUSSIAN_KERNEL_5x5 = np.array([])

CIRCULAR_KERNEL = np.array([])
PYRAMIDAL_KERNEL = np.array([])
CONE_KERNEL = np.array([])

KERNEL_DICT = {
    KernelName.GAUSSIAN: {
        "3x3": GAUSSIAN_KERNEL_3x3,
        "5x5": GAUSSIAN_KERNEL_5x5,
    },
    KernelName.CIRCULAR: CIRCULAR_KERNEL,
    KernelName.PYRAMIDAL: PYRAMIDAL_KERNEL,
    KernelName.CONE: CONE_KERNEL,
}
