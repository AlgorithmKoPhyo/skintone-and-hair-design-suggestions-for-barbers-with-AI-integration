import cv2
import mediapipe as mp


class FaceValidator:
    """
    Validates whether an uploaded image contains a detectable face.

    This class is only responsible for validation.
    It does NOT classify face shape or skin tone.
    """

    def __init__(self, min_detection_confidence: float = 0.5):
        self.min_detection_confidence = min_detection_confidence

        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=self.min_detection_confidence
        )

    def validate(self, image_path: str) -> dict:
        """
        Validate an image for face presence.

        Returns:
            {
                "valid": True/False,
                "error": None or error code,
                "message": human-readable message,
                "face_count": int
            }
        """

        image = cv2.imread(image_path)

        # ---------------------------------------------------------
        # Image could not be loaded
        # ---------------------------------------------------------
        if image is None:
            return {
                "valid": False,
                "error": "INVALID_IMAGE",
                "message": "The uploaded image could not be read.",
                "face_count": 0
            }

        # ---------------------------------------------------------
        # Convert BGR -> RGB for MediaPipe
        # ---------------------------------------------------------
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # ---------------------------------------------------------
        # Detect faces
        # ---------------------------------------------------------
        results = self.face_detection.process(rgb_image)

        if not results.detections:
            return {
                "valid": False,
                "error": "NO_FACE_DETECTED",
                "message": (
                    "No face was detected in the uploaded image. "
                    "Please upload a clear photo showing your face."
                ),
                "face_count": 0
            }

        face_count = len(results.detections)

        # ---------------------------------------------------------
        # Multiple faces
        # ---------------------------------------------------------
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

        # ---------------------------------------------------------
        # Exactly one face
        # ---------------------------------------------------------
        return {
            "valid": True,
            "error": None,
            "message": "Face detected successfully.",
            "face_count": 1
        }

    def close(self):
        """Release MediaPipe resources."""
        self.face_detection.close()