import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC

from sklearn.metrics import accuracy_score


def train_model(csv_path):
    # 1. Load dataset
    data = pd.read_csv(csv_path)

    print(data.head())
    print("Dataset loaded successfully")


    # 2. Basic Data Preprocessing

    # Check missing values
    print("\nMissing values:")
    print(data.isnull().sum())

    # Remove rows containing missing values
    data = data.dropna()

    # Remove duplicate rows
    data = data.drop_duplicates()

    # Check data types
    print("\nData types:")
    print(data.dtypes)

    # Check crop labels
    print("\nCrop labels:")
    print(data["label"].value_counts())


    # 3. Separate features and target
    X = data.drop("label", axis=1)
    y = data["label"]


    # 4. Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    # 5. Feature Scaling
    scaler: StandardScaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)


    # 6. Create Models
    logistic_model = LogisticRegression(max_iter=10000)
    decision_tree_model = DecisionTreeClassifier()
    random_forest_model = RandomForestClassifier()
    svm_model = SVC()


    # 7. Train Individual Models

    # Model training
    logistic_model.fit(X_train_scaled, y_train)
    svm_model.fit(X_train_scaled, y_train)
    decision_tree_model.fit(X_train, y_train)
    random_forest_model.fit(X_train, y_train)


    # 8. Create Voting Classifier -> hard and soft voting
    voting_model = VotingClassifier(
        estimators=[
            ("Logistic Regression", logistic_model),
            ("Decision Tree", decision_tree_model),
            ("Random Forest", random_forest_model),
            ("SVM", svm_model)
        ], voting="hard"
    )


    # 9. Make predictions for each model
    lr_predictions = logistic_model.predict(X_test_scaled)
    dt_predictions = decision_tree_model.predict(X_test)
    rf_predictions = random_forest_model.predict(X_test)
    svm_predictions = svm_model.predict(X_test_scaled)


    # 10. Display individual model accuracies
    print("\nIndividual Model Accuracies:")

    print("Logistic Regression: ",accuracy_score(y_test, lr_predictions))
    print("Decision Tree: ", accuracy_score(y_test, dt_predictions))
    print("Random Forest: ", accuracy_score(y_test, rf_predictions))
    print("SVM: ", accuracy_score(y_test, svm_predictions))


    # 11. Train Voting Classifier

    # VotingClassifier uses the already trained models
    voting_model.fit(X_train, y_train)

    # 12. Voting prediction
    voting_predictions = voting_model.predict(X_test)

    # 13. Voting accuracy
    voting_accuracy = accuracy_score(y_test, voting_predictions)

    print("\n----------------------")
    print("Voting Classifier Accuracy:", voting_accuracy)


    # 14. Save Voting Classifier
    model_data: dict = {
        "model": voting_model,
        "model_name": "Voting Classifier"
    }

    with open("model.pkl", mode="wb") as file:
        pickle.dump(model_data, file)

    # 15. Save Scaler
    with open("scaler.pkl", mode="wb") as file:
        pickle.dump(scaler, file)

    print("\nVoting Classifier saved successfully!")
    print("Scaler saved successfully!")

    return voting_model


if __name__ == "__main__":
    train_model("dataset/crop_recommendation_dataset.csv")