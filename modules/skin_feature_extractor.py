"""Build raw per-pixel RGB/LAB patch payloads and feature vectors from skin extraction output."""

from __future__ import annotations

import base64
import logging
from typing import Any

import cv2
import numpy as np

from modules.skin_color_converter import convert_rgb_to_lab
from modules.skin_image_processor import (
    FEATURE_KEYS,
    STANDARD_PATCH_SIZE,
    TOTAL_PATCH_PIXELS,
    extract_patch_pixel_matrices,
)

logger = logging.getLogger(__name__)

REGION_NAMES: list[str] = ["forehead", "left_cheek", "right_cheek", "chin"]


def decode_patch_from_base64(patch_base64: str) -> np.ndarray:
    """Decode a base64-encoded PNG patch into a BGR numpy array."""
    buffer = np.frombuffer(base64.b64decode(patch_base64), dtype=np.uint8)
    patch = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
    if patch is None:
        raise ValueError("Failed to decode patch image from base64.")
    return patch


def calculate_mean_lab_features(region_patches: dict[str, dict[str, Any]]) -> dict[str, float]:
    """
    Calculates the overall global mean L*, a*, b* values across all valid regions.
    """
    all_lab_pixels = []

    for region_name, patch_data in region_patches.items():
        if "lab_pixels" in patch_data:
            all_lab_pixels.extend(patch_data["lab_pixels"])

    if not all_lab_pixels:
        raise ValueError("No valid LAB pixel matrices found to calculate skin features.")

    lab_array = np.array(all_lab_pixels, dtype=np.float32)  # Shape: (N, 3)
    mean_l, mean_a, mean_b = np.mean(lab_array, axis=0)

    return {
        "mean_L": round(float(mean_l), 4),
        "mean_a": round(float(mean_a), 4),
        "mean_b": round(float(mean_b), 4),
    }


# def calculate_24d_feature_vector(
#     region_patches: dict[str, dict[str, Any]],
# ) -> dict[str, Any]:
#     """
#     Extracts a 24-dimensional feature vector containing Mean and Standard Deviation (std)
#     for L*, a*, b* channels across the 4 skin regions:
#     [forehead, left_cheek, right_cheek, chin].

#     Returns a structured dictionary with both a keyed dictionary and a flat 24D vector.
#     """
#     feature_dict: dict[str, float] = {}
#     feature_vector: list[float] = []

#     for region_name in REGION_NAMES:
#         patch_data = region_patches.get(region_name, {})
#         lab_pixels = patch_data.get("lab_pixels", [])

#         if lab_pixels:
#             lab_arr = np.array(lab_pixels, dtype=np.float64)  # Shape: (225, 3)
#             means = np.mean(lab_arr, axis=0)
#             stds = np.std(lab_arr, axis=0)

#             m_l, m_a, m_b = round(float(means[0]), 4), round(float(means[1]), 4), round(float(means[2]), 4)
#             s_l, s_a, s_b = round(float(stds[0]), 4), round(float(stds[1]), 4), round(float(stds[2]), 4)
#         else:
#             # Fallback if a region failed or is missing
#             m_l, m_a, m_b = 0.0, 0.0, 0.0
#             s_l, s_a, s_b = 0.0, 0.0, 0.0

#         feature_dict[f"{region_name}_mean_L"] = m_l
#         feature_dict[f"{region_name}_mean_a"] = m_a
#         feature_dict[f"{region_name}_mean_b"] = m_b
#         feature_dict[f"{region_name}_std_L"] = s_l
#         feature_dict[f"{region_name}_std_a"] = s_a
#         feature_dict[f"{region_name}_std_b"] = s_b

#         feature_vector.extend([m_l, m_a, m_b, s_l, s_a, s_b])

#     return {
#         "features": feature_dict,
#         "feature_vector": feature_vector,  # 24-element float list
#     }
def calculate_24d_feature_vector(
    region_patches: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Extracts a 24-dimensional feature vector, imputing data for missing regions."""
    feature_dict: dict[str, float] = {}
    feature_vector: list[float] = []

    # First pass: gather valid means/stds to calculate an overall face average
    valid_means, valid_stds = [], []
    for region_name in REGION_NAMES:
        lab_pixels = region_patches.get(region_name, {}).get("lab_pixels", [])
        if lab_pixels:
            lab_arr = np.array(lab_pixels, dtype=np.float64)
            valid_means.append(np.mean(lab_arr, axis=0))
            valid_stds.append(np.std(lab_arr, axis=0))

    # Calculate fallback values using the average of valid facial regions
    fallback_mean = np.mean(valid_means, axis=0) if valid_means else [0.0, 0.0, 0.0]
    fallback_std = np.mean(valid_stds, axis=0) if valid_stds else [0.0, 0.0, 0.0]

    for region_name in REGION_NAMES:
        lab_pixels = region_patches.get(region_name, {}).get("lab_pixels", [])

        if lab_pixels:
            lab_arr = np.array(lab_pixels, dtype=np.float64)
            means = np.mean(lab_arr, axis=0)
            stds = np.std(lab_arr, axis=0)
        else:
            # Impute missing regions (like an occluded chin) with face averages
            means = fallback_mean
            stds = fallback_std

        m_l, m_a, m_b = round(float(means[0]), 4), round(float(means[1]), 4), round(float(means[2]), 4)
        s_l, s_a, s_b = round(float(stds[0]), 4), round(float(stds[1]), 4), round(float(stds[2]), 4)

        feature_dict[f"{region_name}_mean_L"] = m_l
        feature_dict[f"{region_name}_mean_a"] = m_a
        feature_dict[f"{region_name}_mean_b"] = m_b
        feature_dict[f"{region_name}_std_L"] = s_l
        feature_dict[f"{region_name}_std_a"] = s_a
        feature_dict[f"{region_name}_std_b"] = s_b

        feature_vector.extend([m_l, m_a, m_b, s_l, s_a, s_b])

    return {
        "features": feature_dict,
        "feature_vector": feature_vector, 
    }


# def build_region_patches_payload(
#     extraction: dict[str, Any],
#     patch_size: int = STANDARD_PATCH_SIZE,
# ) -> dict[str, dict[str, Any]]:
#     """
#     Convert extracted skin regions into 15x15 (225-pixel) RGB/LAB matrices.
#     """
#     regions = extraction.get("regions", {})
#     region_patches: dict[str, dict[str, Any]] = {}

#     for region_name in REGION_NAMES:
#         region = regions.get(region_name)
#         if not region or region.get("status") == "error":
#             continue

#         patch_base64 = region.get("patch_base64")
#         if not patch_base64:
#             continue

#         patch_bgr = decode_patch_from_base64(patch_base64)
#         patch_rgb = cv2.cvtColor(patch_bgr, cv2.COLOR_BGR2RGB)
#         patch_lab = convert_rgb_to_lab(patch_rgb)

#         matrix_payload = extract_patch_pixel_matrices(
#             patch_bgr,
#             patch_size=patch_size,
#         )

#         matrix_payload["lab_pixels"] = patch_lab.reshape(-1, 3).tolist()
#         region_patches[region_name] = matrix_payload

#     return region_patches
def build_region_patches_payload(
    extraction: dict[str, Any],
    patch_size: int = STANDARD_PATCH_SIZE,
) -> dict[str, dict[str, Any]]:
    """Convert extracted skin regions into 15x15 (225-pixel) RGB/LAB matrices."""
    regions = extraction.get("regions", {})
    region_patches: dict[str, dict[str, Any]] = {}

    for region_name in REGION_NAMES:
        region = regions.get(region_name)
        # Skip regions flagged as errors or invalid skin
        if not region or region.get("status") == "error" or region.get("quality_status") == "invalid_skin_region":
            continue

        patch_base64 = region.get("patch_base64")
        if not patch_base64:
            continue

        patch_bgr = decode_patch_from_base64(patch_base64)
        
        # REMOVED duplicate conversions. extract_patch_pixel_matrices does it all.
        matrix_payload = extract_patch_pixel_matrices(
            patch_bgr,
            patch_size=patch_size,
        )

        region_patches[region_name] = matrix_payload

    return region_patches


def build_regions_metadata(extraction: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Return lightweight region metadata (bbox/center/status) without patch images."""
    metadata: dict[str, dict[str, Any]] = {}

    for region_name in REGION_NAMES:
        region = extraction.get("regions", {}).get(region_name)
        if not region:
            continue

        metadata[region_name] = {
            "status": region.get("status"),
            "center_x": region.get("center_x"),
            "center_y": region.get("center_y"),
            "bbox": region.get("bbox"),
            "landmark_indices": region.get("landmark_indices"),
        }

    return metadata


def build_pixel_patch_response(
    extraction: dict[str, Any],
    patch_size: int = STANDARD_PATCH_SIZE,
) -> dict[str, Any]:
    """Assemble the standard raw pixel-matrix API payload with skin features."""
    region_patches = build_region_patches_payload(extraction, patch_size=patch_size)

    if not region_patches:
        raise ValueError("No valid skin region patches available for pixel extraction.")

    # 1. Global Mean Features
    global_skin_features = calculate_mean_lab_features(region_patches)

    # 2. 24D Regional (Mean + Std) Feature Extraction
    features_24d = calculate_24d_feature_vector(region_patches)

    return {
        "patch_dimensions": f"{patch_size}x{patch_size}",
        "total_pixels_per_patch": patch_size * patch_size,
        "skin_color_features": global_skin_features,
        "features_24d": features_24d,  # <-- Added 24D regional feature payload
        "region_patches": region_patches,
    }