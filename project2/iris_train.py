import argparse
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_size", type=float, default=0.2)
    parser.add_argument("--random_state", type=int, default=42)
    args = parser.parse_args()

    # Load data
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=args.random_state
    )

    # Train model
    clf = RandomForestClassifier(random_state=args.random_state)
    clf.fit(X_train, y_train)

    # Evaluate
    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)

    # Log with MLflow
    with mlflow.start_run():
        mlflow.log_param("test_size", args.test_size)
        mlflow.log_param("random_state", args.random_state)
        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(clf, "iris_model")

    print(f"Accuracy: {acc}")
