import os
import sys

PY = sys.executable

def run_ocr():
    os.system(f'"{PY}" ocr/ocr_camera.py')

def run_dashboard():
    # os.system("streamlit run dashboard/dashboard.py")
    os.system(f"{sys.executable} -m streamlit run dashboard/dashboard.py")

def test_db():
    os.system(f'"{PY}" database/db_test.py')

while True:
    print("\n===== Vehicle Entry System =====")
    print("1. Start OCR Camera")
    print("2. Open Dashboard")
    print("3. Run DB Connection Test")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        run_ocr()
    elif choice == "2":
        run_dashboard()
    elif choice == "3":
        test_db()
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid option, try again.")
