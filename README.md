# 🌧️ Rain in Australia – Streamlit Demo

Цей проєкт демонструє, як розгорнути модель машинного навчання за допомогою **Streamlit** для прогнозування дощу в Австралії.  
Додаток дозволяє користувачам вводити метеорологічні показники (температура, швидкість вітру, хмарність, вологість тощо) і отримувати прогноз — чи буде дощ завтра — на основі навченої моделі **Random Forest**.

---

## 🚀 Демо-версія

Протестувати роботу застосунку можна за посиланням (після деплою):

👉 **https://rain-australia-kalashnikovayana.streamlit.app**

Якщо після відкриття посилання з’явиться повідомлення:

> *“This app has gone to sleep due to inactivity. Would you like to wake it back up?”*  

просто натисніть **“Yes, get this app back up!”** і зачекайте ~30 секунд.

---

## 📂 Структура проєкту


rain-australia-streamlit/
├── data/                  # (опціонально) Оригінальний набір даних weatherAUS.csv
├── models/
│   └── aussie_rain.joblib # Навчена модель
├── app.py                 # Основний файл Streamlit-додатку
├── train.py               # Скрипт для навчання моделі RandomForest
├── requirements.txt       # Необхідні Python-пакети
└── README.md              # Документація проєкту

## ⚙️ Налаштування середовища
1. Передумови

Встановлений Python 3.10+

Встановлений git

2. Клонування репозиторію
git clone https://github.com/kalashnikovayana/rain-australia-streamlit.git
cd rain-australia-streamlit

3. Створення віртуального середовища (рекомендовано)

Windows:

python -m venv venv
venv\Scripts\activate


macOS / Linux:

python -m venv venv
source venv/bin/activate

4. Встановлення залежностей
pip install -r requirements.txt

## 🧠 Навчання моделі

Якщо потрібно перевчити модель з нуля, запустіть скрипт train.py.
Він:

завантажує набір даних weatherAUS.csv;

виконує попередню обробку (імпутація пропусків, кодування категоріальних ознак, масштабування числових);

тренує модель RandomForestClassifier;

зберігає артефакти у файл models/aussie_rain.joblib.

Запуск скрипта:

python train.py

## 🖥️ Запуск Streamlit-додатку локально

Після встановлення залежностей запустіть:

streamlit run app.py


Додаток буде доступний у браузері за адресою:

👉 http://localhost:8501

Ви побачите інтерфейс для введення погодних характеристик і отримаєте прогноз — Yes / No, чи очікується дощ завтра 🌧️
