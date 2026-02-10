import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def main():
    data = load_iris(as_frame=True)
    df = data.frame

    X = df.drop(columns=["target"])
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Baseline accuracy: {acc:.4f}")

    X.mean().plot(kind="bar")
    plt.title("Feature Means (Iris)")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
