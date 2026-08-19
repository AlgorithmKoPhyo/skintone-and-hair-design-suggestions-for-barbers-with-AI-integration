"""
VGGFace Shape Classifier

Receives an image path, verifies that the image exists,
extracts face embeddings using MTCNN and InceptionResnetV1 (vggface2),
and predicts the face shape using the trained SVM model.

Usage:
    from modules.vgg_face_shape_classifier import VGGFaceShapeClassifier

    classifier = VGGFaceShapeClassifier()

    result = classifier.classify("uploads/face.jpg")

    # {
    #     "face_shape": "Oval",
    #     "confidence": 0.91
    # }
"""

import cv2
import joblib
import torch
from pathlib import Path
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1

# ──────────────────────────────────────────────────────────────
# Model paths
# ──────────────────────────────────────────────────────────────

_MODULE_DIR = Path(__file__).parent / "face_shape_classification"
_VGGFACE_DIR = _MODULE_DIR / "src" / "vggface"

_MODEL_PATH = _VGGFACE_DIR / "face_shape_svm.joblib"
_SCALER_PATH = _VGGFACE_DIR / "scaler.joblib"


class VGGFaceShapeClassifier:
    """
    Classify face shape from a local image using VGGFace embeddings.

    Pipeline:

        Image Path
            ↓
        File Exists?
            ↓
        OpenCV Image -> PIL Image
            ↓
        MTCNN Face Detection & Alignment
            ↓
        InceptionResnetV1 (vggface2) Embeddings
            ↓
        StandardScaler
            ↓
        SVM
            ↓
        Face Shape + Confidence
    """

    def __init__(self):

        # ──────────────────────────────────────────────
        # Initialize device
        # ──────────────────────────────────────────────
        
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

        # ──────────────────────────────────────────────
        # Load trained ML artifacts
        # ──────────────────────────────────────────────

        self.model = joblib.load(_MODEL_PATH)
        self.scaler = joblib.load(_SCALER_PATH)

        # ──────────────────────────────────────────────
        # Processing components
        # ──────────────────────────────────────────────

        self.mtcnn = MTCNN(
                image_size=160,
                margin=20,
                keep_all=False, 
                select_largest=True, #get the largest face
                post_process=True, 
                device=self.device
            )
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)

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
        # Step 2 - Preprocess for MTCNN
        # =========================

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_image)

        # =========================
        # Step 3 - Detect Face & Extract Embeddings
        # =========================

        try:
            boxes, _ = self.mtcnn.detect(pil_img)

            if boxes is None or len(boxes) == 0:
                return {
                    "error": "No face detected in the image"
                }

            face_tensor = self.mtcnn(pil_img)

            if face_tensor is None:
                return {
                    "error": "Failed to extract face features"
                }

            face_tensor = face_tensor.unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                emb = self.resnet(face_tensor).cpu().numpy().flatten()
                
        except Exception as e:
            return {
                "error": f"Face detection or embedding extraction failed: {str(e)}"
            }

        # =========================
        # Step 4 - Scale Embeddings
        # =========================

        emb_scaled = self.scaler.transform([emb])

        # =========================
        # Step 5 - SVM Prediction
        # =========================

        prediction = self.model.predict(emb_scaled)
        
        # Determine confidence if probability is supported
        if hasattr(self.model, "predict_proba"):
            probability = self.model.predict_proba(emb_scaled)
            confidence = float(probability.max())
        else:
            # Fallback if probability is not enabled on this SVM
            confidence = 1.0

        label = prediction[0]

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
                    f"[VGGFaceShapeClassifier] Image not found: {path}"
                )
                return None

            # Check it is actually a file
            if not path.is_file():
                print(
                    f"[VGGFaceShapeClassifier] Path is not a file: {path}"
                )
                return None

            # Read image
            image = cv2.imread(str(path))

            if image is None:
                print(
                    f"[VGGFaceShapeClassifier] Failed to decode image: {path}"
                )
                return None

            return image

        except Exception as e:
            print(
                f"[VGGFaceShapeClassifier] Image loading error: {e}"
            )
            return None
