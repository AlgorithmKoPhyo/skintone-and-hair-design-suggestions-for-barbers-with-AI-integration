import cv2
from pathlib import Path

from src.prediction.detector.face_detector import FaceDetector



class WebcamCapture:
    """
    Capture one good face image.

    Flow:

    Webcam
       |
       v
    Face detection
       |
       v
    Check position
       |
       v
    Capture
    """



    def __init__(
        self,
        save_path="data/prediction/captured.jpg"
    ):


        self.save_path = Path(
            save_path
        )


        self.camera = cv2.VideoCapture(1)


        self.detector = FaceDetector()



        if not self.camera.isOpened():

            raise RuntimeError(
                "Cannot open webcam"
            )



    def release(self):

        self.camera.release()

        self.detector.close()

        cv2.destroyAllWindows()



    def put_text(
        self,
        frame,
        text,
        position,
        color
    ):

        cv2.putText(
            frame,
            text,
            position,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )



    def check_posture(
        self,
        bbox,
        frame
    ):


        x, y, w, h = bbox


        frame_h, frame_w, _ = frame.shape



        center_face_x = x + w//2
        center_face_y = y + h//2


        screen_center_x = frame_w//2
        screen_center_y = frame_h//2



        # horizontal position

        if abs(center_face_x-screen_center_x) > frame_w*0.15:

            return False, "Center your face"



        # vertical position

        if abs(center_face_y-screen_center_y) > frame_h*0.15:

            return False, "Move up/down"



        # distance

        if w < frame_w*0.25:

            return False, "Move closer"



        if w > frame_w*0.70:

            return False, "Move back"



        return True, "Face ready"



    def capture(self):


        print(
            "Opening camera..."
        )


        face_ready = False



        while True:


            success, frame = self.camera.read()


            if not success:

                continue



            frame = cv2.flip(
                frame,
                1
            )



            # keep clean image

            original_frame = frame.copy()



            bbox = self.detector.detect_frame(
                frame
            )



            if bbox is None:


                self.put_text(
                    frame,
                    "No face detected",
                    (20,40),
                    (0,0,255)
                )


                face_ready = False



            else:


                x,y,w,h = bbox


                cv2.rectangle(
                    frame,
                    (x,y),
                    (x+w,y+h),
                    (0,255,0),
                    2
                )


                face_ready, message = (
                    self.check_posture(
                        bbox,
                        frame
                    )
                )



                if face_ready:


                    self.put_text(
                        frame,
                        "Face ready",
                        (20,40),
                        (0,255,0)
                    )


                    self.put_text(
                        frame,
                        "SPACE Capture",
                        (20,80),
                        (0,255,0)
                    )


                else:


                    self.put_text(
                        frame,
                        message,
                        (20,40),
                        (0,165,255)
                    )



            cv2.imshow(
                "Face Shape Capture",
                frame
            )



            key = cv2.waitKey(1)



            if key == 32 and face_ready:


                self.save_path.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )


                # save clean frame

                cv2.imwrite(
                    str(self.save_path),
                    original_frame
                )


                print(
                    "Saved:",
                    self.save_path
                )


                break



            elif key == 27:

                self.save_path = None

                break



        self.release()


        return self.save_path