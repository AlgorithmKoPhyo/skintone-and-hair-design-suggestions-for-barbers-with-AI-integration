from src.training.train_model import ModelTrainer



def main():


    trainer = ModelTrainer(

        "data/processed/features.csv",

        "models/face_shape_model.pkl",

        "models/label_encoder.pkl"

    )


    trainer.train()



if __name__ == "__main__":
    main()