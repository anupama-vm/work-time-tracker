import os
import joblib
import pandas as pd

class Classifier:
    def __init__(self, model_path='model/model.joblib'):
        if not os.path.exists(model_path):
            raise FileNotFoundError("Model not found at " + model_path)
        self.model = joblib.load(model_path)
        self.feature_order = [
            "app_name", "idle_time", "keyboard_activity",
            "mouse_activity", "time_of_day"
        ]
        self.label_encoder = self._load_label_encoder()

    def _load_label_encoder(self):
        # Dummy label encoder; update this if you're encoding apps
        return lambda x: x

    def classify(self, features: dict):
        # Fill missing features with default values
        for feat in self.feature_order:
            features.setdefault(feat, 0)

        # Convert to DataFrame
        df = pd.DataFrame([features])[self.feature_order]
        df_encoded = pd.get_dummies(df)

        # Align with model's input shape
        for col in self.model.feature_names_in_:
            if col not in df_encoded.columns:
                df_encoded[col] = 0

        df_encoded = df_encoded[self.model.feature_names_in_]
        prediction = self.model.predict(df_encoded)[0]
        return prediction
