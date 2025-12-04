import os
import xgboost as xgb

def load_all_models(model_dir="models/trained"):
    models = {}

    for file in os.listdir(model_dir):
        if file.endswith(".model"):
            stat_line = file.replace("xgb_", "").replace(".model", "")
            path = os.path.join(model_dir, file)

            model = xgb.XGBClassifier()
            model.load_model(path)

            models[stat_line] = model

    return models
