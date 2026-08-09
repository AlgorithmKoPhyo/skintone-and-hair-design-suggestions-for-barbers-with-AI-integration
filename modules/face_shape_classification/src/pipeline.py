from pathlib import Path

from src.dataset.dataset_loader import DatasetLoader
from src.detection.face_detector import FaceDetector
from src.landmarks.landmark_extractor import LandmarkExtractor
from src.landmarks.landmark_normalizer import LandmarkNormalizer

from src.features.feature_calculator import FeatureCalculator

from src.training.csv_generator import CSVGenerator
from src.training.train_svm import SVMTrainer



class FaceShapePipeline:
    """
    Complete face shape training pipeline.

    Flow:

    Images
      |
      v
    Face Detection
      |
      v
    MediaPipe Landmarks
      |
      +----------------+
      |                |
      v                v
    Geometric      Normalized
    Features       Landmarks
      |                |
      +-------+--------+
              |
              v
          CSV Dataset
              |
              v
             SVM
    """



    def __init__(
        self,
        dataset_path,
        output_csv,
        model_path,
        scaler_path,
        encoder_path,
    ):


        self.dataset_path = Path(
            dataset_path
        )


        self.loader = DatasetLoader(
            self.dataset_path
        )


        self.detector = FaceDetector()



        self.landmark_extractor = LandmarkExtractor()



        self.landmark_normalizer = LandmarkNormalizer()



        self.feature_calculator = FeatureCalculator()



        self.csv_generator = CSVGenerator(
            output_csv
        )



        self.model_trainer = SVMTrainer(

            csv_path=output_csv,

            model_path=model_path,

            scaler_path=scaler_path,

            pca_path="models/svm_pca.pkl",

            encoder_path=encoder_path

        )



    def run(self):


        print(
            "Starting pipeline..."
        )



        images = self.loader.load_images()



        print(
            f"Total images found: {len(images)}"
        )



        feature_dataset = []



        success = 0

        failed = 0



        for image_path, label in images:



            print(
                "\nProcessing:"
            )


            print(
                image_path
            )


            print(
                "Label:",
                label
            )



            # ==================================
            # 1. Face Detection
            # ==================================

            detected = self.detector.detect(
                image_path
            )



            if not detected:


                print(
                    "No face detected"
                )


                failed += 1

                continue




            # ==================================
            # 2. Extract Landmarks
            # ==================================

            landmarks = (
                self.landmark_extractor.extract(
                    image_path
                )
            )



            if landmarks is None:


                print(
                    "Landmark extraction failed"
                )


                failed += 1

                continue




            print(
                "Landmarks:",
                len(landmarks)
            )




            # ==================================
            # 3. Normalize Landmarks
            # ==================================

            normalized_landmarks = (

                self.landmark_normalizer.normalize(
                    landmarks
                )

            )



            if normalized_landmarks is None:


                print(
                    "Normalization failed"
                )


                failed += 1

                continue




            # ==================================
            # 4. Calculate Geometric Features
            # ==================================

            features = (

                self.feature_calculator.calculate(
                    landmarks
                )

            )




            # ==================================
            # 5. Add normalized landmarks
            # ==================================

            for index, value in enumerate(
                normalized_landmarks
            ):


                features[
                    f"landmark_{index}"
                ] = value




            # ==================================
            # Add Label
            # ==================================

            features["label"] = label




            feature_dataset.append(
                features
            )


            success += 1




        print(
            "\n========== RESULT =========="
        )


        print(
            "Successful:",
            success
        )


        print(
            "Failed:",
            failed
        )




        # ==================================
        # 6. Save CSV
        # ==================================

        self.csv_generator.save(
            feature_dataset
        )




        print(
            "\nTraining SVM model..."
        )



        accuracy = (
            self.model_trainer.train()
        )



        print(
            f"\nTraining completed. Accuracy: {accuracy:.4f}"
        )