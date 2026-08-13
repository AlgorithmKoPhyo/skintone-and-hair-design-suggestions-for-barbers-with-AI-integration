# import cv2
# import mediapipe as mp


# class LandmarkExtractor:
#     """
#     Extract facial landmarks using MediaPipe Face Mesh.

#     Output:
#         468 landmarks

#         [
#             (x, y, z),
#             (x, y, z),
#             ...
#         ]
#     """


#     def __init__(self):

#         self.mp_face_mesh = (
#             mp.solutions.face_mesh
#         )


#         self.face_mesh = (
#             self.mp_face_mesh.FaceMesh(
#                 static_image_mode=True,
#                 max_num_faces=1,
#                 refine_landmarks=True,
#                 min_detection_confidence=0.5
#             )
#         )


#     def extract(self, image_path):
#         """
#         Extract landmarks from image.

#         Args:
#             image_path:
#                 path to image

#         Returns:
#             list of tuples or None
#         """


#         image = cv2.imread(
#             str(image_path)
#         )


#         if image is None:
#             raise ValueError(
#                 f"Cannot read image: {image_path}"
#             )


#         # Convert BGR -> RGB
#         rgb_image = cv2.cvtColor(
#             image,
#             cv2.COLOR_BGR2RGB
#         )


#         result = self.face_mesh.process(
#             rgb_image
#         )


#         # no face found
#         if not result.multi_face_landmarks:
#             return None


#         face_landmarks = (
#             result.multi_face_landmarks[0]
#         )


#         landmarks = []


#         for point in face_landmarks.landmark:

#             landmarks.append(
#                 (
#                     point.x,
#                     point.y,
#                     point.z
#                 )
#             )


#         return landmarks

import cv2
import os
import urllib.request
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# -------------------------------------------------------------------
# Mock Classes to trick older files into using the new API
# -------------------------------------------------------------------
class MockFaceMeshResult:
    def __init__(self, multi_face_landmarks):
        self.multi_face_landmarks = multi_face_landmarks

class MockFaceLandmarks:
    def __init__(self, landmarks):
        self.landmark = landmarks

class MockFaceMesh:
    """Acts exactly like the old mp.solutions.face_mesh object so face_shape_classifier doesn't break."""
    def __init__(self, detector):
        self.detector = detector

    def process(self, rgb_image):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        result = self.detector.detect(mp_image)
        
        if not result.face_landmarks:
            return MockFaceMeshResult(None)
            
        multi_face_landmarks = []
        for face in result.face_landmarks:
            multi_face_landmarks.append(MockFaceLandmarks(face))
            
        return MockFaceMeshResult(multi_face_landmarks)

# -------------------------------------------------------------------
# Main LandmarkExtractor Class
# -------------------------------------------------------------------
class LandmarkExtractor:
    """
    Extract facial landmarks using MediaPipe FaceLandmarker (Tasks API).
    """
    def __init__(self):
        # Define where to save the model weights
        self.model_path = os.path.join(os.path.dirname(__file__), 'face_landmarker.task')
        
        # Download the required model file if missing
        if not os.path.exists(self.model_path):
            print("Downloading MediaPipe Face Landmarker model...")
            url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
            try:
                urllib.request.urlretrieve(url, self.model_path)
                print("Download complete!")
            except Exception as e:
                raise RuntimeError(f"Failed to download model: {e}")

        # Configure the FaceLandmarker options
        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            num_faces=1,
            min_face_detection_confidence=0.5
        )
        self.detector = vision.FaceLandmarker.create_from_options(options)
        
        # Create a mock face_mesh so face_shape_classifier.py doesn't crash on line 287
        self.face_mesh = MockFaceMesh(self.detector)

    def extract(self, image_path):
        """
        Extract landmarks from image path.
        """
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Cannot read image: {image_path}")
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Use our mock object to process
        result = self.face_mesh.process(rgb_image)
        if not result.multi_face_landmarks:
            return None
            
        face_landmarks = result.multi_face_landmarks[0]
        landmarks = []
        for point in face_landmarks.landmark:
            landmarks.append((point.x, point.y, point.z))
        return landmarks