import pandas as pd
import joblib

from pathlib import Path


from sklearn.model_selection import (
    train_test_split,
    GridSearchCV
)


from sklearn.preprocessing import (
    LabelEncoder,
    StandardScaler
)


from sklearn.decomposition import PCA


from sklearn.svm import SVC


from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)




class SVMTrainer:
    """
    Train Face Shape Classification model.

    Pipeline:

    CSV
      |
      v
    LabelEncoder
      |
      v
    Train/Test Split
      |
      v
    StandardScaler
      |
      v
    PCA
      |
      v
    GridSearchCV
      |
      v
    Best SVM RBF
      |
      v
    Save:

        svm_model.pkl
        scaler.pkl
        pca.pkl
        encoder.pkl
    """



    def __init__(
        self,
        csv_path,
        model_path,
        scaler_path,
        pca_path,
        encoder_path
    ):


        self.csv_path = Path(csv_path)

        self.model_path = Path(model_path)

        self.scaler_path = Path(scaler_path)

        self.pca_path = Path(pca_path)

        self.encoder_path = Path(encoder_path)




    def train(self):


        # ==================================
        # Load dataset
        # ==================================

        df = pd.read_csv(
            self.csv_path
        )


        print(
            "\nDataset:",
            df.shape
        )



        X = df.drop(
            "label",
            axis=1
        )


        y = df["label"]



        print(
            "\nFeature count:",
            len(X.columns)
        )



        # ==================================
        # Label encoding
        # ==================================

        encoder = LabelEncoder()


        y_encoded = encoder.fit_transform(
            y
        )


        print(
            "\nClasses:"
        )


        for i, name in enumerate(
            encoder.classes_
        ):

            print(
                i,
                "->",
                name
            )



        # ==================================
        # Train Test Split
        # ==================================

        X_train, X_test, y_train, y_test = train_test_split(

            X,

            y_encoded,

            test_size=0.2,

            random_state=42,

            stratify=y_encoded

        )



        # ==================================
        # Feature Scaling
        # ==================================

        scaler = StandardScaler()


        X_train_scaled = scaler.fit_transform(
            X_train
        )


        X_test_scaled = scaler.transform(
            X_test
        )


        print(
            "\nAfter scaling:",
            X_train_scaled.shape
        )



        # ==================================
        # PCA
        # ==================================

        pca = PCA(
            n_components=200,
            random_state=42
        )


        X_train_pca = pca.fit_transform(
            X_train_scaled
        )


        X_test_pca = pca.transform(
            X_test_scaled
        )



        print(
            "After PCA:",
            X_train_pca.shape
        )


        print(
            "Explained variance:",
            sum(
                pca.explained_variance_ratio_
            )
        )



        # ==================================
        # Grid Search SVM
        # ==================================

        svm = SVC(
            probability=True,
            class_weight="balanced"
        )



        param_grid = {


            "kernel":[
                "rbf"
            ],


            "C":[
                1,
                10,
                50,
                100,
                200
            ],


            "gamma":[
                "scale",
                "auto",
                0.001,
                0.01,
                0.1
            ]

        }



        grid = GridSearchCV(

            estimator=svm,

            param_grid=param_grid,

            cv=5,

            scoring="accuracy",

            n_jobs=-1,

            verbose=2

        )



        print(
            "\nSearching best SVM parameters..."
        )



        grid.fit(

            X_train_pca,

            y_train

        )



        model = grid.best_estimator_



        print(
            "\nBest Parameters:"
        )


        print(
            grid.best_params_
        )



        # ==================================
        # Evaluation
        # ==================================

        predictions = model.predict(
            X_test_pca
        )



        accuracy = accuracy_score(

            y_test,

            predictions

        )



        print(
            "\nSVM Accuracy:",
            accuracy
        )



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



        print(
            "\nConfusion Matrix:"
        )


        print(

            confusion_matrix(

                y_test,

                predictions

            )

        )



        # ==================================
        # Save files
        # ==================================

        self.model_path.parent.mkdir(

            parents=True,

            exist_ok=True

        )


        joblib.dump(

            model,

            self.model_path

        )


        joblib.dump(

            scaler,

            self.scaler_path

        )


        joblib.dump(

            pca,

            self.pca_path

        )


        joblib.dump(

            encoder,

            self.encoder_path

        )



        print(
            "\nSaved:"
        )


        print(
            "Model:",
            self.model_path
        )


        print(
            "Scaler:",
            self.scaler_path
        )


        print(
            "PCA:",
            self.pca_path
        )


        print(
            "Encoder:",
            self.encoder_path
        )



        return accuracy