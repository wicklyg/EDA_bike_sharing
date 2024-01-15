import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Load dataset
data = pd.read_csv("day.csv")

# Create a Streamlit app
st.title("Bike Sharing Data Analysis Dashboard")

# Sidebar for data upload
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# If a file is uploaded, use it as the dataset
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
num_records = len(data)
st.sidebar.write('NO of Records',num_records)

# Display the original dataset
st.subheader("Original Dataset")
st.write(data)

# Display Dataset Statistics
st.subheader("Dataset Statistics (Describe)")
st.write(data.describe())

# Mengubah nilai weathersit menjadi label yang sesuai
weather_labels = {
    1: "Clear/Few clouds/Partly cloudy",
    2: "Mist/Cloudy/Broken clouds/Few clouds",
    3: "Light Snow/Light Rain/Thunderstorm/Scattered clouds",
    4: "Heavy Rain/Ice Pallets/Thunderstorm/Mist/Snow/Fog"
}
data['weather_label'] = data['weathersit'].map(weather_labels)

yr_labels = {
    0: "2011",
    1: "2012",
    2: "2013",
    3: "2014",
    4: "2015",
    5: "2016",
    6: "2017",
    7: "2018",
    8: "2019",
    9: "2020",
    10: "2021",
    11: "2022",
    12: "2023",
    13: "2024"
}
data['yr_labels'] = data['yr'].map(yr_labels)

# Mengelompokkan data berdasarkan tahun (yr), bulan (mnth), dan menghitung rata-rata peminjaman sepeda (cnt)
avg_daily_rentals_monthly = data.groupby(['yr_labels', 'mnth'])['cnt'].mean()

# Mengelompokkan data berdasarkan weather_label dan menghitung jumlah peminjaman sepeda (cnt)
rentals_by_weather = data.groupby('weather_label')['cnt'].sum()

# Task 1: Tren rata-rata peminjaman sepeda harian dalam setiap bulannya
st.subheader("Trend of Average Daily Bike Rentals Per Month")
month_labels = ["Januari","Februari","Maret","April","Mei", "Juni","Juli","Agustus","September","Oktober","November","Desember"]
# Widget untuk memilih tahun
selected_year = st.selectbox("Select Year", options=data['yr_labels'].unique())

avg_daily_rentals_selected_year = avg_daily_rentals_monthly.loc[selected_year]

fig, ax = plt.subplots()
ax.plot(month_labels, avg_daily_rentals_selected_year)
ax.set_xlabel('Month')
ax.set_ylabel('Average Daily Bike Rentals')
ax.set_xticks(month_labels)
ax.set_xticklabels(month_labels, rotation=45)
st.pyplot(fig)

# Task 2: Pengaruh suhu terhadap jumlah peminjam sepeda
st.subheader("Effect of Temperature on Bike Rentals (Regression Plot)")
fig, ax = plt.subplots()
sns.regplot(x='temp', y='cnt', data=data, scatter_kws={'alpha':0.5}, ax=ax)
st.pyplot(fig)

# Task 3: Pola peminjaman sepeda yang berkaitan dengan cuaca
st.subheader("Bike Rentals Patterns Related to Weather (Pie Chart)")
fig, ax = plt.subplots()
ax.pie(rentals_by_weather, labels=rentals_by_weather.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)
