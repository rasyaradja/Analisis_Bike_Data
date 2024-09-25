import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(page_title="Rasya Bike Sharing", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('./data/day.csv')
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# Title
st.title("Bike Sharing Data Analysis Dashboard")

# Sidebar
st.sidebar.title("Made By Rasya") 
st.sidebar.markdown("check out my [linkedin](https://www.linkedin.com/in/rasyaradja/)")
st.sidebar.header("Filters")
year = st.sidebar.selectbox("Select Year", df['dteday'].dt.year.unique())
df_filtered = df[df['dteday'].dt.year == year]

# Functions for visualizations
def plot_daily_rentals(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data['dteday'], data['cnt'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Rentals')
    ax.set_title('Daily Bike Rentals')
    return fig

def plot_monthly_rentals(data):
    monthly_rentals = data.groupby(data['dteday'].dt.to_period('M'))['cnt'].sum().reset_index()
    monthly_rentals['dteday'] = monthly_rentals['dteday'].dt.to_timestamp()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_rentals['dteday'], monthly_rentals['cnt'])
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Rentals')
    ax.set_title('Monthly Bike Rentals')
    return fig

def plot_seasonal_rentals(data):
    seasonal_rentals = data.groupby('season')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='season', y='cnt', data=seasonal_rentals, ax=ax)
    ax.set_xlabel('Season')
    ax.set_ylabel('Average Number of Rentals')
    ax.set_title('Average Bike Rentals by Season')
    return fig

def plot_weather_impact(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='weathersit', y='cnt', data=data, ax=ax)
    ax.set_xlabel('Weather Situation')
    ax.set_ylabel('Number of Rentals')
    ax.set_title('Impact of Weather on Bike Rentals')
    return fig

def plot_temp_impact(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='temp', y='cnt', data=data, ax=ax)
    ax.set_xlabel('Temperature')
    ax.set_ylabel('Number of Rentals')
    ax.set_title('Impact of Temperature on Bike Rentals')
    return fig

def plot_humidity_impact(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='hum', y='cnt', data=data, ax=ax)
    ax.set_xlabel('Humidity')
    ax.set_ylabel('Number of Rentals')
    ax.set_title('Impact of Humidity on Bike Rentals')
    return fig

def plot_windspeed_impact(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='windspeed', y='cnt', data=data, ax=ax)
    ax.set_xlabel('Wind Speed')
    ax.set_ylabel('Number of Rentals')
    ax.set_title('Impact of Wind Speed on Bike Rentals')
    return fig

def plot_day_type_impact(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='workingday', y='cnt', data=data, ax=ax)
    ax.set_xlabel('Day Type')
    ax.set_ylabel('Number of Rentals')
    ax.set_title('Impact of Day Type on Bike Rentals')
    ax.set_xticklabels(['Non-working Day', 'Working Day'])
    return fig

def plot_correlation_heatmap(data):
    numeric_columns = ['temp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']
    corr_matrix = data[numeric_columns].corr()
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Correlation between Weather Variable and Customer')
    return fig

def plot_donut_chart(data):
    casual = data['casual'].sum()
    registered = data['registered'].sum()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.pie([casual, registered], labels=['Casual', 'Registered'], colors=sns.color_palette('Set2'), autopct='%1.1f%%', startangle=90, pctdistance=0.85)

    # Create a circle at the center to transform it into a donut chart
    center_circle = plt.Circle((0,0), 0.70, fc='white')
    ax.add_artist(center_circle)
    
    ax.set_title('Proporsi Penyewa Casual Dan Registered dalam Total Penyewaan Sepeda')
    
    return fig

def plot_monthly_distribution(data):
    # Aggregate data by month
    monthly_data = data.groupby('mnth').agg({
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()

    # Sort by month
    monthly_data = monthly_data.sort_values('mnth')

    # Create a horizontal bar chart
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot bars
    ax.barh(monthly_data['mnth'], monthly_data['casual'], label='Casual', color='coral')
    ax.barh(monthly_data['mnth'], monthly_data['registered'], left=monthly_data['casual'], label='Registered', color='skyblue')

    # Customize the plot
    ax.set_xlabel('Number of Rentals')
    ax.set_ylabel('Month')
    ax.set_title('Distribusi Penyewaan Sepeda per Bulan')
    ax.legend()

    # Use month names instead of numbers
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ax.set_yticks(range(1, 13))
    ax.set_yticklabels(month_names)

    # Add value labels
    for i, (casual, registered) in enumerate(zip(monthly_data['casual'], monthly_data['registered'])):
        ax.text(casual/2, i+1, f'{casual:,}', ha='center', va='center')
        ax.text(casual + registered/2, i+1, f'{registered:,}', ha='center', va='center')

    return fig



# Main content
st.header(f"Bike Rental Analysis for {year}")

# Question 1: Bagaimana Proporsi Penyewa Casual Dan Registered dalam Total Penyewaan Sepeda
st.header("1. Bagaimana Proporsi Penyewa Casual Dan Registered dalam Total Penyewaan Sepeda")
st.pyplot(plot_donut_chart(df_filtered))

# Question 2: Distribution of categorical variables
# Monthly Distribution
st.header("2. Distribusi Penyewaan Sepeda per Bulan")
st.pyplot(plot_monthly_distribution(df_filtered))

# Question 3: Korelasi antara Variabel Cuaca dan Jumlah Penyewaan
st.header("3. Apakah faktor cuaca mempengaruhi jumlah penyewaan sepeda?")
st.pyplot(plot_correlation_heatmap(df_filtered))


# Daily and Monthly Rentals
col1, col2 = st.columns(2)
with col1:
    st.subheader("Daily Bike Rentals")
    st.pyplot(plot_daily_rentals(df_filtered))
with col2:
    st.subheader("Monthly Bike Rentals")
    st.pyplot(plot_monthly_rentals(df_filtered))

# Seasonal Rentals and Weather Impact
col3, col4 = st.columns(2)
with col3:
    st.subheader("Average Bike Rentals by Season")
    st.pyplot(plot_seasonal_rentals(df_filtered))
with col4:
    st.subheader("Impact of Weather on Bike Rentals")
    st.pyplot(plot_weather_impact(df_filtered))

# Temperature, Humidity, and Wind Speed Impact
st.header("Impact of Weather Conditions on Bike Rentals")
col5, col6, col7 = st.columns(3)
with col5:
    st.pyplot(plot_temp_impact(df_filtered))
with col6:
    st.pyplot(plot_humidity_impact(df_filtered))
with col7:
    st.pyplot(plot_windspeed_impact(df_filtered))

# Day Type Impact
st.header("Impact of Day Type on Bike Rentals")
st.pyplot(plot_day_type_impact(df_filtered))

# Display raw data
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.write(df_filtered)
    st.write(f"Total records: {len(df)}")