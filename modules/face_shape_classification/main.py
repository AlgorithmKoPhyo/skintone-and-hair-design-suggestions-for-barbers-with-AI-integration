from src.pipeline import FaceShapePipeline


def main():

    pipeline = FaceShapePipeline(

        dataset_path="data/raw/training_set",

        output_csv="data/processed/features.csv",

        model_path="models/svm_face_shape_model.pkl",

        scaler_path="models/svm_scaler.pkl",

        encoder_path="models/svm_label_encoder.pkl",

    )

    pipeline.run()


if __name__ == "__main__":
    main()