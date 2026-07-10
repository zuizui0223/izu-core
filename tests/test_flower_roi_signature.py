import io

import pytest

from channel_id.flower_roi_signature import saliency_roi_crop
from channel_id.public_visual_signature import extract_image_descriptors

pytest.importorskip("numpy")
Image = pytest.importorskip("PIL.Image")


def image_bytes(image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def test_saliency_crop_finds_bright_coloured_target():
    image = Image.new("RGB", (160, 120), "darkgreen")
    for x in range(55, 105):
        for y in range(35, 85):
            image.putpixel((x, y), (240, 220, 20))
    roi = saliency_roi_crop(image_bytes(image))
    assert roi.status == "roi_crop"
    assert roi.bbox_left <= 55
    assert roi.bbox_right >= 105
    assert roi.bbox_top <= 35
    assert roi.bbox_bottom >= 85
    descriptors = extract_image_descriptors(roi.crop_bytes)
    assert descriptors["mean_saturation"] > 0.1


def test_saliency_crop_falls_back_on_uninformative_frame():
    image = Image.new("RGB", (80, 80), "gray")
    roi = saliency_roi_crop(image_bytes(image))
    assert roi.status == "fallback_full_frame"
    assert roi.bbox_left == 0
    assert roi.bbox_top == 0
