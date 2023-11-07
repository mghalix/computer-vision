import numpy as np
import pytest

from src.image_props.image import Image
from src.image_props.image_stats import ImageStatistics
from src.utils.image_utils import ImageUtils as uti


@pytest.mark.parametrize("img_path", uti.sample_images.values())
def test_max(img_path):
    stats = ImageStatistics(Image(img_path))
    assert stats.maximum() == np.max(stats.img.matrix)


@pytest.mark.parametrize("img_path", uti.sample_images.values())
def test_min(img_path):
    stats = ImageStatistics(Image(img_path))
    assert stats.minimum() == np.min(stats.img.matrix)


@pytest.mark.parametrize("img_path", uti.sample_images.values())
def test_mean(img_path):
    stats = ImageStatistics(Image(img_path))
    assert stats.mean() == np.mean(stats.img.matrix)


@pytest.mark.parametrize("img_path", uti.sample_images.values())
def test_std(img_path):
    stats = ImageStatistics(Image(img_path))
    assert np.allclose(stats.std(), np.std(stats.img.matrix))


@pytest.mark.parametrize("img_path", uti.sample_images.values())
def test_length(img_path):
    stats = ImageStatistics(Image(img_path))
    assert stats.length == np.size(stats.img.matrix)


@pytest.mark.parametrize("img_path", uti.sample_images.values())
def test_hist(img_path):
    stats = ImageStatistics(Image(img_path))
    basename, extension = uti.get_basename_extension(img_path)
    expected_output_path = f"./res/plt/{basename}_hist{extension}"
    stats.save_hist()
    assert uti.check_path_exists(uti.get_absolute_path(expected_output_path))


def test_hist_with_color_image():
    stats = ImageStatistics(Image(uti.sample_images["dog"], uti.ImageType.COLOR))
    with pytest.raises(TypeError):
        stats.show_hist()
