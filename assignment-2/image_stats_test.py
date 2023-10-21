import pytest
import numpy as np
from image_stats import ImageStatistics
from utils import images, ImageType, Utils as uti


@pytest.mark.parametrize("img_path", images)
def test_max(img_path):
    stats = ImageStatistics(img_path)
    assert stats.maximum() == np.max(stats.matrix)


@pytest.mark.parametrize("img_path", images)
def test_min(img_path):
    stats = ImageStatistics(img_path)
    assert stats.minimum() == np.min(stats.matrix)


@pytest.mark.parametrize("img_path", images)
def test_mean(img_path):
    stats = ImageStatistics(img_path)
    assert stats.mean() == np.mean(stats.matrix)


@pytest.mark.parametrize("img_path", images)
def test_std(img_path):
    stats = ImageStatistics(img_path)
    assert stats.std() == pytest.approx(np.std(stats.matrix))


@pytest.mark.parametrize("img_path", images)
def test_length(img_path):
    stats = ImageStatistics(img_path)
    assert stats.length == np.size(stats.matrix)


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        ImageStatistics("not_found.png")


@pytest.mark.parametrize("img_path", images)
def test_hist(img_path):
    stats = ImageStatistics(img_path)
    expected_output_path = f"./plots/{uti.extract_file_name(img_path)}_hist.png"
    stats.hist()
    assert uti.check_path_exists(uti.get_absolute_path(expected_output_path))


def test_hist_with_color_image():
    stats = ImageStatistics(images[0], ImageType.COLOR)
    with pytest.raises(TypeError):
        stats.hist()
