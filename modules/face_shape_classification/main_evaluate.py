from src.training.evaluate import ModelEvaluator



def main():

    evaluator = ModelEvaluator(

        csv_path="data/processed/features.csv",

        model_path="models/face_shape_model.pkl",

        encoder_path="models/label_encoder.pkl"

    )


    evaluator.evaluate()



if __name__ == "__main__":
    main()