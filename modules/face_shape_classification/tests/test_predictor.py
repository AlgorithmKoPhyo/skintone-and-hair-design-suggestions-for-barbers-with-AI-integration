from src.prediction.predictor import FaceShapePredictor



def main():

    predictor = FaceShapePredictor(

        model_path=
        "models/svm_face_shape_model.pkl",

        scaler_path=
        "models/svm_scaler.pkl",

        pca_path=
        "models/svm_pca.pkl",

        encoder_path=
        "models/svm_label_encoder.pkl"

    )


    result = predictor.predict(
        "data/prediction/captured.jpg"
    )


    print(result)



if __name__ == "__main__":
    main()