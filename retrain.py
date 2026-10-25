import os
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

MODEL_NAME = "investment-agent"

def load_feedback_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    feedback_dir = os.path.join(base_dir, "data", "feedback")

    dfs = []
    for file in os.listdir(feedback_dir):
        if file.endswith(".csv"):
            dfs.append(pd.read_csv(os.path.join(feedback_dir, file)))

    return pd.concat(dfs, ignore_index=True)

def main():
    mlflow.set_experiment("agentic-mlops-retraining")

    df = load_feedback_data()

    X = df[["agent_id", "tool_name", "status"]]
    y = df["trade_value"]

    cat_features = ["agent_id", "tool_name", "status"]
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features)
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("regressor", LinearRegression())
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    with mlflow.start_run() as run:
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        mse = mean_squared_error(y_test, preds)

        mlflow.log_metric("mse", mse)
        mlflow.sklearn.log_model(
            model,
            "model",
            registered_model_name=MODEL_NAME,
            pip_requirements=[
                "mlflow==2.9.2",
                "numpy==1.26.4",
                "pandas==2.2.2",
                "scikit-learn==1.5.2",
                "scipy==1.12.0",
            ],
        )

        client = mlflow.tracking.MlflowClient()
        versions = client.search_model_versions(f"name='{MODEL_NAME}'")
        run_versions = [version for version in versions if version.run_id == run.info.run_id]
        if not run_versions:
            raise RuntimeError(f"No registered model version found for run {run.info.run_id}")

        candidate_version = max(run_versions, key=lambda version: int(version.version)).version
        github_output = os.environ.get("GITHUB_OUTPUT")
        if github_output:
            with open(github_output, "a", encoding="utf-8") as output_file:
                output_file.write(f"candidate_version={candidate_version}\n")
        print(f"Registered Challenger version: {candidate_version}")

        print(f"Training complete. MSE: {mse}")

if __name__ == "__main__":
    main()
