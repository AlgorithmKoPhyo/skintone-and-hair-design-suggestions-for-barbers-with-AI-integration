import cv2
import mediapipe as mp


class LandmarkExtractor:
    """
    Extract facial landmarks using MediaPipe Face Mesh.

    Output:
        468 landmarks

        [
            (x, y, z),
            (x, y, z),
            ...
        ]
    """


    def __init__(self):

        self.mp_face_mesh = (
            mp.solutions.face_mesh
        )


        self.face_mesh = (
            self.mp_face_mesh.FaceMesh(
                static_image_mode=True,
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5
            )
        )


    def extract(self, image_path):
        """
        Extract landmarks from image.

        Args:
            image_path:
                path to image

        Returns:
            list of tuples or None
        """


        image = cv2.imread(
            str(image_path)
        )


        if image is None:
            raise ValueError(
                f"Cannot read image: {image_path}"
            )


        # Convert BGR -> RGB
        rgb_image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )


        result = self.face_mesh.process(
            rgb_image
        )


        # no face found
        if not result.multi_face_landmarks:
            return None


        face_landmarks = (
            result.multi_face_landmarks[0]
        )


        landmarks = []


        for point in face_landmarks.landmark:

            landmarks.append(
                (
                    point.x,
                    point.y,
                    point.z
                )
            )


        return landmarks
