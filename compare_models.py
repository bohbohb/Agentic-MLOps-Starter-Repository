import argparse
import os

from mlflow.tracking import MlflowClient


MODEL_NAME = "investment-agent"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate_version")
    candidate_version = parser.parse_args().candidate_version

    if not os.environ.get("MLFLOW_TRACKING_URI"):
        raise RuntimeError("Configure the MLFLOW_TRACKING_URI repository secret.")

    client = MlflowClient()
    challenger = client.get_model_version(MODEL_NAME, candidate_version)
    challenger_mse = client.get_run(challenger.run_id).data.metrics["mse"]
    client.transition_model_version_stage(
        MODEL_NAME, candidate_version, "Staging", archive_existing_versions=False
    )

    champions = client.get_latest_versions(MODEL_NAME, stages=["Production"])
    champion = max(champions, key=lambda version: int(version.version), default=None)

    if champion is None:
        client.transition_model_version_stage(
            MODEL_NAME, candidate_version, "Production", archive_existing_versions=True
        )
        print(f"No Production Champion existed; version {candidate_version} is now Production.")
        return

    champion_mse = client.get_run(champion.run_id).data.metrics["mse"]
    print(f"Challenger MSE: {challenger_mse}; Champion MSE: {champion_mse}")

    if challenger_mse < champion_mse:
        client.transition_model_version_stage(
            MODEL_NAME, candidate_version, "Production", archive_existing_versions=True
        )
        print(f"Challenger {candidate_version} outperformed the Champion and is now Production.")
    else:
        client.transition_model_version_stage(
            MODEL_NAME, champion.version, "Production", archive_existing_versions=True
        )
        print(
            f"Challenger {candidate_version} did not improve MSE; "
            f"Champion {champion.version} remains Production."
        )


if __name__ == "__main__":
    main()