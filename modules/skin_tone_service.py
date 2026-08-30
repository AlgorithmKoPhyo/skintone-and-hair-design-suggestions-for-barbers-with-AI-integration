# modules/skin_tone_service.py
from __future__ import annotations

import logging
from pathlib import Path
import cv2
import numpy as np

from modules.skin_extractor import SkinRegionExtractor, FaceNotDetectedError
from modules.skin_classifier import UndertoneClassifier
from modules.skin_feature_extractor import build_pixel_patch_response
# from modules.skin_image_processor import STANDARD_PATCH_SIZE, apply_gray_world_wb, resize_image_if_large
from modules.skin_image_processor import STANDARD_PATCH_SIZE, apply_face_aware_wb, resize_image_if_large, validate_face_lighting
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

    # def analyze_image(self, image_path: str) -> dict:
    #     image = cv2.imread(image_path)
    #     if image is None:
    #         return {"status": "error", "message": "Failed to read image file."}

    #     processed_img, _, _ = resize_image_if_large(image, max_dim=800)
    #     balanced_img = apply_gray_world_wb(processed_img)

    #     if not self.extractor:
    #         return {"status": "error", "message": "Skin region extractor uninitialized."}

    #     try:
    #         extraction = self.extractor.extract(balanced_img)
    #     except FaceNotDetectedError as exc:
    #         return {"status": "error", "message": str(exc), "code": "FACE_NOT_DETECTED"}

    #     pixel_payload = build_pixel_patch_response(
    #         extraction, patch_size=STANDARD_PATCH_SIZE
    #     )

    #     undertone = "warm"
    #     confidence = 0.85

    #     if self.classifier and self.classifier.is_loaded:
    #         vector_24d = pixel_payload["features_24d"]["feature_vector"]
    #         pred = self.classifier.predict(vector_24d)
    #         if pred:
    #             undertone = str(pred.get("undertone", "warm")).lower()
    #             if "probabilities" in pred and undertone in pred["probabilities"]:
    #                 confidence = pred["probabilities"][undertone]

    #     recs = get_recommendations(undertone)

    #     return {
    #         "status": "success",
    #         "undertone": undertone,
    #         "confidence": confidence,
    #         "pixel_payload": pixel_payload,
    #         "recommendations": recs,
    #     }
    def _adjust_gamma(self, image, gamma=1.0):
        invGamma = 1.0 / gamma
        table = ((np.arange(0, 256) / 255.0) ** invGamma * 255).astype("uint8")
        return cv2.LUT(image, table)
    
    def analyze_image(self, image_path: str) -> dict:
        # 1. ပထမဦးစွာ FaceValidator ဖြင့် မျက်နှာအရေအတွက်နှင့် အမှန်တကယ် ပါဝင်မှုကို စစ်ဆေးခြင်း
        # (အကယ်၍ FaceValidator class ကို သီးသန့်ဖိုင်ခွဲထားပါက အသုံးပြုရန်)
        image = cv2.imread(image_path)
        if image is None:
            return {"status": "error", "message": "Failed to read image file.", "code": "INVALID_IMAGE"}

        processed_img, _, _ = resize_image_if_large(image, max_dim=800)

        if not self.extractor:
            return {"status": "error", "message": "Skin region extractor uninitialized."}

        # 2. မျက်နှာရှာဖွေခြင်းနှင့် အရေအတွက် စစ်ဆေးခြင်း (MediaPipe Landmarker မှတဆင့်)
        try:
            raw_extraction = self.extractor.extract(processed_img)
        except Exception as exc:
            # မျက်နှာမတွေ့လျှင် သို့မဟုတ် Error တက်လျှင် UI တွင် ပြရန် Error code ပို့ပေးမည်
            return {
                "status": "error", 
                "message": "No face was detected in the uploaded image. Please upload a clear photo showing your face.", 
                "code": "NO_FACE_DETECTED"
            }

        # 3. မျက်နှာ Bounding Box ကို ယူ၍ အလင်းအမှောင် (Lighting) စစ်ဆေးခြင်း
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = 0, 0
        
        regions = raw_extraction.get("regions", {})
        for reg_name, reg_data in regions.items():
            bbox = reg_data.get("bbox")
            if bbox and reg_data.get("status") != "error":
                min_x = min(min_x, bbox.get("x1", float('inf')))
                min_y = min(min_y, bbox.get("y1", float('inf')))
                max_x = max(max_x, bbox.get("x2", 0))
                max_y = max(max_y, bbox.get("y2", 0))

        if min_x == float('inf'):
            h, w = processed_img.shape[:2]
            face_bbox = (int(w*0.25), int(h*0.25), int(w*0.5), int(h*0.5))
        else:
            face_bbox = (min_x, min_y, max_x - min_x, max_y - min_y)

        x, y, w_box, h_box = face_bbox
        img_h, img_w = processed_img.shape[:2]
        x = max(0, int(x))
        y = max(0, int(y))
        w_box = max(1, min(int(w_box), img_w - x))
        h_box = max(1, min(int(h_box), img_h - y))
        
        face_crop = processed_img[y:y+h_box, x:x+w_box]
        
        # အလင်းအမှောင် Quality Validation စစ်ဆေးခြင်း
        validation_result = validate_face_lighting(face_crop)
        if not validation_result["is_valid"]:
            return {
                "status": "error", 
                "message": validation_result["message"], 
                "code": "POOR_LIGHTING"
            }

        # 4. Feature Extraction & Robust Multi-Pass Prediction
        try:
            raw_payload = build_pixel_patch_response(
                raw_extraction, patch_size=STANDARD_PATCH_SIZE
            )
        except ValueError as exc:
            return {
                "status": "error",
                "message": "မျက်နှာပြင်ပေါ်တွင် အသားအရေ အချက်အလက် လုံလောက်စွာ မတွေ့ရှိပါ။ အလင်းရောင်ကောင်းသောနေရာတွင် ရှင်းလင်းစွာ ပြန်လည်ရိုက်ကူးပါ။",
                "code": "INVALID_SKIN_REGIONS"
            }

        # PASS 2: Gentle Face-Aware White Balance
        balanced_img = apply_face_aware_wb(processed_img, face_bbox, strength=0.5)
        try:
            final_extraction = self.extractor.extract(balanced_img)
            balanced_payload = build_pixel_patch_response(
                final_extraction, patch_size=STANDARD_PATCH_SIZE
            )
        except Exception:
            # Graceful fallback to raw extraction if balanced image detection fails
            final_extraction = raw_extraction
            balanced_payload = raw_payload

        undertone = "neutral"
        confidence = 0.0
        probabilities = {"cool": 0.0, "neutral": 0.0, "warm": 0.0}

        if self.classifier and self.classifier.is_loaded:
            raw_vector = raw_payload["features_24d"]["feature_vector"]
            balanced_vector = balanced_payload["features_24d"]["feature_vector"]

            pred_raw = self.classifier.predict(raw_vector)
            pred_balanced = self.classifier.predict(balanced_vector)

            # Ensemble probabilities across raw and balanced features
            if pred_raw and "probabilities" in pred_raw and pred_balanced and "probabilities" in pred_balanced:
                classes = pred_raw["probabilities"].keys()
                avg_probabilities = {}
                for cls in classes:
                    avg_p = (pred_raw["probabilities"].get(cls, 0.0) + pred_balanced["probabilities"].get(cls, 0.0)) / 2.0
                    avg_probabilities[cls] = round(float(avg_p), 4)

                probabilities = avg_probabilities
                undertone = str(max(avg_probabilities, key=avg_probabilities.get)).lower()
                confidence = float(avg_probabilities[undertone])
            elif pred_balanced:
                undertone = str(pred_balanced.get("undertone", "neutral")).lower()
                if "probabilities" in pred_balanced and undertone in pred_balanced["probabilities"]:
                    confidence = float(pred_balanced["probabilities"][undertone])
                    probabilities = pred_balanced["probabilities"]
            elif pred_raw:
                undertone = str(pred_raw.get("undertone", "neutral")).lower()
                if "probabilities" in pred_raw and undertone in pred_raw["probabilities"]:
                    confidence = float(pred_raw["probabilities"][undertone])
                    probabilities = pred_raw["probabilities"]

        recs = get_recommendations(undertone)

        return {
            "status": "success",
            "undertone": undertone,
            "confidence": confidence,
            "probabilities": probabilities,
            "pixel_payload": balanced_payload or raw_payload,
            "recommendations": recs,
        }