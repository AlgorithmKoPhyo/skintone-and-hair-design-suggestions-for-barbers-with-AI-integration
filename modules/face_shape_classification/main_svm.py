from src.training.train_svm import SVMTrainer



def main():


    trainer = SVMTrainer(

        csv_path=
        "data/processed/features.csv",


        model_path=
        "models/svm_face_shape_model.pkl",


        scaler_path=
        "models/svm_scaler.pkl",


        pca_path=
        "models/svm_pca.pkl",


        encoder_path=
        "models/svm_label_encoder.pkl"

    )


    accuracy = trainer.train()


    print(
        f"\nTraining completed. Accuracy: {accuracy:.4f}"
    )



if __name__ == "__main__":

    main()