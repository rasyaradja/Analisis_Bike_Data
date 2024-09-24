import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Set page title
st.set_page_config(page_title="Rasya Bike Sharing", layout="wide")

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")
    return df

df = load_data()

# Sidebar
st.sidebar.title("Made By Rasya") 
st.sidebar.markdown("check out my [linkedin](https://www.linkedin.com/in/rasyaradja/)")
st.sidebar.markdown("Explore patterns and trends in your data.")

# Main content
st.title("Interactive Data Analysis Dashboard")

# Overview
st.header("Dataset Overview")
st.write(df.head())
st.write(f"Total records: {len(df)}")

# Column selection
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
categorical_columns = df.select_dtypes(include=['object']).columns

# Time series analysis (if applicable)
date_columns = df.select_dtypes(include=['datetime64', 'datetime64[ns]']).columns
if len(date_columns) > 0:
    st.header("Time Series Analysis")
    date_column = st.selectbox("Select date column", date_columns)
    value_column = st.selectbox("Select value column", numeric_columns)

    df[date_column] = pd.to_datetime(df[date_column])
    time_unit = st.selectbox("Select time unit", ["Day", "Week", "Month"])

    if time_unit == "Day":
        grouped_data = df.groupby(df[date_column].dt.date)[value_column].sum().reset_index()
    elif time_unit == "Week":
        grouped_data = df.groupby(df[date_column].dt.isocalendar().week)[value_column].sum().reset_index()
    else:
        grouped_data = df.groupby(df[date_column].dt.to_period('M'))[value_column].sum().reset_index()
        grouped_data[date_column] = grouped_data[date_column].dt.to_timestamp()


# Categorical analysis
if len(categorical_columns) > 0:
    st.header("Categorical Analysis")
    cat_column = st.selectbox("Select categorical column", categorical_columns)
    value_column = st.selectbox("Select value column for categorical analysis", numeric_columns)

    cat_data = df.groupby(cat_column)[value_column].mean().reset_index()

    chart_type = st.radio("Select chart type", ["Bar", "Pie", "Box"])

    if chart_type == "Bar":
        fig = px.bar(cat_data, x=cat_column, y=value_column, title=f'Average {value_column} by {cat_column}')
    elif chart_type == "Pie":
        fig = px.pie(cat_data, values=value_column, names=cat_column, title=f'Distribution of {value_column} by {cat_column}')
    else:  # Box plot
        fig = px.box(df, x=cat_column, y=value_column, title=f'Distribution of {value_column} by {cat_column}')    

    st.plotly_chart(fig)

# Scatter plot
st.header("Scatter Plot")
x_column = st.selectbox("Select X-axis", numeric_columns, key="scatter_x")
y_column = st.selectbox("Select Y-axis", numeric_columns, key="scatter_y")
color_column = st.selectbox("Select color column (optional)", ["None"] + list(categorical_columns))

if color_column == "None":
    fig = px.scatter(df, x=x_column, y=y_column, title=f'{y_column} vs {x_column}')
else:
    fig = px.scatter(df, x=x_column, y=y_column, color=color_column, title=f'{y_column} vs {x_column}, colored by {color_column}')
    st.plotly_chart(fig)

if color_column == "None":
    fig = px.scatter(df, x=x_column, y=y_column, title=f'{y_column} vs {x_column}')
else:
    fig = px.scatter(df, x=x_column, y=y_column, color=color_column, title=f'{y_column} vs {x_column}, colored by {color_column}')
    st.plotly_chart(fig)

# Histogram
st.header("Histogram")
hist_column = st.selectbox("Select column for histogram", numeric_columns)
bin_count = st.slider("Number of bins", min_value=5, max_value=100, value=30)

fig = px.histogram(df, x=hist_column, nbins=bin_count, title=f'Histogram of {hist_column}')
st.plotly_chart(fig)

# Correlation heatmap
st.header("Feature Correlation")
correlation_matrix = df[numeric_columns].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
plt.title('Correlation Heatmap')
st.pyplot(fig)

# Heatmap
if len(numeric_columns) > 1:
    st.header("Heatmap")
    heatmap_columns = st.multiselect("Select columns for heatmap", numeric_columns)
    
    if len(heatmap_columns) > 1:
        correlation_matrix = df[heatmap_columns].corr()
        fig = px.imshow(correlation_matrix, 
                        labels=dict(color="Correlation"),
                        x=correlation_matrix.columns,
                        y=correlation_matrix.columns,
                        title="Correlation Heatmap")
        st.plotly_chart(fig)
    else:
        st.write("Please select at least two columns for the heatmap.")

# Pair plot
if len(numeric_columns) > 1:
    st.header("Pair Plot")
    pair_columns = st.multiselect("Select columns for pair plot", numeric_columns)
    
    if len(pair_columns) > 1:
        fig = sns.pairplot(df[pair_columns])
        st.pyplot(fig)
    else:
        st.write("Please select at least two columns for the pair plot.")

# Basic statistics
st.header("Basic Statistics")
st.write(df.describe())



# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Dashboard created with Streamlit")