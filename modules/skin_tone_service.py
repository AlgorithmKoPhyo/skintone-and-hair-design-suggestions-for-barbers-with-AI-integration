# modules/skin_tone_service.py
from __future__ import annotations

import logging
from pathlib import Path
import cv2

from modules.skin_extractor import SkinRegionExtractor, FaceNotDetectedError
from modules.skin_classifier import UndertoneClassifier
from modules.skin_feature_extractor import build_pixel_patch_response
from modules.skin_image_processor import STANDARD_PATCH_SIZE, apply_gray_world_wb, resize_image_if_large
from modules.color_analysis_recommender import get_recommendations

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "face_landmarker.task"

class SkinToneService:
    def __init__(self):
        try:
            self.extractor = SkinRegionExtractor(model_path=MODEL_PATH)
        except Exception as err:
            logger.error("Failed to initialize SkinRegionExtractor: %s", err)
            self.extractor = None

        try:
            self.classifier = UndertoneClassifier()
            self.classifier.load()
        except Exception as err:
            logger.warning("UndertoneClassifier model load failed: %s", err)
            self.classifier = None

    def analyze_image(self, image_path: str) -> dict:
        image = cv2.imread(image_path)
        if image is None:
            return {"status": "error", "message": "Failed to read image file."}

        processed_img, _, _ = resize_image_if_large(image, max_dim=800)
        balanced_img = apply_gray_world_wb(processed_img)

        if not self.extractor:
            return {"status": "error", "message": "Skin region extractor uninitialized."}

        try:
            extraction = self.extractor.extract(balanced_img)
        except FaceNotDetectedError as exc:
            return {"status": "error", "message": str(exc), "code": "FACE_NOT_DETECTED"}

        pixel_payload = build_pixel_patch_response(
            extraction, patch_size=STANDARD_PATCH_SIZE
        )

        undertone = "warm"
        confidence = 0.85

        if self.classifier and self.classifier.is_loaded:
            vector_24d = pixel_payload["features_24d"]["feature_vector"]
            pred = self.classifier.predict(vector_24d)
            if pred:
                undertone = str(pred.get("undertone", "warm")).lower()
                if "probabilities" in pred and undertone in pred["probabilities"]:
                    confidence = pred["probabilities"][undertone]

        recs = get_recommendations(undertone)

        return {
            "status": "success",
            "undertone": undertone,
            "confidence": confidence,
            "pixel_payload": pixel_payload,
            "recommendations": recs,
        }