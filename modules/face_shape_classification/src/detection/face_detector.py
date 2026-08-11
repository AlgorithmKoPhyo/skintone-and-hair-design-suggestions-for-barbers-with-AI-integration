import cv2
import mediapipe as mp


class FaceDetector:


    def __init__(self):

        self.face_detection = (
            mp.solutions.face_detection.FaceDetection(
                model_selection=1,
                min_detection_confidence=0.5
            )
        )


    def detect(self, image_path):

        image = cv2.imread(
            str(image_path)
        )


        if image is None:
            raise ValueError(
                f"Cannot read image {image_path}"
            )


        rgb_image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )


        result = self.face_detection.process(
            rgb_image
        )


        if result.detections:

            return True


        return False