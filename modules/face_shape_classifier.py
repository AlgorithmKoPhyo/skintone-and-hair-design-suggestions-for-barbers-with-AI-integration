
"""
Face Shape Classifier

Receives an image path, verifies that the image exists,
extracts facial landmarks, calculates features, and predicts
the face shape using the trained SVM model.

Usage:
    from modules.face_shape_classifier import FaceShapeClassifier

    classifier = FaceShapeClassifier()

    result = classifier.classify("uploads/face.jpg")

    # {
    #     "face_shape": "Oval",
    #     "confidence": 0.91
    # }
"""

import sys

import cv2
import joblib
import numpy as np
import pandas as pd

from pathlib import Path


# ──────────────────────────────────────────────────────────────
# Add face_shape_classification to path
# ──────────────────────────────────────────────────────────────

_MODULE_DIR = Path(__file__).parent / "face_shape_classification"

if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))


from modules.face_shape_classification.src.landmarks.landmark_extractor import (
    LandmarkExtractor
)

from modules.face_shape_classification.src.landmarks.landmark_normalizer import (
    LandmarkNormalizer
)

from modules.face_shape_classification.src.features.feature_calculator import (
    FeatureCalculator
)


# ──────────────────────────────────────────────────────────────
# Model paths
# ──────────────────────────────────────────────────────────────

_MODELS_DIR = _MODULE_DIR / "models"

_MODEL_PATH = _MODELS_DIR / "svm_face_shape_model.pkl"
_SCALER_PATH = _MODELS_DIR / "svm_scaler.pkl"
_PCA_PATH = _MODELS_DIR / "svm_pca.pkl"
_ENCODER_PATH = _MODELS_DIR / "svm_label_encoder.pkl"


class FaceShapeClassifier:
    """
    Classify face shape from a local image.

    Pipeline:

        Image Path
            ↓
        File Exists?
            ↓
        OpenCV Image
            ↓
        MediaPipe Face Landmarks
            ↓
        Geometric Features
            ↓
        Landmark Normalization
            ↓
        StandardScaler
            ↓
        PCA
            ↓
        SVM
            ↓
        Face Shape + Confidence
    """

    def __init__(self):

        # ──────────────────────────────────────────────
        # Load trained ML artifacts
        # ──────────────────────────────────────────────

        self.model = joblib.load(_MODEL_PATH)
        self.scaler = joblib.load(_SCALER_PATH)
        self.pca = joblib.load(_PCA_PATH)
        self.encoder = joblib.load(_ENCODER_PATH)

        # ──────────────────────────────────────────────
        # Processing components
        # ──────────────────────────────────────────────

        self.landmark_extractor = LandmarkExtractor()
        self.landmark_normalizer = LandmarkNormalizer()
        self.feature_calculator = FeatureCalculator()

    # ──────────────────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────────────────

    def classify(self, image_path: str) -> dict:
        """
        Predict face shape from a local image.

        Args:
            image_path:
                Path to the image.

        Returns:
            {
                "face_shape": str,
                "confidence": float
            }

        Or:

            {
                "error": str
            }
        """

        # =========================
        # Step 1 - Check image
        # =========================

        image = self._load_image(image_path)

        if image is None:
            return {
                "error": "Image does not exist or could not be read"
            }

        # =========================
        # Step 2 - Extract landmarks
        # =========================

        landmarks = self._extract_landmarks_from_array(image)

        if landmarks is None:
            return {
                "error": "No face detected in the image"
            }

        # =========================
        # Step 3 - Calculate geometry
        # =========================

        features = self.feature_calculator.calculate(landmarks)

        # =========================
        # Step 4 - Normalize landmarks
        # =========================

        normalized = self.landmark_normalizer.normalize(landmarks)

        if normalized is None:
            return {
                "error": "Landmark normalization failed"
            }

        for index, value in enumerate(normalized):
            features[f"landmark_{index}"] = value

        # =========================
        # Step 5 - Build DataFrame
        # =========================

        df = pd.DataFrame([features])

        # =========================
        # Step 6 - Scale
        # =========================

        scaled = self.scaler.transform(df)

        # =========================
        # Step 7 - PCA
        # =========================

        pca_features = self.pca.transform(scaled)

        # =========================
        # Step 8 - SVM prediction
        # =========================

        prediction = self.model.predict(pca_features)

        probability = self.model.predict_proba(pca_features)

        # =========================
        # Step 9 - Decode label
        # =========================

        label = self.encoder.inverse_transform(prediction)[0]

        confidence = float(probability.max())

        return {
            "face_shape": label,
            "confidence": confidence
        }

    # ──────────────────────────────────────────────────────────
    # Private helpers
    # ──────────────────────────────────────────────────────────

    def _load_image(self, image_path: str):
        """
        Check whether the image exists and load it
        into a BGR numpy array.

        Returns:
            numpy.ndarray or None
        """

        try:
            path = Path(image_path)

            # Check file exists
            if not path.exists():
                print(
                    f"[FaceShapeClassifier] Image not found: {path}"
                )
                return None

            # Check it is actually a file
            if not path.is_file():
                print(
                    f"[FaceShapeClassifier] Path is not a file: {path}"
                )
                return None

            # Read image
            image = cv2.imread(str(path))

            if image is None:
                print(
                    f"[FaceShapeClassifier] Failed to decode image: {path}"
                )
                return None

            return image

        except Exception as e:
            print(
                f"[FaceShapeClassifier] Image loading error: {e}"
            )
            return None

    def _extract_landmarks_from_array(
        self,
        image: np.ndarray
    ):
        """
        Run MediaPipe landmark extraction on a BGR numpy array.

        Returns:
            list of (x, y, z) tuples
            or None if no face is detected.
        """

        import mediapipe as mp

        # OpenCV -> RGB
        rgb_image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        # MediaPipe processing
        result = self.landmark_extractor.face_mesh.process(
            rgb_image
        )

        if not result.multi_face_landmarks:
            return None

        # Use first detected face
        face_landmarks = result.multi_face_landmarks[0]

        return [
            (point.x, point.y, point.z)
            for point in face_landmarks.landmark
        ]

