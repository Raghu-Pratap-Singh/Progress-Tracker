# 📈 Progress Tracker

A custom Python desktop app for daily productivity.

## 🚀 Installation
1. Go to **Releases**.
2. Download and unzip `Progress-Tracker-v1.zip`.
3. Run `Progress Tracker.exe`.

## 🛠️ Features
- Fenwick Tree logic for fast progress calculation.
- Dark mode custom UI.
- Local SQLite database storage.

- ## ⚠️ Important Usage Notes (What NOT to do)

To ensure the progress calculations and Fenwick Tree logic remain accurate, please follow these guidelines:

* **Avoid Non-Chronological Entry**: Do not add data for a "previous date" after you have already entered data for a "later date." The app is optimized for real-time, day-to-day tracking.

* **Database Manual Edits**: Do not manually open or edit the `tracker.db` file with external software, as it may corrupt the data structure required by the app.
