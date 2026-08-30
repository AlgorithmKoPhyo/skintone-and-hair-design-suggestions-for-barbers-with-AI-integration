"""Adaptive face landmark grouping, skin patch extraction, and quality validation."""

from __future__ import annotations

import base64
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from modules.skin_image_processor import (
    compute_skin_validated_mean_color,
    extract_patch_pixel_matrices,
)
# Landmark groups for robust region centroids (mean X, mean Y per cluster).
SKIN_LANDMARK_GROUPS: dict[str, list[int]] = {
    "forehead": [10, 151, 9],
    "left_cheek": [50, 117, 123, 187, 205],
    "right_cheek": [280, 346, 352, 411, 425],
    "chin": [152, 175, 200],
}

NOSE_BRIDGE_INDEX = 6
POSE_SYMMETRY_THRESHOLD = 1.5
PATCH_SIZE_FACE_WIDTH_RATIO = 0.04
MIN_PATCH_SIZE = 15

DEFAULT_MODEL_PATH = Path(__file__).resolve().parent / "models" / "face_landmarker.task"
if not DEFAULT_MODEL_PATH.exists():
    # Fallback to project root models/ if present
    _alt_path = Path(__file__).resolve().parent.parent / "models" / "face_landmarker.task"
    if _alt_path.exists():
        DEFAULT_MODEL_PATH = _alt_path


class ModelNotFoundError(FileNotFoundError):
    """Raised when the MediaPipe face landmarker model file is missing."""


class FaceNotDetectedError(ValueError):
    """Raised when no face is detected in the input image."""


@dataclass(frozen=True)
class RegionPatch:
    name: str
    landmark_indices: list[int]
    center_x: int
    center_y: int
    patch_size: int
    bbox: dict[str, int]
    status: str
    patch_base64: str | None = None
    rgb_pixels: list[list[int]] | None = None     
    lab_pixels: list[list[float]] | None = None
    mean_bgr: list[int] | None = None
    mean_rgb: list[int] | None = None
    skin_pixel_count: int | None = None
    skin_pixel_ratio: float | None = None
    quality_status: str | None = None
    quality_message: str | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "name": self.name,
            "landmark_indices": self.landmark_indices,
            "center_x": self.center_x,
            "center_y": self.center_y,
            "patch_size": self.patch_size,
            "bbox": self.bbox,
            "status": self.status,
        }
        if self.rgb_pixels is not None:            
            payload["rgb_pixels"] = self.rgb_pixels
        if self.lab_pixels is not None:            
            payload["lab_pixels"] = self.lab_pixels
        if self.patch_base64 is not None:
            payload["patch_base64"] = self.patch_base64
        if self.mean_bgr is not None:
            payload["mean_bgr"] = self.mean_bgr
        if self.mean_rgb is not None:
            payload["mean_rgb"] = self.mean_rgb
        if self.skin_pixel_count is not None:
            payload["skin_pixel_count"] = self.skin_pixel_count
        if self.skin_pixel_ratio is not None:
            payload["skin_pixel_ratio"] = self.skin_pixel_ratio
        if self.quality_status is not None:
            payload["quality_status"] = self.quality_status
        if self.quality_message is not None:
            payload["quality_message"] = self.quality_message
        if self.error is not None:
            payload["error"] = self.error
        return payload


class SkinRegionExtractor:
    """MediaPipe Face Landmarker wrapper for adaptive skin patch extraction."""

    def __init__(self, model_path: Path | str = DEFAULT_MODEL_PATH) -> None:
        self.model_path = Path(model_path)
        if not self.model_path.is_file():
            raise ModelNotFoundError(
                f"Face landmarker model not found at '{self.model_path}'. "
                "Run 'python download_model.py' to download it."
            )

        base_options = python.BaseOptions(model_asset_path=str(self.model_path))
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_faces=1,
            min_face_detection_confidence=0.5,
            min_face_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self._landmarker = vision.FaceLandmarker.create_from_options(options)

    def close(self) -> None:
        self._landmarker.close()

    def __enter__(self) -> "SkinRegionExtractor":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def extract(self, bgr_image: np.ndarray) -> dict[str, Any]:
        """Detect landmarks, compute centroids, and extract validated skin patches."""
        if bgr_image is None or bgr_image.size == 0:
            raise ValueError("Input image is empty or invalid.")

        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        result = self._landmarker.detect(mp_image)

        if not result.face_landmarks:
            raise FaceNotDetectedError(
                "No face detected in the image. Ensure the face is visible, "
                "well-lit, and not heavily occluded."
            )

        landmarks = result.face_landmarks[0]
        height, width = bgr_image.shape[:2]

        face_width = compute_face_bbox_width(landmarks, width, height)
        patch_size = compute_dynamic_patch_size(face_width)

        centroids = {
            region_name: compute_group_centroid(landmarks, indices, width, height)
            for region_name, indices in SKIN_LANDMARK_GROUPS.items()
        }

        pose_status, pose_metadata = assess_face_pose(
            landmarks,
            width,
            height,
            centroids["left_cheek"],
            centroids["right_cheek"],
        )

        regions: dict[str, dict[str, Any]] = {}
        for region_name, indices in SKIN_LANDMARK_GROUPS.items():
            centroid_x, centroid_y = centroids[region_name]
            regions[region_name] = _extract_region_patch(
                bgr_image=bgr_image,
                region_name=region_name,
                landmark_indices=indices,
                center_x=centroid_x,
                center_y=centroid_y,
                patch_size=patch_size,
            )

        return {
            "face_detected": True,
            "num_faces": len(result.face_landmarks),
            "face_width": face_width,
            "patch_size": patch_size,
            "pose_status": pose_status,
            "pose_metadata": pose_metadata,
            "regions": regions,
        }


def extract_skin_regions(
    bgr_image: np.ndarray,
    model_path: Path | str = DEFAULT_MODEL_PATH,
) -> dict[str, Any]:
    """Convenience helper that opens and closes the landmarker automatically."""
    with SkinRegionExtractor(model_path=model_path) as extractor:
        return extractor.extract(bgr_image)


def compute_group_centroid(
    landmarks: list[Any],
    indices: list[int],
    width: int,
    height: int,
) -> tuple[int, int]:
    """Compute pixel centroid as mean X and mean Y over a landmark group."""
    xs: list[float] = []
    ys: list[float] = []

    for index in indices:
        if index >= len(landmarks):
            continue
        landmark = landmarks[index]
        xs.append(landmark.x * width)
        ys.append(landmark.y * height)

    if not xs:
        raise ValueError(f"No valid landmarks found for indices {indices}.")

    return int(round(float(np.mean(xs)))), int(round(float(np.mean(ys))))


def compute_face_bbox_width(
    landmarks: list[Any],
    width: int,
    height: int,
) -> int:
    """Estimate face width from the horizontal span of all detected landmarks."""
    xs = [landmark.x * width for landmark in landmarks]
    return max(1, int(round(max(xs) - min(xs))))


def compute_dynamic_patch_size(face_width: int) -> int:
    """Scale-invariant patch size: max(15, 4% of face bounding-box width)."""
    return max(MIN_PATCH_SIZE, int(face_width * PATCH_SIZE_FACE_WIDTH_RATIO))


def assess_face_pose(
    landmarks: list[Any],
    width: int,
    height: int,
    left_cheek_center: tuple[int, int],
    right_cheek_center: tuple[int, int],
    nose_index: int = NOSE_BRIDGE_INDEX,
    symmetry_threshold: float = POSE_SYMMETRY_THRESHOLD,
) -> tuple[str, dict[str, float]]:
    """
    Estimate head yaw via nose-to-cheek distance symmetry.

    Returns pose_status and diagnostic metadata.
    """
    if nose_index >= len(landmarks):
        return "unknown", {"symmetry_ratio": 0.0}

    nose = landmarks[nose_index]
    nose_x = nose.x * width
    nose_y = nose.y * height

    left_x, left_y = left_cheek_center
    right_x, right_y = right_cheek_center

    dist_left = math.hypot(nose_x - left_x, nose_y - left_y)
    dist_right = math.hypot(nose_x - right_x, nose_y - right_y)
    nearer = max(min(dist_left, dist_right), 1e-6)
    symmetry_ratio = max(dist_left, dist_right) / nearer

    metadata = {
        "nose_to_left_cheek": round(dist_left, 2),
        "nose_to_right_cheek": round(dist_right, 2),
        "symmetry_ratio": round(symmetry_ratio, 3),
    }

    if symmetry_ratio > symmetry_threshold:
        return "face_turned_sideways", metadata

    return "centered", metadata


def _extract_region_patch(
    bgr_image: np.ndarray,
    region_name: str,
    landmark_indices: list[int],
    center_x: int,
    center_y: int,
    patch_size: int,
) -> dict[str, Any]:
    """Crop, validate, and summarize one skin region patch."""
    try:
        patch, bbox, center_x, center_y = crop_patch(
            bgr_image,
            center_x,
            center_y,
            patch_size,
        )
        color_stats = compute_skin_validated_mean_color(patch)

        # 15x15 Pixel Matrices (225 pixels for RGB & LAB) Extraction
        raw_matrices = extract_patch_pixel_matrices(patch)

        region_status = "success"
        quality_status = str(color_stats["quality_status"])
        quality_message = color_stats["quality_message"]

        if quality_status in {"low_skin_coverage", "fallback_all_pixels"}:
            region_status = "warning"

        return RegionPatch(
            name=region_name,
            landmark_indices=landmark_indices,
            center_x=center_x,
            center_y=center_y,
            patch_size=patch_size,
            bbox=bbox,
            status=region_status,
            patch_base64=_encode_patch_png(patch),
            rgb_pixels=raw_matrices["rgb_pixels"],  
            lab_pixels=raw_matrices["lab_pixels"],   
            mean_bgr=list(color_stats["mean_bgr"]),  # type: ignore[arg-type]
            mean_rgb=list(color_stats["mean_rgb"]),  # type: ignore[arg-type]
            skin_pixel_count=int(color_stats["skin_pixel_count"]),
            skin_pixel_ratio=float(color_stats["skin_pixel_ratio"]),
            quality_status=quality_status,
            quality_message=str(quality_message) if quality_message else None,
        ).to_dict()

    except Exception as exc:  # noqa: BLE001 - surface per-region failures
        return RegionPatch(
            name=region_name,
            landmark_indices=landmark_indices,
            center_x=center_x,
            center_y=center_y,
            patch_size=patch_size,
            bbox={"x1": 0, "y1": 0, "x2": 0, "y2": 0},
            status="error",
            error=str(exc),
        ).to_dict()


def clamp_center_to_frame(
    center_x: int,
    center_y: int,
    patch_size: int,
    width: int,
    height: int,
) -> tuple[int, int]:
    """Clamp patch center so the full patch stays inside image bounds."""
    half = patch_size // 2
    min_center = half
    max_center_x = width - patch_size + half
    max_center_y = height - patch_size + half

    clamped_x = max(min_center, min(max_center_x, center_x))
    clamped_y = max(min_center, min(max_center_y, center_y))
    return clamped_x, clamped_y


def crop_patch(
    image: np.ndarray,
    center_x: int,
    center_y: int,
    patch_size: int,
) -> tuple[np.ndarray, dict[str, int], int, int]:
    """
    Crop a fixed-size patch centered on (center_x, center_y).

    The center is clamped so the entire patch remains within the frame.
    """
    height, width = image.shape[:2]

    if width < patch_size or height < patch_size:
        raise ValueError(
            f"Image ({width}x{height}) is too small for a {patch_size}x{patch_size} patch."
        )

    center_x, center_y = clamp_center_to_frame(
        center_x,
        center_y,
        patch_size,
        width,
        height,
    )

    half = patch_size // 2
    x1 = center_x - half
    y1 = center_y - half
    x2 = x1 + patch_size
    y2 = y1 + patch_size

    if x1 < 0 or y1 < 0 or x2 > width or y2 > height:
        raise ValueError("Patch boundaries exceed image dimensions.")

    patch = image[y1:y2, x1:x2].copy()

    if patch.shape[0] != patch_size or patch.shape[1] != patch_size:
        raise ValueError("Patch crop failed boundary check.")

    return patch, {"x1": x1, "y1": y1, "x2": x2, "y2": y2}, center_x, center_y


def _encode_patch_png(patch: np.ndarray) -> str:
    """Encode a BGR patch as a base64 PNG string."""
    success, buffer = cv2.imencode(".png", patch)
    if not success:
        raise RuntimeError("Failed to encode patch as PNG.")
    return base64.b64encode(buffer.tobytes()).decode("ascii")
