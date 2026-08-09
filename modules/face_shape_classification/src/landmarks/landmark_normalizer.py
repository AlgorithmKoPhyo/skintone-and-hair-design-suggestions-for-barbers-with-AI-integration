import numpy as np


class LandmarkNormalizer:
    """
    Normalize MediaPipe landmarks.

    Removes:
    - face position
    - face size
    - camera distance

    Keeps:
    - facial geometry
    """


    def normalize(self, landmarks):

        landmarks = np.array(
            landmarks,
            dtype=np.float32
        )


        # nose center as reference point
        nose = landmarks[168]


        # face scale
        left_face = landmarks[234]
        right_face = landmarks[454]
        chin = landmarks[152]
        forehead = landmarks[10]


        face_width = np.linalg.norm(
            right_face - left_face
        )


        face_height = np.linalg.norm(
            chin - forehead
        )


        if face_width == 0:
            return None


        if face_height == 0:
            return None



        normalized = []


        for point in landmarks:


            x = (
                point[0] - nose[0]
            ) / face_width


            y = (
                point[1] - nose[1]
            ) / face_height


            z = (
                point[2]
            ) / face_width



            normalized.extend(
                [
                    x,
                    y,
                    z
                ]
            )


        return normalized