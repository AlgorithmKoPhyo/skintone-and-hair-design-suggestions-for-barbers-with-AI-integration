import math

from src.landmarks.landmark_indices import (

    # Vertical
    FOREHEAD_TOP,
    CHIN,

    # Widths
    LEFT_FACE_EDGE,
    RIGHT_FACE_EDGE,

    LEFT_CHEEKBONE,
    RIGHT_CHEEKBONE,

    LEFT_JAW,
    RIGHT_JAW,

    LEFT_CHIN,
    RIGHT_CHIN,

    LEFT_TEMPLE,
    RIGHT_TEMPLE,


    # Face thirds
    NOSE_BRIDGE,
    MOUTH_BOTTOM,


    # Jaw angle
    LEFT_JAW_ANGLE,
    RIGHT_JAW_ANGLE,


    # Contours
    LEFT_JAW_CONTOUR,
    RIGHT_JAW_CONTOUR,

    LEFT_CHEEK_CONTOUR,
    RIGHT_CHEEK_CONTOUR,

    LEFT_FOREHEAD_CONTOUR,
    RIGHT_FOREHEAD_CONTOUR,

    LEFT_CHIN_CONTOUR,
    RIGHT_CHIN_CONTOUR,


    # Symmetry
    LEFT_CHEEK_CENTER,
    RIGHT_CHEEK_CENTER,
)



class FeatureCalculator:
    """
    Extract geometric face shape features
    from MediaPipe Face Mesh landmarks.

    Features:
    - face dimensions
    - width ratios
    - face proportions
    - jaw angles
    - contour curvature
    - symmetry
    """



    def distance(self, p1, p2):
        """
        Euclidean distance between
        two 3D MediaPipe landmarks.
        """

        x1, y1, z1 = p1
        x2, y2, z2 = p2


        return math.sqrt(
            (x2 - x1) ** 2 +
            (y2 - y1) ** 2 +
            (z2 - z1) ** 2
        )



    def safe_ratio(self, a, b):
        """
        Safe division.
        """

        if b == 0:
            return 0

        return a / b



    def calculate_angle(self, a, b, c):
        """
        Calculate angle ABC.

        Used for jaw sharpness.
        """

        ba = (
            a[0] - b[0],
            a[1] - b[1]
        )


        bc = (
            c[0] - b[0],
            c[1] - b[1]
        )


        dot = (
            ba[0] * bc[0] +
            ba[1] * bc[1]
        )


        magnitude = (
            math.sqrt(
                ba[0] ** 2 +
                ba[1] ** 2
            )
            *
            math.sqrt(
                bc[0] ** 2 +
                bc[1] ** 2
            )
        )


        if magnitude == 0:
            return 0


        cosine = dot / magnitude


        cosine = max(
            -1,
            min(1, cosine)
        )


        return math.degrees(
            math.acos(cosine)
        )



    def contour_length(
        self,
        landmarks,
        points
    ):
        """
        Calculate contour curve length.
        """

        total = 0


        for i in range(
            len(points)-1
        ):

            total += self.distance(
                landmarks[points[i]],
                landmarks[points[i+1]]
            )


        return total



    def calculate(self, landmarks):

        features = {}



        # =================================================
        # Basic face measurements
        # =================================================


        face_height = self.distance(
            landmarks[FOREHEAD_TOP],
            landmarks[CHIN]
        )


        face_width = self.distance(
            landmarks[LEFT_FACE_EDGE],
            landmarks[RIGHT_FACE_EDGE]
        )


        cheekbone_width = self.distance(
            landmarks[LEFT_CHEEKBONE],
            landmarks[RIGHT_CHEEKBONE]
        )


        jaw_width = self.distance(
            landmarks[LEFT_JAW],
            landmarks[RIGHT_JAW]
        )


        chin_width = self.distance(
            landmarks[LEFT_CHIN],
            landmarks[RIGHT_CHIN]
        )


        forehead_width = self.distance(
            landmarks[LEFT_TEMPLE],
            landmarks[RIGHT_TEMPLE]
        )



        features.update({

            "face_height": face_height,

            "face_width": face_width,

            "cheekbone_width": cheekbone_width,

            "jaw_width": jaw_width,

            "chin_width": chin_width,

            "forehead_width": forehead_width

        })



        # =================================================
        # Width ratios
        # =================================================


        features["face_width_height_ratio"] = (
            self.safe_ratio(
                face_width,
                face_height
            )
        )


        features["face_elongation"] = (
            self.safe_ratio(
                face_height,
                face_width
            )
        )


        features["jaw_face_ratio"] = (
            self.safe_ratio(
                jaw_width,
                face_width
            )
        )


        features["cheek_face_ratio"] = (
            self.safe_ratio(
                cheekbone_width,
                face_width
            )
        )


        features["forehead_face_ratio"] = (
            self.safe_ratio(
                forehead_width,
                face_width
            )
        )


        features["jaw_cheek_ratio"] = (
            self.safe_ratio(
                jaw_width,
                cheekbone_width
            )
        )


        features["forehead_jaw_ratio"] = (
            self.safe_ratio(
                forehead_width,
                jaw_width
            )
        )


        features["cheek_jaw_ratio"] = (
            self.safe_ratio(
                cheekbone_width,
                jaw_width
            )
        )


        features["chin_jaw_ratio"] = (
            self.safe_ratio(
                chin_width,
                jaw_width
            )
        )



        # =================================================
        # Shape specific ratios
        # =================================================


        # Heart:
        # large forehead + narrow jaw

        features["face_taper_ratio"] = (

            self.safe_ratio(
                forehead_width - jaw_width,
                face_width
            )

        )



        # Narrow chin detection

        features["chin_taper_ratio"] = (

            self.safe_ratio(
                cheekbone_width - chin_width,
                cheekbone_width
            )

        )



        # Diamond:
        # cheekbone wider than forehead

        features["cheek_forehead_ratio"] = (

            self.safe_ratio(
                cheekbone_width,
                forehead_width
            )

        )



        features["lower_face_strength"] = (

            self.safe_ratio(
                jaw_width + chin_width,
                face_width
            )

        )



        # =================================================
        # Face thirds
        # =================================================


        upper_face = self.distance(
            landmarks[FOREHEAD_TOP],
            landmarks[NOSE_BRIDGE]
        )


        middle_face = self.distance(
            landmarks[NOSE_BRIDGE],
            landmarks[MOUTH_BOTTOM]
        )


        lower_face = self.distance(
            landmarks[MOUTH_BOTTOM],
            landmarks[CHIN]
        )



        features["upper_face_ratio"] = (

            self.safe_ratio(
                upper_face,
                face_height
            )

        )


        features["middle_face_ratio"] = (

            self.safe_ratio(
                middle_face,
                face_height
            )

        )


        features["lower_face_ratio"] = (

            self.safe_ratio(
                lower_face,
                face_height
            )

        )



        # =================================================
        # Jaw angles
        # =================================================


        left_jaw_angle = self.calculate_angle(

            landmarks[LEFT_FACE_EDGE],

            landmarks[LEFT_JAW_ANGLE],

            landmarks[CHIN]

        )


        right_jaw_angle = self.calculate_angle(

            landmarks[RIGHT_FACE_EDGE],

            landmarks[RIGHT_JAW_ANGLE],

            landmarks[CHIN]

        )



        features["left_jaw_angle"] = left_jaw_angle

        features["right_jaw_angle"] = right_jaw_angle



        features["jaw_angle_average"] = (

            left_jaw_angle +
            right_jaw_angle

        ) / 2



        features["jaw_angle_difference"] = abs(

            left_jaw_angle -
            right_jaw_angle

        )



        # =================================================
        # Contour curvature
        # =================================================


        jaw_left = self.contour_length(
            landmarks,
            LEFT_JAW_CONTOUR
        )


        jaw_right = self.contour_length(
            landmarks,
            RIGHT_JAW_CONTOUR
        )


        features["jaw_curve_ratio"] = (

            self.safe_ratio(
                jaw_left,
                jaw_right
            )

        )



        cheek_left = self.contour_length(
            landmarks,
            LEFT_CHEEK_CONTOUR
        )


        cheek_right = self.contour_length(
            landmarks,
            RIGHT_CHEEK_CONTOUR
        )


        features["cheek_curve_ratio"] = (

            self.safe_ratio(
                cheek_left,
                cheek_right
            )

        )



        forehead_left = self.contour_length(
            landmarks,
            LEFT_FOREHEAD_CONTOUR
        )


        forehead_right = self.contour_length(
            landmarks,
            RIGHT_FOREHEAD_CONTOUR
        )


        features["forehead_curve_ratio"] = (

            self.safe_ratio(
                forehead_left,
                forehead_right
            )

        )



        chin_left = self.contour_length(
            landmarks,
            LEFT_CHIN_CONTOUR
        )


        chin_right = self.contour_length(
            landmarks,
            RIGHT_CHIN_CONTOUR
        )


        features["chin_curve_ratio"] = (

            self.safe_ratio(
                chin_left,
                chin_right
            )

        )



        # =================================================
        # Symmetry
        # =================================================


        left_face = self.distance(

            landmarks[LEFT_FACE_EDGE],

            landmarks[LEFT_CHEEK_CENTER]

        )


        right_face = self.distance(

            landmarks[RIGHT_FACE_EDGE],

            landmarks[RIGHT_CHEEK_CENTER]

        )



        features["face_symmetry"] = (

            self.safe_ratio(
                left_face,
                right_face
            )

        )


        return features