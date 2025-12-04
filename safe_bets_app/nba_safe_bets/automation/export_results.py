import os
import pandas as pd
from daily_predict.daily_predict import daily_predict

EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

def export_results():
    df = daily_predict()

    csv_path = os.path.join(EXPORT_DIR, "top25_today.csv")
    json_path = os.path.join(EXPORT_DIR, "top25_today.json")

    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=4)

    print(f"✔ Exported CSV to {csv_path}")
    print(f"✔ Exported JSON to {json_path}")

if __name__ == "__main__":
    export_results()
