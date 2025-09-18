from flask import Flask, render_template_string
import pandas as pd
import datetime

app = Flask(__name__)

# Load schedule
file_path = "Kundalik daftari.xlsx"
df = pd.read_excel(file_path, sheet_name="Sheet0")

# Clean
schedule_df = df.iloc[7:].reset_index(drop=True)
schedule_df.columns = ["#", "Subject", "Grade", "Homework"]

weekday_map = {
    "Dushanba": 0,
    "Seshanba": 1,
    "Chorshanba": 2,
    "Payshanba": 3,
    "Juma": 4,
    "Shanba": 5
}

def extract_schedule():
    schedules = {}
    current_day = None
    for _, row in schedule_df.iterrows():
        subject = str(row["Subject"]).strip()
        if subject in weekday_map.keys():
            current_day = weekday_map[subject]
            schedules[current_day] = []
        elif current_day is not None and row["#"] not in [None, "№"]:
            if subject != "nan" and subject:  # remove empty/nan
                schedules[current_day].append(subject)
    return schedules

schedules = extract_schedule()

# Uzbek weekday names for display
reverse_weekday_map = {v: k for k, v in weekday_map.items()}

@app.route("/")
def index():
    today = datetime.date.today().weekday()
    tomorrow = (today + 1) % 7

    today_subjects = schedules.get(today, [])
    tomorrow_subjects = schedules.get(tomorrow, [])

    html_template = """
    <!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Tomorrow's Schedule</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #6a11cb, #2575fc);
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      margin: 0;
      color: #fff;
    }

    .card {
      background: #ffffff;
      color: #333;
      padding: 30px 40px;
      border-radius: 20px;
      width: 400px;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
      text-align: center;
      animation: fadeIn 0.8s ease-out;
    }

    .card h1 {
      font-size: 28px;
      margin-bottom: 20px;
      color: #2575fc;
    }

    .card h2 {
      font-size: 22px;
      margin-bottom: 15px;
      color: #444;
    }

    ul {
      list-style: none;
      padding: 0;
      margin: 0;
    }

    li {
      font-size: 18px;
      margin: 10px 0;
      padding: 12px;
      background: #f5f7fa;
      border-radius: 10px;
      transition: transform 0.2s, background 0.2s;
    }

    li:hover {
      transform: scale(1.05);
      background: #e3e9ff;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body>
  <div class="card">
    <h1>📅 Ertangi Jadval</h1>
    <h2>{{ tomorrow_name }}</h2>
    <ul>
      {% for subj in tomorrow_subjects %}
        <li>{{ subj }}</li>
      {% endfor %}
    </ul>
  </div>
</body>
</html>
    """

    return render_template_string(
        html_template,
        today_subjects=today_subjects,
        tomorrow_subjects=tomorrow_subjects,
        today_name=reverse_weekday_map.get(today, "—"),
        tomorrow_name=reverse_weekday_map.get(tomorrow, "—")
    )

if __name__ == "__main__":
    app.run(debug=True)
