import numpy as np

from ..image_enhancement.filters.border_treatment import BorderType


def handle_border(matrix: np.ndarray, border_type: BorderType):
    """
    Handles the border of the given matrix according to the given border type.

    Args:
        matrix (np.ndarray): The matrix whose border is to be handled.
        border_type (BorderType): The type of border to be used.

    Returns:
        np.ndarray: The matrix with the handled border.
    """
    if border_type == BorderType.IGNORE:
        return matrix
    elif border_type == BorderType.REPEAT:
        return np.pad(matrix, 1, mode="edge")
    elif border_type == BorderType.REFLECT:
        return np.pad(matrix, 1, mode="reflect")
    else:
        raise ValueError("Invalid border type.")


def select_region(
    matrix: np.ndarray,
    pos: tuple,
    box_size: int = 3,
    border_type: BorderType = BorderType.IGNORE,
) -> np.ndarray:
    """
    Selects a region of the given matrix centered at the given position.

    Args:
        matrix (np.ndarray): The matrix from which the region is to be selected.
        pos (tuple): The position of the center of the region.
        box_size (int): The size of the region to be selected.

    Returns:
        np.ndarray: The selected region.
    """
    if box_size % 2 == 0:
        raise ValueError("Box size must be odd.")

    matrix = handle_border(matrix, border_type)
    x, y = pos

    return np.zeros((3, 3), np.uint8)
