from sklearn.ensemble import RandomForestClassifier
import joblib
import os


def train_and_save_model(X, y, output_path):
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    with open(output_path, "wb") as f:
        joblib.dump(model, f)

    return model
