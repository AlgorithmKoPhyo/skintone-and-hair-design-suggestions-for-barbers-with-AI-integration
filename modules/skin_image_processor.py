"""Image preprocessing utilities: resizing, white balance, and skin validation."""

from __future__ import annotations

from typing import Any

import cv2
import numpy as np

# Standard YCrCb skin thresholds (OpenCV channel order: Y, Cr, Cb).
SKIN_CR_MIN = 133
SKIN_CR_MAX = 173
SKIN_CB_MIN = 77
SKIN_CB_MAX = 127

MIN_SKIN_PIXEL_RATIO = 0.15
STANDARD_PATCH_SIZE = 15
TOTAL_PATCH_PIXELS = STANDARD_PATCH_SIZE * STANDARD_PATCH_SIZE

REGIONS = ["forehead", "left_cheek", "right_cheek", "chin"]

FEATURE_KEYS: list[str] = []
for region in REGIONS:
    FEATURE_KEYS.extend([
        f"{region}_mean_L",
        f"{region}_mean_a",
        f"{region}_mean_b",
        f"{region}_std_L",
        f"{region}_std_a",
        f"{region}_std_b",
    ])

def adjust_gamma(image: np.ndarray, gamma: float = 1.0) -> np.ndarray:
    """Apply gamma correction to adjust overall image exposure."""
    inv_gamma = 1.0 / gamma
    table = ((np.arange(0, 256) / 255.0) ** inv_gamma * 255).astype(np.uint8)
    return cv2.LUT(image, table)

def auto_correct_exposure(image: np.ndarray) -> np.ndarray:
    """Dynamically darken or brighten image based on center luminance."""
    h, w = image.shape[:2]
    # Look at the center 50% where the face usually is
    center_crop = image[int(h*0.25):int(h*0.75), int(w*0.25):int(w*0.75)]
    
    # Calculate luminance (Y channel in YCrCb)
    ycrcb = cv2.cvtColor(center_crop, cv2.COLOR_BGR2YCrCb)
    mean_y = np.mean(ycrcb[:, :, 0])
    
    # If center is excessively bright, darken it
    if mean_y > 180:
        return adjust_gamma(image, gamma=0.7)
    # If center is extremely dark, brighten it
    elif mean_y < 70:
        return adjust_gamma(image, gamma=1.3)
    return image

def resize_image_if_large(
    img: np.ndarray,
    max_dim: int = 800,
) -> tuple[np.ndarray, bool, dict[str, int]]:
    """
    Downscale images whose longest side exceeds ``max_dim``.

    Uses ``cv2.INTER_AREA`` for high-quality downsampling.

    Returns:
        Tuple of (processed image, was_resized flag, size metadata dict).
    """
    if img is None or img.size == 0:
        raise ValueError("Input image is empty or invalid.")

    height, width = img.shape[:2]
    original_size = {"width": width, "height": height}

    if max(height, width) <= max_dim:
        return img, False, original_size

    scale = max_dim / float(max(height, width))
    new_width = int(round(width * scale))
    new_height = int(round(height * scale))

    resized = cv2.resize(
        img,
        (new_width, new_height),
        interpolation=cv2.INTER_AREA,
    )
    return resized, True, original_size

def create_ycrcb_skin_mask(
    bgr_patch: np.ndarray,
    cr_min: int = SKIN_CR_MIN,
    cr_max: int = SKIN_CR_MAX,
    cb_min: int = SKIN_CB_MIN,
    cb_max: int = SKIN_CB_MAX,
) -> np.ndarray:
    """
    Build a binary mask of likely skin pixels using YCrCb thresholds.

    Filters hair, heavy shadows, and non-skin regions within a patch.
    """
    if bgr_patch is None or bgr_patch.size == 0:
        raise ValueError("Patch is empty or invalid.")

    ycrcb = cv2.cvtColor(bgr_patch, cv2.COLOR_BGR2YCrCb)
    cr = ycrcb[:, :, 1]
    cb = ycrcb[:, :, 2]

    mask = ((cr >= cr_min) & (cr <= cr_max) & (cb >= cb_min) & (cb <= cb_max)).astype(
        np.uint8
    )
    return mask

# modules/skin_image_processor.py ထဲတွင် အောက်ပါ Function ကို ထည့်ပါ

def validate_face_lighting(face_crop: np.ndarray) -> dict[str, Any]:
    """
    Validates if the detected face has adequate lighting and valid skin color data.
    """
    if face_crop is None or face_crop.size == 0:
        return {"is_valid": False, "message": "မျက်နှာကို ရှာမတွေ့ပါ။ (Face crop is empty)"}

    # ၁။ အလင်းအမှောင် (Brightness) ကို တိုင်းတာခြင်း
    gray_face = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
    mean_brightness = np.mean(gray_face)

    # အလင်းနည်းလွန်း/မှောင်လွန်းလျှင် (Threshold 50 အောက်)
    if mean_brightness < 50:
        return {
            "is_valid": False, 
            "message": "ဓာတ်ပုံမှာ မျက်နှာအရမ်းမှောင်နေပါတယ်။ ကျေးဇူးပြု၍ အလင်းရောင်ကောင်းမွန်သော နေရာတွင် မျက်နှာကို အလင်းပေး၍ ပြန်လည်ရိုက်ကူးပါ။ (Too Dark/Backlit)"
        }
    
    # အလင်းများလွန်း/ဖြူဖွေးနေလျှင် (Threshold 210 အထက်)
    if mean_brightness > 210:
        return {
            "is_valid": False, 
            "message": "မျက်နှာပေါ်တွင် အလင်းပြန်လွန်းနေပါသည်။ ကျေးဇူးပြု၍ အလင်းရောင် တိုက်ရိုက်မကျသော နေရာတွင် ပြန်လည်ရိုက်ကူးပါ။ (Too Bright/Overexposed)"
        }

    # ၂။ သဘာဝ အရေပြားအရောင် (Skin Pixels) ပါဝင်မှုကို စစ်ဆေးခြင်း
    # မူလရေးသားထားသော create_ycrcb_skin_mask ကို အသုံးပြုပါသည်
    skin_mask = create_ycrcb_skin_mask(face_crop)
    skin_ratio = np.count_nonzero(skin_mask) / skin_mask.size

    # အရေပြားအရောင် ၅% တောင် မတွေ့ရလျှင် (အရိပ်များကြောင့် အရောင်ပြောင်းသွားခြင်း)
    if skin_ratio < 0.05:
        return {
            "is_valid": False,
            "message": "မျက်နှာပေါ်တွင် သဘာဝအသားအရေ အရောင်ကို ရှာမတွေ့ပါ။ အလင်းရောင်မကောင်းခြင်း (သို့) အရောင်ရင့်သော အရိပ်များ ကျနေခြင်းကြောင့် ဖြစ်နိုင်ပါသည်။ နေရာပြောင်း၍ ပြန်လည်ရိုက်ကူးပါ။ (Invalid Skin Color)"
        }

    return {"is_valid": True, "message": "Good lighting"}


# def apply_gray_world_wb(img: np.ndarray) -> np.ndarray:
#     """
#     Apply Gray World white balance to a BGR image.

#     Assumes the average color in the scene should be neutral gray and
#     scales each channel accordingly.
#     """
#     if img is None or img.size == 0:
#         raise ValueError("Input image is empty or invalid.")

#     if len(img.shape) != 3 or img.shape[2] != 3:
#         raise ValueError("Gray World white balance requires a 3-channel BGR image.")

#     result = img.astype(np.float32)
#     channel_means = [
#         float(np.mean(result[:, :, 0])),
#         float(np.mean(result[:, :, 1])),
#         float(np.mean(result[:, :, 2])),
#     ]

#     if any(mean <= 0 for mean in channel_means):
#         return img.copy()

#     gray_mean = sum(channel_means) / 3.0

#     for channel_idx, mean in enumerate(channel_means):
#         result[:, :, channel_idx] *= gray_mean / mean

#     return np.clip(result, 0, 255).astype(np.uint8)
# modules/skin_image_processor.py ထဲတွင် အောက်ပါ Function ကို ထည့်ပါ

def apply_face_aware_wb(img: np.ndarray, face_bbox: tuple[int, int, int, int], strength: float = 0.5) -> np.ndarray:
    """
    Applies gentle Gray World white balance based on the detected face region
    to reduce ambient lighting cast while preserving natural skin undertone.
    strength: 0.0 (no change) to 1.0 (full Gray World). Default 0.5.
    """
    if img is None or img.size == 0:
        raise ValueError("Input image is empty or invalid.")

    x, y, w, h = face_bbox
    
    # ဓာတ်ပုံဘောင်ကျော်မသွားစေရန် ထိန်းချုပ်ခြင်း (Safety checks)
    img_h, img_w = img.shape[:2]
    x = max(0, int(x))
    y = max(0, int(y))
    w = max(1, min(int(w), img_w - x))
    h = max(1, min(int(h), img_h - y))
    
    # မျက်နှာဧရိယာကိုပဲ ဖြတ်ယူခြင်း
    face_crop = img[y:y+h, x:x+w]
    
    # Error ဖြစ်ခဲ့ပါက မူရင်းပုံကိုသာ ပြန်ပေးရန်
    if face_crop.size == 0:
        return img.copy()

    result = img.astype(np.float32)
    
    # မျက်နှာပေါ်ရှိ အရောင်များကိုသာ ပျမ်းမျှတွက်ချက်ခြင်း (Background များကို ဖယ်ထုတ်လိုက်ပြီ)
    channel_means = [
        float(np.mean(face_crop[:, :, 0])),
        float(np.mean(face_crop[:, :, 1])),
        float(np.mean(face_crop[:, :, 2])),
    ]

    if any(mean <= 0 for mean in channel_means):
        return img.copy()

    gray_mean = sum(channel_means) / 3.0

    # တစ်ပုံလုံးကို မျက်နှာအလင်းရောင်ပေါ်မူတည်ပြီး သဘာဝကျကျ ချိန်ညှိခြင်း (Gentle Scaling)
    for channel_idx, mean in enumerate(channel_means):
        scale = gray_mean / mean
        blended_scale = 1.0 + strength * (scale - 1.0)
        # Limit scaling factor to safe range [0.75, 1.35]
        blended_scale = max(0.75, min(1.35, blended_scale))
        result[:, :, channel_idx] *= blended_scale

    return np.clip(result, 0, 255).astype(np.uint8)





# def compute_skin_validated_mean_color(
#     bgr_patch: np.ndarray,
#     cr_min: int = SKIN_CR_MIN,
#     cr_max: int = SKIN_CR_MAX,
#     cb_min: int = SKIN_CB_MIN,
#     cb_max: int = SKIN_CB_MAX,
#     min_skin_ratio: float = MIN_SKIN_PIXEL_RATIO,
# ) -> dict[str, object]:
#     """
#     Compute mean BGR/RGB using only YCrCb-validated skin pixels in a patch.

#     Returns color statistics plus quality metadata for downstream validation.
#     """
#     skin_mask = create_ycrcb_skin_mask(
#         bgr_patch,
#         cr_min=cr_min,
#         cr_max=cr_max,
#         cb_min=cb_min,
#         cb_max=cb_max,
#     )

#     total_pixels = int(skin_mask.size)
#     skin_pixels = bgr_patch[skin_mask == 1]
#     skin_pixel_count = int(skin_pixels.shape[0])
#     skin_pixel_ratio = skin_pixel_count / total_pixels if total_pixels else 0.0

#     if skin_pixel_count == 0:
#         mean_bgr_raw = cv2.mean(bgr_patch)[:3]
#         mean_bgr = [round(mean_bgr_raw[0]), round(mean_bgr_raw[1]), round(mean_bgr_raw[2])]
#         mean_rgb = [mean_bgr[2], mean_bgr[1], mean_bgr[0]]
#         return {
#             "mean_bgr": mean_bgr,
#             "mean_rgb": mean_rgb,
#             "skin_pixel_count": 0,
#             "skin_pixel_ratio": 0.0,
#             "quality_status": "fallback_all_pixels",
#             "quality_message": (
#                 "No skin pixels passed YCrCb validation; using full-patch average as fallback."
#             ),
#         }

#     mean_bgr_raw = cv2.mean(skin_pixels)[:3]
#     mean_bgr = [round(mean_bgr_raw[0]), round(mean_bgr_raw[1]), round(mean_bgr_raw[2])]
#     mean_rgb = [mean_bgr[2], mean_bgr[1], mean_bgr[0]]

#     if skin_pixel_ratio < min_skin_ratio:
#         quality_status = "low_skin_coverage"
#         quality_message = (
#             f"Only {skin_pixel_ratio:.0%} of patch pixels classified as skin "
#             f"(threshold {min_skin_ratio:.0%})."
#         )
#     else:
#         quality_status = "good"
#         quality_message = None

#     return {
#         "mean_bgr": mean_bgr,
#         "mean_rgb": mean_rgb,
#         "skin_pixel_count": skin_pixel_count,
#         "skin_pixel_ratio": round(skin_pixel_ratio, 4),
#         "quality_status": quality_status,
#         "quality_message": quality_message,
#     }
def compute_skin_validated_mean_color(
    bgr_patch: np.ndarray,
    cr_min: int = SKIN_CR_MIN,
    cr_max: int = SKIN_CR_MAX,
    cb_min: int = SKIN_CB_MIN,
    cb_max: int = SKIN_CB_MAX,
    min_skin_ratio: float = MIN_SKIN_PIXEL_RATIO,
) -> dict[str, object]:
    """Compute mean BGR/RGB using YCrCb-validated skin pixels in a patch with robust fallback."""
    if bgr_patch is None or bgr_patch.size == 0:
        raise ValueError("Patch is empty or invalid.")

    skin_mask = create_ycrcb_skin_mask(bgr_patch, cr_min, cr_max, cb_min, cb_max)
    total_pixels = int(skin_mask.size)
    skin_pixels = bgr_patch[skin_mask == 1]
    skin_pixel_count = int(skin_pixels.shape[0])
    skin_pixel_ratio = skin_pixel_count / total_pixels if total_pixels else 0.0

    if skin_pixel_count > 0:
        mean_bgr_raw = cv2.mean(skin_pixels)[:3]
        quality_status = "good" if skin_pixel_ratio >= min_skin_ratio else "low_skin_coverage"
    else:
        # Fallback to patch mean if YCrCb mask is overly strict
        mean_bgr_raw = cv2.mean(bgr_patch)[:3]
        quality_status = "fallback_patch_mean"

    mean_bgr = [round(mean_bgr_raw[0]), round(mean_bgr_raw[1]), round(mean_bgr_raw[2])]
    mean_rgb = [mean_bgr[2], mean_bgr[1], mean_bgr[0]]

    return {
        "mean_bgr": mean_bgr,
        "mean_rgb": mean_rgb,
        "skin_pixel_count": skin_pixel_count,
        "skin_pixel_ratio": round(skin_pixel_ratio, 4),
        "quality_status": quality_status,
        "quality_message": None if quality_status == "good" else f"{skin_pixel_ratio:.0%} of pixels classified as skin.",
    }


def compute_patch_color_features(bgr_patch: np.ndarray) -> dict[str, Any]:
    """
    Extract dual color-space features from a BGR patch using YCrCb skin masking.

    Computes 12D LAB + RGB mean/std features on validated skin pixels and returns
    both a feature dictionary and ordered feature vector for ML pipelines.
    """
    if bgr_patch is None or bgr_patch.size == 0:
        raise ValueError("Patch is empty or invalid.")

    if len(bgr_patch.shape) != 3 or bgr_patch.shape[2] != 3:
        raise ValueError("Patch must be a 3-channel BGR image.")

    skin_mask = create_ycrcb_skin_mask(bgr_patch)
    valid_mask = skin_mask == 1
    used_fallback_mask = False

    if not np.any(valid_mask):
        valid_mask = np.ones(bgr_patch.shape[:2], dtype=bool)
        used_fallback_mask = True

    skin_bgr = bgr_patch[valid_mask]
    blue = skin_bgr[:, 0].astype(np.float64)
    green = skin_bgr[:, 1].astype(np.float64)
    red = skin_bgr[:, 2].astype(np.float64)

    mean_R = float(np.mean(red))
    mean_G = float(np.mean(green))
    mean_B = float(np.mean(blue))
    std_R = float(np.std(red))
    std_G = float(np.std(green))
    std_B = float(np.std(blue))

    lab_image = cv2.cvtColor(bgr_patch, cv2.COLOR_BGR2Lab)
    l_std = lab_image[:, :, 0].astype(np.float64) * 100.0 / 255.0
    a_std = lab_image[:, :, 1].astype(np.float64) - 128.0
    b_std = lab_image[:, :, 2].astype(np.float64) - 128.0

    lab_pixels = np.stack(
        [l_std[valid_mask], a_std[valid_mask], b_std[valid_mask]],
        axis=1,
    )
    mean_L = float(np.mean(lab_pixels[:, 0]))
    mean_a = float(np.mean(lab_pixels[:, 1]))
    mean_b = float(np.mean(lab_pixels[:, 2]))
    std_L = float(np.std(lab_pixels[:, 0]))
    std_a = float(np.std(lab_pixels[:, 1]))
    std_b = float(np.std(lab_pixels[:, 2]))

    raw_values = [
        mean_L,
        mean_a,
        mean_b,
        std_L,
        std_a,
        std_b,
        mean_R,
        mean_G,
        mean_B,
        std_R,
        std_G,
        std_B,
    ]
    features = {key: round(value, 4) for key, value in zip(FEATURE_KEYS, raw_values)}
    feature_vector = [features[key] for key in FEATURE_KEYS]

    return {
        "features": features,
        "feature_vector": feature_vector,
        "skin_pixel_count": int(np.count_nonzero(valid_mask)),
        "used_fallback_mask": used_fallback_mask,
    }


def ensure_standard_patch(
    bgr_patch: np.ndarray,
    patch_size: int = STANDARD_PATCH_SIZE,
) -> np.ndarray:
    """Resize or crop input to an exact ``patch_size x patch_size`` BGR patch."""
    if bgr_patch is None or bgr_patch.size == 0:
        raise ValueError("Patch is empty or invalid.")

    if len(bgr_patch.shape) != 3 or bgr_patch.shape[2] != 3:
        raise ValueError("Patch must be a 3-channel BGR image.")

    height, width = bgr_patch.shape[:2]
    if height == patch_size and width == patch_size:
        return bgr_patch.copy()

    return cv2.resize(
        bgr_patch,
        (patch_size, patch_size),
        interpolation=cv2.INTER_AREA,
    )


def extract_patch_pixel_matrices(
    bgr_patch: np.ndarray,
    patch_size: int = STANDARD_PATCH_SIZE,
) -> dict[str, Any]:
    """
    Extract full per-pixel RGB and standardized LAB values from a skin patch.

    Returns flattened lists of exactly ``patch_size * patch_size`` (225) pixels.
    """
    patch = ensure_standard_patch(bgr_patch, patch_size=patch_size)

    rgb_image = cv2.cvtColor(patch, cv2.COLOR_BGR2RGB)
    rgb_flat = rgb_image.reshape(-1, 3)
    rgb_pixels = [[int(r), int(g), int(b)] for r, g, b in rgb_flat.tolist()]

    lab_image = cv2.cvtColor(patch, cv2.COLOR_BGR2Lab)
    l_std = lab_image[:, :, 0].astype(np.float64) * 100.0 / 255.0
    a_std = lab_image[:, :, 1].astype(np.float64) - 128.0
    b_std = lab_image[:, :, 2].astype(np.float64) - 128.0

    lab_stack = np.stack([l_std, a_std, b_std], axis=-1).reshape(-1, 3)
    lab_pixels = [
        [round(channel_values[0], 4), round(channel_values[1], 4), round(channel_values[2], 4)]
        for channel_values in lab_stack.tolist()
    ]

    expected_pixels = patch_size * patch_size
    if len(rgb_pixels) != expected_pixels or len(lab_pixels) != expected_pixels:
        raise ValueError(
            f"Expected {expected_pixels} pixels, got RGB={len(rgb_pixels)} LAB={len(lab_pixels)}."
        )

    return {
        "rgb_pixels": rgb_pixels,
        "lab_pixels": lab_pixels,        
    }
