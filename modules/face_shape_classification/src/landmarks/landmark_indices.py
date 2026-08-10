"""
MediaPipe Face Mesh landmark indexes for face shape classification.

Based on MediaPipe 468/478 Face Mesh topology.

Features extracted:
- Face dimensions
- Forehead width
- Cheekbone width
- Jaw structure
- Chin shape
- Face thirds
- Jaw angles
- Face contour curvature
- Symmetry

"""


# ==================================================
# Vertical face measurements
# ==================================================

FOREHEAD_TOP = 10
CHIN = 152



# ==================================================
# Maximum face width
# ==================================================

LEFT_FACE_EDGE = 234
RIGHT_FACE_EDGE = 454



# ==================================================
# Cheekbone / zygomatic width
# ==================================================

LEFT_CHEEKBONE = 116
RIGHT_CHEEKBONE = 345



# ==================================================
# Jaw width
# ==================================================

LEFT_JAW = 132
RIGHT_JAW = 361



# ==================================================
# Chin width
# ==================================================

LEFT_CHIN = 148
RIGHT_CHIN = 377



# ==================================================
# Forehead / temple width
# ==================================================

LEFT_TEMPLE = 103
RIGHT_TEMPLE = 332



# ==================================================
# Face vertical sections
# ==================================================

NOSE_BRIDGE = 168
NOSE_BOTTOM = 2

MOUTH_TOP = 13
MOUTH_BOTTOM = 14



# ==================================================
# Jaw angle points
# Used to distinguish:
#
# Square:
# sharp jaw angle
#
# Round:
# smooth jaw angle
# ==================================================

LEFT_JAW_ANGLE = 172
RIGHT_JAW_ANGLE = 397



# ==================================================
# Jaw contour
# Used for jaw curvature
# ==================================================

LEFT_JAW_CONTOUR = [
    234,
    93,
    132,
    58,
    172
]


RIGHT_JAW_CONTOUR = [
    454,
    323,
    361,
    288,
    397
]



# ==================================================
# Cheek contour
# Used for cheekbone prominence
#
# Diamond:
# wider cheek area
#
# Oval:
# balanced cheek area
# ==================================================

LEFT_CHEEK_CONTOUR = [
    234,
    93,
    116,
    117,
    118
]


RIGHT_CHEEK_CONTOUR = [
    454,
    323,
    345,
    346,
    347
]



# ==================================================
# Forehead contour
# Used for forehead shape
#
# Heart:
# wider upper face
# ==================================================

LEFT_FOREHEAD_CONTOUR = [
    103,
    104,
    69,
    67
]


RIGHT_FOREHEAD_CONTOUR = [
    332,
    333,
    299,
    297
]



# ==================================================
# Chin contour
# Used for chin shape
#
# Heart:
# narrow chin
#
# Square:
# wider chin
# ==================================================

LEFT_CHIN_CONTOUR = [
    172,
    136,
    150,
    149
]


RIGHT_CHIN_CONTOUR = [
    397,
    365,
    379,
    378
]



# ==================================================
# Face symmetry points
# ==================================================

LEFT_CHEEK_CENTER = 205
RIGHT_CHEEK_CENTER = 425



# ==================================================
# Face center line
# Used for symmetry calculations
# ==================================================

FACE_CENTER = [
    10,
    168,
    1,
    152
]