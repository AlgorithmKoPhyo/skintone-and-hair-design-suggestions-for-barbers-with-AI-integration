import joblib
import pandas as pd

from pathlib import Path


from src.landmarks.landmark_extractor import LandmarkExtractor
from src.landmarks.landmark_normalizer import LandmarkNormalizer

from src.features.feature_calculator import FeatureCalculator




class FaceShapePredictor:


    def __init__(
        self,
        model_path,
        scaler_path,
        pca_path,
        encoder_path
    ):


        self.model = joblib.load(
            Path(model_path)
        )


        self.scaler = joblib.load(
            Path(scaler_path)
        )


        self.pca = joblib.load(
            Path(pca_path)
        )


        self.encoder = joblib.load(
            Path(encoder_path)
        )


        self.landmark_extractor = LandmarkExtractor()


        self.landmark_normalizer = LandmarkNormalizer()


        self.feature_calculator = FeatureCalculator()



    def predict(
        self,
        image_path
    ):


        print(
            "Predicting:",
            image_path
        )



        # =========================
        # Extract landmarks
        # =========================

        landmarks = self.landmark_extractor.extract(
            image_path
        )


        if landmarks is None:

            return {
                "error":
                "No face detected"
            }



        # =========================
        # Geometry features
        # =========================

        features = self.feature_calculator.calculate(
            landmarks
        )



        # =========================
        # Normalized landmarks
        # =========================

        normalized = self.landmark_normalizer.normalize(
            landmarks
        )


        if normalized is None:

            return {
                "error":
                "Normalization failed"
            }



        for index,value in enumerate(normalized):

            features[
                f"landmark_{index}"
            ] = value



        print(
            "Total features:",
            len(features)
        )



        # =========================
        # Convert dataframe
        # =========================

        df = pd.DataFrame(
            [features]
        )



        # =========================
        # Scale
        # =========================

        scaled = self.scaler.transform(
            df
        )



        # =========================
        # PCA
        # =========================

        pca_features = self.pca.transform(
            scaled
        )



        # =========================
        # Predict
        # =========================

        prediction = self.model.predict(
            pca_features
        )


        probability = self.model.predict_proba(
            pca_features
        )



        label = self.encoder.inverse_transform(
            prediction
        )[0]



        confidence = probability.max()



        return {

            "face_shape": label,

            "confidence": float(confidence)

        }