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

        # 4. Face-Aware White Balance ဖြင့် အလင်းညှိပြီး Undertone ဆက်လက် ခွဲခြမ်းစိတ်ဖြာခြင်း
        # PASS 2: Face-Aware White Balance နှင့် Feature Extraction ဆက်လုပ်ခြင်း
        balanced_img = apply_face_aware_wb(processed_img, face_bbox)
        final_extraction = self.extractor.extract(balanced_img)

        try:
            pixel_payload = build_pixel_patch_response(
                final_extraction, patch_size=STANDARD_PATCH_SIZE
            )
        except ValueError as exc:
            # မျက်နှာဧရိယာပေါ်တွင် skin patch လုံလောက်စွာ မရှိပါက (ဥပမာ - အရိပ်ကျနေခြင်း)
            return {
                "status": "error",
                "message": "မျက်နှာပြင်ပေါ်တွင် အသားအရေ အချက်အလက် လုံလောက်စွာ မတွေ့ရှိပါ။ အလင်းရောင်ကောင်းသောနေရာတွင် ရှင်းလင်းစွာ ပြန်လည်ရိုက်ကူးပါ။",
                "code": "INVALID_SKIN_REGIONS"
            }

        undertone = "neutral"
        confidence = 0.85

        if self.classifier and self.classifier.is_loaded:
            vector_24d = pixel_payload["features_24d"]["feature_vector"]
            pred = self.classifier.predict(vector_24d)
            if pred:
                undertone = str(pred.get("undertone", "warm")).lower()
                if "probabilities" in pred and undertone in pred["probabilities"]:
                    confidence = pred["probabilities"][undertone]

        # undertone = "neutral"
        # confidence = 0.85

        # if self.classifier and self.classifier.is_loaded:
        #     # TTA အတွက် Variants (အလင်းအမှောင် အပြောင်းအလဲငယ်များ) ပြုလုပ်ခြင်း
        #     variants = {
        #         "orig": processed_img,
        #         "dark": self._adjust_gamma(processed_img, gamma=0.85),
        #         "bright": self._adjust_gamma(processed_img, gamma=1.15)
        #     }
            
        #     all_probabilities = []
        #     print("\n--- 🔍 TTA (Test-Time Augmentation) Predictions ---")
            
        #     for var_name, var_img in variants.items():
        #         try:
        #             # တစ်ခုချင်းစီအတွက် Face-Aware WB နှင့် Extraction ပြုလုပ်ခြင်း
        #             var_balanced = apply_face_aware_wb(var_img, face_bbox)
        #             var_extraction = self.extractor.extract(var_balanced)
        #             var_payload = build_pixel_patch_response(
        #                 var_extraction, patch_size=STANDARD_PATCH_SIZE
        #             )
                    
        #             vector_24d = var_payload["features_24d"]["feature_vector"]
        #             pred = self.classifier.predict(vector_24d)
                    
        #             if pred:
        #                 print(f"  ▪ Variant [{var_name}]: Pred Result -> {pred}")
                    
        #             if pred and "probabilities" in pred:
        #                 all_probabilities.append(pred["probabilities"])
        #         except Exception as e:
        #             print(f"  ⚠️ Variant [{var_name}] failed: {e}")
        #             continue
            
        #     if all_probabilities:
        #         # Variant အားလုံးမှ probabilities များကို ပျမ်းမျှတွက်ချက်ခြင်း (Average Probabilities)
        #         avg_probabilities = {}
        #         classes = all_probabilities[0].keys()
        #         for cls in classes:
        #             avg_probabilities[cls] = float(np.mean([p.get(cls, 0.0) for p in all_probabilities]))
                
        #         print(f"  📊 Averaged Probabilities: {avg_probabilities}")
                
        #         # အမြင့်ဆုံး Probability ရှိသော Undertone ကို ရွေးချယ်ခြင်း
        #         best_undertone = max(avg_probabilities, key=avg_probabilities.get)
        #         undertone = str(best_undertone).lower()
        #         confidence = float(avg_probabilities[undertone])
        #         print(f"  🎯 Final TTA Decision: {undertone.upper()} (Confidence: {confidence:.2f})\n--------------------------------------------------")
        #     else:
        #         # Fallback to single prediction if variants fail
        #         vector_24d = pixel_payload["features_24d"]["feature_vector"]
        #         pred = self.classifier.predict(vector_24d)
        #         if pred:
        #             undertone = str(pred.get("undertone", "neutral")).lower()
        #             if "probabilities" in pred and undertone in pred["probabilities"]:
        #                 confidence = pred["probabilities"][undertone]

        recs = get_recommendations(undertone)

        return {
            "status": "success",
            "undertone": undertone,
            "confidence": confidence,
            "pixel_payload": pixel_payload,
            "recommendations": recs,
        }