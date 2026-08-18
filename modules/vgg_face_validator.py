import cv2
import torch
from pathlib import Path
from PIL import Image
from facenet_pytorch import MTCNN

class VGGFaceValidator:
    """
    Validates whether an uploaded image contains a detectable face using MTCNN (VGG Pipeline).

    This class provides the exact same interface as the old FaceValidator
    so it can act as a drop-in replacement in main.py.
    """

    def __init__(self):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        # We use keep_all=True here so we can detect multiple faces and warn the user.
        self.mtcnn = MTCNN(
            image_size=160, margin=20, keep_all=True, post_process=True, device=self.device
        )

    def validate(self, image_path: str) -> dict:
        """
        Validate an image for face presence using MTCNN.

        Returns:
            {
                "valid": True/False,
                "error": None or error code,
                "message": human-readable message,
                "face_count": int
            }
        """
        try:
            path = Path(image_path)
            if not path.exists() or not path.is_file():
                return {
                    "valid": False,
                    "error": "INVALID_IMAGE",
                    "message": "The uploaded image could not be read.",
                    "face_count": 0
                }

            image = cv2.imread(str(path))
            if image is None:
                return {
                    "valid": False,
                    "error": "INVALID_IMAGE",
                    "message": "The uploaded image could not be read.",
                    "face_count": 0
                }

            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_image)

            # Detect faces
            boxes, _ = self.mtcnn.detect(pil_img)

            if boxes is None or len(boxes) == 0:
                return {
                    "valid": False,
                    "error": "NO_FACE_DETECTED",
                    "message": (
                        "No face was detected in the uploaded image. "
                        "Please upload a clear photo showing your face."
                    ),
                    "face_count": 0
                }

            face_count = len(boxes)

            if face_count > 1:
                return {
                    "valid": False,
                    "error": "MULTIPLE_FACES",
                    "message": (
                        "Multiple faces were detected. "
                        "Please upload a photo containing only one face."
                    ),
                    "face_count": face_count
                }

            return {
                "valid": True,
                "error": None,
                "message": "Face detected successfully.",
                "face_count": 1
            }

        except Exception as e:
            return {
                "valid": False,
                "error": "PROCESS_ERROR",
                "message": f"Could not process the image: {str(e)}",
                "face_count": 0
            }

    def close(self):
        """Cleanup if necessary"""
        pass
