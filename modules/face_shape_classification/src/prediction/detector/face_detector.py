import cv2
import mediapipe as mp


class FaceDetector:
    """
    Face detection using MediaPipe.

    Used for:
    1. Dataset image checking
    2. Webcam face detection
    """


    def __init__(self):

        self.face_detection = (
            mp.solutions.face_detection.FaceDetection(
                model_selection=1,
                min_detection_confidence=0.6
            )
        )



    def process(self, frame):
        """
        Run MediaPipe detection.

        Returns:
            MediaPipe result
            or None
        """


        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        result = self.face_detection.process(
            rgb
        )


        if not result.detections:

            return None


        return result



    def detect(self, image_path):
        """
        Detect face from image path.

        Used during dataset processing.

        Returns:
            True / False
        """


        image = cv2.imread(
            str(image_path)
        )


        if image is None:

            return False



        result = self.process(
            image
        )


        return result is not None



    def detect_frame(self, frame):
        """
        Detect face from webcam frame.

        Returns:

            (
                x,
                y,
                width,
                height
            )

            or

            None
        """


        result = self.process(
            frame
        )


        if result is None:

            return None



        detection = (
            result
            .detections[0]
        )


        bbox = (
            detection
            .location_data
            .relative_bounding_box
        )


        frame_height, frame_width, _ = frame.shape



        x = int(
            bbox.xmin * frame_width
        )


        y = int(
            bbox.ymin * frame_height
        )


        width = int(
            bbox.width * frame_width
        )


        height = int(
            bbox.height * frame_height
        )



        # prevent negative values

        x = max(
            0,
            x
        )

        y = max(
            0,
            y
        )



        return (
            x,
            y,
            width,
            height
        )



    def close(self):

        self.face_detection.close()