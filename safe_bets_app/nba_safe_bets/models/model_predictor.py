import xgboost as xgb
import pandas as pd
from models.feature_selector import select_features

def load_model(path):
    model = xgb.XGBClassifier()
    model.load_model(path)
    return model

def predict_model(model, df):
    X = select_features(df)
    proba = model.predict_proba(X)[:, 1]
    return proba
