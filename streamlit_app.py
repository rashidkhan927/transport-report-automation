
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Transport Report Dashboard", layout="wide")

st.title("🚛 Transport Report Dashboard")

# Upload or load default CSV
file = st.file_uploader("Upload Transport Data CSV", type=["csv"])
if file:
    df = pd.read_csv(file)
else:
    if os.path.exists("data/transport_data_sample.csv"):
        df = pd.read_csv("data/transport_data_sample.csv")
    else:
        st.warning("Please upload a CSV file or place one at 'data/transport_data_sample.csv'")
        st.stop()

# Preprocess
df.dropna(inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
df['FuelEfficiency'] = df['Distance'] / df['FuelUsed']

# Metrics
st.subheader("🔢 Key Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Total Distance (KM)", f"{df['Distance'].sum():,.2f}")
col2.metric("Avg Fuel Efficiency (KM/L)", f"{df['FuelEfficiency'].mean():.2f}")
col3.metric("Total Records", f"{len(df)}")

# Charts
st.subheader("📊 Distance Traveled by Vehicle")
distance_by_vehicle = df.groupby('VehicleID')['Distance'].sum().sort_values()
st.bar_chart(distance_by_vehicle)

st.subheader("⛽ Average Fuel Efficiency by Vehicle")
efficiency_by_vehicle = df.groupby('VehicleID')['FuelEfficiency'].mean().sort_values()
st.bar_chart(efficiency_by_vehicle)

# Delivery Status Pie Chart
st.subheader("🚦 Delivery Status Breakdown")
status_counts = df['DeliveryStatus'].value_counts()
st.write(status_counts)
st.pyplot(status_counts.plot.pie(autopct="%1.1f%%", figsize=(6, 6), title="Delivery Status").get_figure())
