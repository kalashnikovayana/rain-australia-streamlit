# app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os


@st.cache_resource
def load_artifacts():
    """Завантаження моделі та всіх препроцесорів з joblib-файла."""
    # якщо файл лежить у папці models/
    path = os.path.join("models", "aussie_rain.joblib")
    aussie = joblib.load(path)

    return {
        "model": aussie["model"],
        "imputer": aussie["imputer"],
        "scaler": aussie["scaler"],
        "encoder": aussie["encoder"],
        "input_cols": aussie["input_cols"],
        "numeric_cols": aussie["numeric_cols"],
        "categorical_cols": aussie["categorical_cols"],
    }


artifacts = load_artifacts()
model = artifacts["model"]
imputer = artifacts["imputer"]
scaler = artifacts["scaler"]
encoder = artifacts["encoder"]
input_cols = artifacts["input_cols"]
numeric_cols = artifacts["numeric_cols"]
categorical_cols = artifacts["categorical_cols"]

st.title("☔ Прогноз: чи піде дощ завтра в Австралії?")
st.write(
    "Введи характеристики погоди за сьогодні, а модель спрогнозує, "
    "чи очікується дощ завтра."
)

# ---- 1. Інтерфейс для введення даних ----

col1, col2 = st.columns(2)

with col1:
    location = st.text_input("Location", "Sydney")
    min_temp = st.number_input("MinTemp (°C)", value=12.0)
    max_temp = st.number_input("MaxTemp (°C)", value=22.0)
    rainfall = st.number_input("Rainfall (mm)", value=0.0)
    evaporation = st.number_input("Evaporation (mm)", value=5.0)
    sunshine = st.number_input("Sunshine (hours)", value=7.0)
    wind_gust_speed = st.number_input("WindGustSpeed (km/h)", value=30.0)
    wind_speed_9am = st.number_input("WindSpeed9am (km/h)", value=15.0)

with col2:
    wind_speed_3pm = st.number_input("WindSpeed3pm (km/h)", value=20.0)
    humidity_9am = st.number_input("Humidity9am (%)", value=70.0)
    humidity_3pm = st.number_input("Humidity3pm (%)", value=50.0)
    pressure_9am = st.number_input("Pressure9am (hPa)", value=1010.0)
    pressure_3pm = st.number_input("Pressure3pm (hPa)", value=1008.0)
    cloud_9am = st.number_input("Cloud9am (октав)", value=4.0)
    cloud_3pm = st.number_input("Cloud3pm (октав)", value=4.0)
    temp_9am = st.number_input("Temp9am (°C)", value=18.0)
    temp_3pm = st.number_input("Temp3pm (°C)", value=21.0)

st.subheader("Вітер та дощ сьогодні")
wind_gust_dir = st.text_input("WindGustDir", "W")
wind_dir_9am = st.text_input("WindDir9am", "W")
wind_dir_3pm = st.text_input("WindDir3pm", "W")
rain_today = st.selectbox("RainToday", ["No", "Yes"])


# ---- 2. Зробити один рядок DataFrame у правильному порядку колонок ----

def build_input_df():
    data = {
        "MinTemp": min_temp,
        "MaxTemp": max_temp,
        "Rainfall": rainfall,
        "Evaporation": evaporation,
        "Sunshine": sunshine,
        "WindGustSpeed": wind_gust_speed,
        "WindSpeed9am": wind_speed_9am,
        "WindSpeed3pm": wind_speed_3pm,
        "Humidity9am": humidity_9am,
        "Humidity3pm": humidity_3pm,
        "Pressure9am": pressure_9am,
        "Pressure3pm": pressure_3pm,
        "Cloud9am": cloud_9am,
        "Cloud3pm": cloud_3pm,
        "Temp9am": temp_9am,
        "Temp3pm": temp_3pm,
        "Location": location,
        "WindGustDir": wind_gust_dir,
        "WindDir9am": wind_dir_9am,
        "WindDir3pm": wind_dir_3pm,
        "RainToday": rain_today,
    }

    # важливо: колонки в тому ж порядку, як input_cols
    df = pd.DataFrame([data], columns=input_cols)
    return df


# ---- 3. Повний препроцесинг (як у ноутбуці) ----

def preprocess(df_row: pd.DataFrame) -> np.ndarray:
    # числові
    X_num = df_row[numeric_cols]
    X_num = imputer.transform(X_num)          # імпутація
    X_num = scaler.transform(X_num)          # масштабування

    # категоріальні
    X_cat = df_row[categorical_cols].astype("object")
    X_cat = encoder.transform(X_cat)         # OneHotEncoder повертає sparse matrix

    # об’єднати
    X_final = np.hstack([X_num, X_cat.toarray()])
    return X_final


# ---- 4. Кнопка прогнозу ----

if st.button("Зробити прогноз"):
    df_input = build_input_df()
    X_final = preprocess(df_input)

    proba = model.predict_proba(X_final)[0, 1]
    pred = model.predict(X_final)[0]  # 1 = Yes, 0 = No

    label = "Yes" if pred == 1 else "No"

    st.subheader("Результат")
    st.write(f"**Чи буде дощ завтра?** → **{label}**")
    st.write(f"**Ймовірність дощу:** {proba:.1%}")
