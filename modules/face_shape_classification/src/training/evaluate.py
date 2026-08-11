import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)



class ModelEvaluator:


    def __init__(
        self,
        csv_path,
        model_path,
        encoder_path
    ):

        self.csv_path = Path(csv_path)

        self.model_path = Path(model_path)

        self.encoder_path = Path(
            encoder_path
        )



    def evaluate(self):

        # -------------------------
        # Load dataset
        # -------------------------

        df = pd.read_csv(
            self.csv_path
        )


        X = df.drop(
            "label",
            axis=1
        )


        y = df["label"]



        # -------------------------
        # Load encoder
        # -------------------------

        encoder = joblib.load(
            self.encoder_path
        )


        y_encoded = encoder.transform(
            y
        )



        # -------------------------
        # Same split as training
        # -------------------------

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y_encoded,
            test_size=0.2,
            random_state=42,
            stratify=y_encoded
        )



        # -------------------------
        # Load model
        # -------------------------

        model = joblib.load(
            self.model_path
        )



        # -------------------------
        # Prediction
        # -------------------------

        predictions = model.predict(
            X_test
        )



        # -------------------------
        # Accuracy
        # -------------------------

        accuracy = accuracy_score(
            y_test,
            predictions
        )


        print(
            "\nAccuracy:",
            accuracy
        )



        # -------------------------
        # Classification report
        # -------------------------

        print(
            "\nClassification Report:"
        )


        print(
            classification_report(
                y_test,
                predictions,
                target_names=encoder.classes_
            )
        )



        # -------------------------
        # Confusion matrix
        # -------------------------

        print(
            "\nConfusion Matrix:"
        )


        matrix = confusion_matrix(
            y_test,
            predictions
        )


        print(matrix)

        importances = model.feature_importances_

        for name, importance in zip(
              X.columns,
              importances
        ):
             print(
                name,
                importance
         )