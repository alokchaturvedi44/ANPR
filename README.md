# ANPR 2 - Automatic Number Plate Recognition

A real-time system designed to detect vehicle license plates using YOLO, extract text via EasyOCR, and log the entry/exit data into a MongoDB database.

## Features
- **Real-time Detection:** Uses YOLOv8 for high-speed plate localization.
- **OCR Engine:** Powered by EasyOCR for accurate text extraction.
- **Database Integration:** Automatic logging of plate numbers, timestamps, and status (IN/OUT).
- **Live Monitoring Dashboard:** A Streamlit-based interface providing:
     1. **Advanced Filtering:** Search by specific plate numbers or filter by date.
     2. **Inside Vehicles Tracking:** A dedicated view to see which vehicles are currently on the premises.
     3. **Analytics Summary:** Real-time counters for total records, unique plates, and current "IN" status counts.
     4. **Data Export:** Capability to download filtered logs as CSV for reporting.
     5. **Visual Analytics:** Daily entry count charts for trend analysis.

## Tech Stack
- **Language:** Python 3.11
- **Frameworks:** Streamlit, PyMongo, Ultralytics (YOLO)
- **Database:** MongoDB Atlas

## Installation & Setup

1. **Clone the repo:**
   ```bash
   git clone https://github.com/alokchaturvedi44/ANPR.git
   cd ANPR

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install python-dotenv
   
3. **Configure Environment Variables: Create a .env file in the root directory:**
   ```bash
   MONGO_URI=mongodb+srv://your_user:your_password@cluster.mongodb.net/?appName=Cluster0
   DASHBOARD_USERNAME=<your_username>
   DASHBOARD_PASSWORD=<your_password>
   
4. **Run the Application:**
   ```bash
   python app.py
