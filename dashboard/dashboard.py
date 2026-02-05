import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import date

st.set_page_config(page_title="Gate Vehicle Log Dashboard", layout="wide")

# client = MongoClient("mongodb+srv://chaturvedialok44_db_user:FxHFDZZKMacwuohR@cluster0.thvr1so.mongodb.net/?appName=Cluster0")
client = MongoClient("mongodb+srv://chaturvedialok44_db_user:sDDTLmBMSTwEhh9C@cluster0.bgcmtgp.mongodb.net/?appName=Cluster0")
db = client["gate_db"]
logs = db["vehicle_logs"]

VALID_USERNAME = "chaturvedialok44"
VALID_PASSWORD = "Alok@2727"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Gate Vehicle Log – Login")

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

    if login_btn:
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid username or password.")
    st.stop()

st.title("🚗 Gate Vehicle Log Dashboard")

data = list(logs.find({}, {"_id": 0}).sort("timestamp", -1))

if not data:
    st.info("No records found.")
    st.stop()

df = pd.DataFrame(data)
df["timestamp"] = pd.to_datetime(df["timestamp"])

st.sidebar.header("Filters")

plate_filter = st.sidebar.text_input("Search Plate")
date_filter = st.sidebar.selectbox("Date Filter", ["All", "Today", "Custom"])

filtered = df.copy()

if date_filter == "Today":
    today = date.today()
    filtered = filtered[filtered["timestamp"].dt.date == today]

elif date_filter == "Custom":
    min_d = df["timestamp"].dt.date.min()
    max_d = df["timestamp"].dt.date.max()
    start, end = st.sidebar.date_input("Select Range", (min_d, max_d))
    if start <= end:
        mask = (filtered["timestamp"].dt.date >= start) & (
            filtered["timestamp"].dt.date <= end
        )
        filtered = filtered[mask]

if plate_filter:
    filtered = filtered[
        filtered["plate"].str.contains(plate_filter.upper(), na=False)
    ]

tab1, tab2 = st.tabs(["📜 All Logs", "🏫 Inside Vehicles"])

with tab1:
    st.subheader("All Logs (Filtered)")

    if filtered.empty:
        st.info("No records match this filter.")
    else:
        st.dataframe(filtered, use_container_width=True)

        csv_all = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download filtered logs as CSV",
            data=csv_all,
            file_name="vehicle_logs_filtered.csv",
            mime="text/csv",
        )

        st.markdown("---")
        st.subheader("Summary")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total records", len(filtered))
        with col2:
            st.metric(
                "Unique plates",
                filtered["plate"].nunique() if not filtered.empty else 0,
            )
        with col3:
            in_count = (filtered["status"] == "IN").sum()
            st.metric("IN status count", int(in_count))

        st.markdown("### 📊 Daily Entry Count (filtered)")
        filtered["date"] = filtered["timestamp"].dt.date
        counts = (
            filtered.groupby("date")
            .size()
            .reset_index(name="count")
            .sort_values("date")
        )

        if not counts.empty:
            counts = counts.set_index("date")
            st.bar_chart(counts["count"])
        else:
            st.info("Not enough data to plot chart.")

with tab2:
    st.subheader("Vehicles Currently Inside")

    latest = df.sort_values("timestamp", ascending=False).drop_duplicates("plate")
    inside = latest[latest["status"] == "IN"]

    if plate_filter:
        inside = inside[
            inside["plate"].str.contains(plate_filter.upper(), na=False)
        ]

    if inside.empty:
        st.info("No vehicles currently inside for this filter.")
    else:
        st.dataframe(inside, use_container_width=True)
        st.caption(f"Vehicles inside: {len(inside)}")

        csv_inside = inside.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download inside vehicles as CSV",
            data=csv_inside,
            file_name="inside_vehicles.csv",
            mime="text/csv",
        )
