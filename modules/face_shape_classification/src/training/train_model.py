import pandas as pd

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

import joblib



class ModelTrainer:


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



    def load_data(self):

        df = pd.read_csv(
            self.csv_path
        )


        print(
            "Dataset shape:",
            df.shape
        )


        return df



    def train(self):

        df = self.load_data()



        # -------------------------
        # Split features and labels
        # -------------------------

        X = df.drop(
            "label",
            axis=1
        )


        y = df["label"]



        # Convert text labels
        # Heart -> 0
        # Oval  -> 1
        # etc.

        encoder = LabelEncoder()


        y_encoded = encoder.fit_transform(
            y
        )



        # -------------------------
        # Train / Test split
        # -------------------------

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y_encoded,
            test_size=0.2,
            random_state=42,
            stratify=y_encoded
        )



        # -------------------------
        # Random Forest
        # -------------------------

        model = RandomForestClassifier(
            n_estimators=200,
            random_state=42
        )



        print(
            "Training model..."
        )


        model.fit(
            X_train,
            y_train
        )



        # -------------------------
        # Evaluation
        # -------------------------

        predictions = model.predict(
            X_test
        )


        accuracy = accuracy_score(
            y_test,
            predictions
        )


        print(
            "Accuracy:",
            accuracy
        )



        # -------------------------
        # Save
        # -------------------------

        self.model_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        joblib.dump(
            model,
            self.model_path
        )


        joblib.dump(
            encoder,
            self.encoder_path
        )


        print(
            "Model saved:",
            self.model_path
        )
