"""Color conversion and normalization utilities for skin region analysis."""

import cv2
import numpy as np


def convert_rgb_to_lab(rgb_array: np.ndarray) -> np.ndarray:
    """
    Converts an RGB image array or matrix to CIELAB and normalizes 
    it to standard CIE L*a*b* float ranges.

    :param rgb_array: NumPy array of shape (H, W, 3) or (N, 3) with RGB values (0-255)
    :return: NumPy array of float32 values in standard CIE L*a*b* ranges:
             - L* in [0, 100]
             - a* in [-128, 127]
             - b* in [-128, 127]
    """
    # Ensure correct array shape for OpenCV conversion (needs 3D array: H x W x 3)
    is_flat = False
    if rgb_array.ndim == 2:
        is_flat = True
        rgb_array = rgb_array.reshape(1, -1, 3)

    # Ensure array format is uint8
    if rgb_array.dtype != np.uint8:
        rgb_array = np.clip(rgb_array, 0, 255).astype(np.uint8)

    # OpenCV RGB to LAB conversion
    lab_uint8 = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2LAB)

    # Scale and normalize OpenCV uint8 values to standard CIE L*a*b* float ranges
    lab_float = lab_uint8.astype(np.float32)
    lab_float[:, :, 0] = lab_float[:, :, 0] * (100.0 / 255.0)  # L* scaled to [0, 100]
    lab_float[:, :, 1] = lab_float[:, :, 1] - 128.0            # a* shifted to [-128, 127]
    lab_float[:, :, 2] = lab_float[:, :, 2] - 128.0            # b* shifted to [-128, 127]

    # Return to flat shape if input was 2D list of pixels
    if is_flat:
        return lab_float.reshape(-1, 3)

    return lab_float