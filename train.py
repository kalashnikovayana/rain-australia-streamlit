# train.py
import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

# 1. Завантаження даних
df = pd.read_csv("weatherAUS.csv")

# Приблизно як у лекції: прибираємо стовпці, які не використовуємо
for col in ["Date", "RISK_MM"]:
    if col in df.columns:
        df = df.drop(columns=[col])

# Ціль:
target_col = "RainTomorrow"

# Викидаємо рядки без цілі
df = df.dropna(subset=[target_col])

y = df[target_col].map({"No": 0, "Yes": 1})
X = df.drop(columns=[target_col])

# 2. Розбиття на train / test (просто для контролю)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Визначаємо числові / категоріальні колонки
numeric_cols = X_train.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_cols = X_train.select_dtypes(include=["object"]).columns.tolist()
input_cols = numeric_cols + categorical_cols

# 4. Імп’ютер + скейлер для числових
num_imputer = SimpleImputer(strategy="median")
num_scaler = MinMaxScaler()

# 5. Імп’ютер + OneHotEncoder для категоріальних
cat_imputer = SimpleImputer(strategy="most_frequent")
cat_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=True)

# 6. Фітаємо препроцесинг на train
X_num_train = num_imputer.fit_transform(X_train[numeric_cols])
X_num_train = num_scaler.fit_transform(X_num_train)

X_cat_train = cat_imputer.fit_transform(X_train[categorical_cols])
X_cat_train = cat_encoder.fit_transform(X_cat_train)  # це sparse

# 7. Об’єднуємо фічі
from scipy import sparse

X_train_final = sparse.hstack([X_num_train, X_cat_train])

# 8. Модель – RandomForest (можна DecisionTreeClassifier, якщо дуже хочеш “дерева”)
rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

rf.fit(X_train_final, y_train)

# Тестова точність (просто надрукуємо)
from sklearn.metrics import accuracy_score

X_num_test = num_imputer.transform(X_test[numeric_cols])
X_num_test = num_scaler.transform(X_num_test)

X_cat_test = cat_imputer.transform(X_test[categorical_cols])
X_cat_test = cat_encoder.transform(X_cat_test)

X_test_final = sparse.hstack([X_num_test, X_cat_test])

y_pred = rf.predict(X_test_final)
print("Test accuracy:", accuracy_score(y_test, y_pred))

# 9. Пакуємо все в dict у тому вигляді, який чекає app.py
artifacts = {
    "model": rf,
    "imputer": num_imputer,
    "scaler": num_scaler,
    "encoder": cat_encoder,
    "input_cols": input_cols,
    "numeric_cols": numeric_cols,
    "categorical_cols": categorical_cols,
}

os.makedirs("models", exist_ok=True)
joblib.dump(artifacts, os.path.join("models", "aussie_rain.joblib"), compress=("zlib", 3))
print("Saved models/aussie_rain.joblib")
