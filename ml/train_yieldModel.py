import pandas as pd
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


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

    # Check crop types
    print("\nCrop types:")
    print(data["Crop Type"].value_counts())


    # 3. Separate features and target
    X = data[["Crop Type", "Soil Type", "Temperature", "Humidity", "Rainfall", "Season"]]
    y = data["crop_yield"]


    # 4. Convert categorical columns into numbers using One-Hot Encoding
    X = pd.get_dummies(X)

    # 5. Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 6. Create Linear Regression model
    model: LinearRegression = LinearRegression()

    # 7. Train the model
    model.fit(X_train, y_train)

    # 8. Make predictions
    predictions = model.predict(X_test)

    # 9. Evaluate the model
    mae = mean_absolute_error(y_test, predictions)
    # mse = mean_squared_error(y_test, predictions)
    # rmse = mse ** 0.5
    r2 = r2_score(y_test, predictions)


    print("\nLinear Regression Results")
    print("MAE :", mae)
    # print("MSE :", mse)
    # print("RMSE:", rmse)
    print("R2  :", r2)


    # 10. Save the trained model
    model_data: dict = {
        "model": model,
        "columns": X.columns.tolist()
    }

    # print("Current folder:", os.getcwd())
    # print("ML folder exists:", os.path.exists("ml"))

    with open("yield_model.pkl", mode="wb") as file:
        pickle.dump(model_data, file)

    print("\nYield model saved successfully!")

    return model

if __name__ == "__main__":
    train_model("dataset/crop-yield_selected_features.csv")

















  