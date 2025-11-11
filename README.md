☔ Rain in Australia – Streamlit Demo

Цей проєкт демонструє, як розгорнути модель машинного навчання за допомогою Streamlit для прогнозування дощу в Австралії.
Додаток дозволяє користувачам вводити метеорологічні показники (температура, швидкість вітру, хмарність, вологість тощо) і отримувати прогноз — чи буде дощ завтра — на основі навченої моделі Random Forest.

Протестувати роботу застосунку можна за посиланням (після деплою):
👉 https://rain-australia-kalashnikovayana.streamlit.app

Якщо після відкриття посилання з’явиться повідомлення:

“This app has gone to sleep due to inactivity. Would you like to wake it back up?”
просто натисніть “Yes, get this app back up!” і зачекайте близько 30 секунд.

🌿 Структура проєкту
data/ (опціонально)            # Оригінальний набір даних weatherAUS.csv
models/                        # Навчена модель
    └── aussie_rain.joblib
app.py                         # Основний файл Streamlit-додатку
train.py                       # Скрипт для навчання моделі RandomForest
requirements.txt               # Необхідні Python-пакети
README.md                      # Документація проєкту

⚙️ Налаштування середовища
Передумови

Встановлений Python 3.10 або новіший

Встановлені пакети з requirements.txt

🚀 Встановлення

Клонувати репозиторій

git clone https://github.com/kalashnikovayana/rain-australia-streamlit.git
cd rain-australia-streamlit


Створити віртуальне середовище (рекомендовано)

python -m venv venv
venv\Scripts\activate   # для Windows
# або
source venv/bin/activate  # для macOS / Linux


Встановити залежності

pip install -r requirements.txt

🌦️ Навчання моделі

Для навчання моделі запустіть файл train.py.
Скрипт виконує такі кроки:

завантажує набір даних weatherAUS.csv;

виконує попередню обробку (імп’ютація, кодування, масштабування);

тренує модель RandomForestClassifier;

зберігає артефакт у models/aussie_rain.joblib.

python train.py


Після цього модель буде готова до використання у Streamlit-додатку.

💻 Запуск Streamlit-додатку локально
streamlit run app.py


Після запуску відкрийте у браузері:

http://localhost:8501


Ви побачите інтерфейс для введення погодних характеристик і отримаєте прогноз — Yes / No, чи очікується дощ завтра 🌧️

🌐 Деплой на Streamlit Cloud

Завантажте репозиторій на GitHub.

Перейдіть на https://share.streamlit.io
 → Deploy an app.

Вкажіть:

Repository: kalashnikovayana/rain-australia-streamlit

Branch: main

Main file path: app.py

Натисніть Deploy і зачекайте кілька хвилин.

Після цього застосунок стане доступним за публічним посиланням.

🛠 Використані технології

Python 3.10+

Streamlit

Pandas

NumPy

Scikit-learn

Joblib