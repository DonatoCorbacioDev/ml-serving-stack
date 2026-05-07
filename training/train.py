from pathlib import Path
import argparse

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier


def parse_args():

    parser = argparse.ArgumentParser(
        description="Train a RandomForest model on the Iris dataset"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/models",
        help="Directory where the trained model will be saved"
    )

    return parser.parse_args()


def main():

    args = parse_args()

    # Load dataset
    iris = load_iris()

    X = iris.data
    y = iris.target

    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save model
    model_path = output_dir / "model.joblib"

    joblib.dump(model, model_path)

    print(f"Model saved to: {model_path}")


if __name__ == "__main__":
    main()