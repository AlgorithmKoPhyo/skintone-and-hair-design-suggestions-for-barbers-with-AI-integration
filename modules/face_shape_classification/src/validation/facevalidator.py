# # app/services/validator.py

# import cv2
# import mediapipe as mp


# class FaceValidator:
#     """
#     Validates whether an uploaded image contains a detectable face.

#     This class is only responsible for validation.
#     It does NOT classify face shape or skin tone.
#     """

#     def __init__(self, min_detection_confidence: float = 0.5):
#         self.min_detection_confidence = min_detection_confidence

#         self.mp_face_detection = mp.solutions.face_detection
#         self.face_detection = self.mp_face_detection.FaceDetection(
#             model_selection=1,
#             min_detection_confidence=self.min_detection_confidence
#         )

#     def validate(self, image_path: str) -> dict:
#         """
#         Validate an image for face presence.

#         Returns:
#             {
#                 "valid": True/False,
#                 "error": None or error code,
#                 "message": human-readable message,
#                 "face_count": int
#             }
#         """

#         image = cv2.imread(image_path)

#         # ---------------------------------------------------------
#         # Image could not be loaded
#         # ---------------------------------------------------------
#         if image is None:
#             return {
#                 "valid": False,
#                 "error": "INVALID_IMAGE",
#                 "message": "The uploaded image could not be read.",
#                 "face_count": 0
#             }

#         # ---------------------------------------------------------
#         # Convert BGR -> RGB for MediaPipe
#         # ---------------------------------------------------------
#         rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#         # ---------------------------------------------------------
#         # Detect faces
#         # ---------------------------------------------------------
#         results = self.face_detection.process(rgb_image)

#         if not results.detections:
#             return {
#                 "valid": False,
#                 "error": "NO_FACE_DETECTED",
#                 "message": (
#                     "No face was detected in the uploaded image. "
#                     "Please upload a clear photo showing your face."
#                 ),
#                 "face_count": 0
#             }

#         face_count = len(results.detections)

#         # ---------------------------------------------------------
#         # Multiple faces
#         # ---------------------------------------------------------
#         if face_count > 1:
#             return {
#                 "valid": False,
#                 "error": "MULTIPLE_FACES",
#                 "message": (
#                     "Multiple faces were detected. "
#                     "Please upload a photo containing only one face."
#                 ),
#                 "face_count": face_count
#             }

#         # ---------------------------------------------------------
#         # Exactly one face
#         # ---------------------------------------------------------
#         return {
#             "valid": True,
#             "error": None,
#             "message": "Face detected successfully.",
#             "face_count": 1
#         }

#     def close(self):
#         """Release MediaPipe resources."""
#         self.face_detection.close()


# import cv2
# import os
# import urllib.request
# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision


# class FaceValidator:
#     """
#     Validates whether an uploaded image contains a detectable face.

#     This class is only responsible for validation.
#     It does NOT classify face shape or skin tone.
#     """

#     def __init__(self, min_detection_confidence: float = 0.5):
#         self.min_detection_confidence = min_detection_confidence

#         # Define where to save the model weights in the same directory
#         self.model_path = os.path.join(os.path.dirname(__file__), 'blaze_face_short_range.tflite')
        
#         # Automatically download the required model file if it's missing
#         if not os.path.exists(self.model_path):
#             print("Downloading MediaPipe Face Detector model for Validator...")
#             url = "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite"
#             try:
#                 urllib.request.urlretrieve(url, self.model_path)
#                 print("Download complete!")
#             except Exception as e:
#                 raise RuntimeError(f"Failed to download model: {e}")

#         # Configure the FaceDetector options
#         base_options = python.BaseOptions(model_asset_path=self.model_path)
#         options = vision.FaceDetectorOptions(
#             base_options=base_options,
#             min_detection_confidence=self.min_detection_confidence
#         )
#         self.detector = vision.FaceDetector.create_from_options(options)

#     def validate(self, image_path: str) -> dict:
#         """
#         Validate an image for face presence.

#         Returns:
#             {
#                 "valid": True/False,
#                 "error": None or error code,
#                 "message": human-readable message,
#                 "face_count": int
#             }
#         """

#         image = cv2.imread(image_path)

#         # ---------------------------------------------------------
#         # Image could not be loaded
#         # ---------------------------------------------------------
#         if image is None:
#             return {
#                 "valid": False,
#                 "error": "INVALID_IMAGE",
#                 "message": "The uploaded image could not be read.",
#                 "face_count": 0
#             }

#         # ---------------------------------------------------------
#         # Convert BGR -> RGB for MediaPipe
#         # ---------------------------------------------------------
#         rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
#         # Create MediaPipe Image object required by the new Tasks API
#         mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

#         # ---------------------------------------------------------
#         # Detect faces
#         # ---------------------------------------------------------
#         try:
#             results = self.detector.detect(mp_image)
#         except Exception as e:
#             return {
#                 "valid": False,
#                 "error": "DETECTION_ERROR",
#                 "message": f"An error occurred during face detection: {str(e)}",
#                 "face_count": 0
#             }

#         if not results.detections:
#             return {
#                 "valid": False,
#                 "error": "NO_FACE_DETECTED",
#                 "message": (
#                     "No face was detected in the uploaded image. "
#                     "Please upload a clear photo showing your face."
#                 ),
#                 "face_count": 0
#             }

#         face_count = len(results.detections)

#         # ---------------------------------------------------------
#         # Multiple faces
#         # ---------------------------------------------------------
#         if face_count > 1:
#             return {
#                 "valid": False,
#                 "error": "MULTIPLE_FACES",
#                 "message": (
#                     "Multiple faces were detected. "
#                     "Please upload a photo containing only one face."
#                 ),
#                 "face_count": face_count
#             }

#         # ---------------------------------------------------------
#         # Exactly one face
#         # ---------------------------------------------------------
#         return {
#             "valid": True,
#             "error": None,
#             "message": "Face detected successfully.",
#             "face_count": 1
#         }

#     def close(self):
#         """Release MediaPipe resources."""
#         if hasattr(self, 'detector'):
#             self.detector.close()



import cv2
import os
import urllib.request
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class FaceValidator:
    """
    Validates whether an uploaded image contains a detectable face.

    This class is only responsible for validation.
    It does NOT classify face shape or skin tone.
    """

    def __init__(self, min_detection_confidence: float = 0.5, allow_multiple_faces: bool = True):
        self.min_detection_confidence = min_detection_confidence
        # Set to True to temporarily allow images with more than 1 face
        self.allow_multiple_faces = allow_multiple_faces

        # Define where to save the model weights in the same directory
        self.model_path = os.path.join(os.path.dirname(__file__), 'blaze_face_short_range.tflite')
        
        # Automatically download the required model file if it's missing
        if not os.path.exists(self.model_path):
            print("Downloading MediaPipe Face Detector model for Validator...")
            url = "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite"
            try:
                urllib.request.urlretrieve(url, self.model_path)
                print("Download complete!")
            except Exception as e:
                raise RuntimeError(f"Failed to download model: {e}")

        # Configure the FaceDetector options
        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.FaceDetectorOptions(
            base_options=base_options,
            min_detection_confidence=self.min_detection_confidence
        )
        self.detector = vision.FaceDetector.create_from_options(options)

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
        
        # Create MediaPipe Image object required by the new Tasks API
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        # ---------------------------------------------------------
        # Detect faces
        # ---------------------------------------------------------
        try:
            results = self.detector.detect(mp_image)
        except Exception as e:
            return {
                "valid": False,
                "error": "DETECTION_ERROR",
                "message": f"An error occurred during face detection: {str(e)}",
                "face_count": 0
            }

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
        # Multiple faces (Disabled temporarily when allow_multiple_faces=True)
        # ---------------------------------------------------------
        if face_count > 1 and not self.allow_multiple_faces:
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
        # Valid face presence
        # ---------------------------------------------------------
        return {
            "valid": True,
            "error": None,
            "message": f"{face_count} face(s) detected successfully.",
            "face_count": face_count
        }

    def close(self):
        """Release MediaPipe resources."""
        if hasattr(self, 'detector'):
            self.detector.close()