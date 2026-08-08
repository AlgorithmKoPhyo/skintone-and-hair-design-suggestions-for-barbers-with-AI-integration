from __future__ import annotations
from pathlib import Path
import joblib
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "undertone_model.pkl"
ENCODER_PATH = BASE_DIR / "models" / "label_encoder.pkl"

class UndertoneModelNotFoundError(Exception):
    pass

class UndertoneClassifier:
    def __init__(self, model_path: Path = MODEL_PATH, encoder_path: Path = ENCODER_PATH):
        self.model_path = model_path
        self.encoder_path = encoder_path
        self.model = None
        self.label_encoder = None

    def load(self) -> None:
        if not self.model_path.exists() or not self.encoder_path.exists():
            raise UndertoneModelNotFoundError("Model files not found.")
        self.model = joblib.load(self.model_path)
        self.label_encoder = joblib.load(self.encoder_path)

    @property
    def is_loaded(self) -> bool:
        return self.model is not None and self.label_encoder is not None

    def predict(self, feature_vector_24d: list[float] | np.ndarray) -> dict[str, float | str | dict[str, float]]:
        if not self.is_loaded:
            raise RuntimeError("Undertone classifier is not loaded.")

        X = np.array(feature_vector_24d).reshape(1, -1)
        pred_label_idx = self.model.predict(X)[0]
        predicted_class = str(self.label_encoder.inverse_transform([pred_label_idx])[0])

        probabilities = {}
        classes = [str(c) for c in self.label_encoder.classes_]

        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(X)[0]
            for idx, cls in enumerate(classes):
                probabilities[cls] = round(float(probs[idx]), 4)
        else:
            for cls in classes:
                probabilities[cls] = 1.0 if cls == predicted_class else 0.0

        return {
            "undertone": predicted_class,
            "probabilities": probabilities,
            "feature_vector": [round(float(v), 4) for v in feature_vector_24d]
        }