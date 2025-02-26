import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Streamlit Title
st.title("📊 Supermarket Sales Dashboard")

st.markdown("""
**Note:** When uploading your dataset, please ensure it contains the following column names:
- `Date`   `Time` `City` `Product line` `Total`

""")


# File Upload Feature
uploaded_file = st.file_uploader("Upload your sales data (CSV file)", type=["csv"])
# Load dataset (either user-uploaded or default file)
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='latin1')
else:
    df = pd.read_csv("supermarket_sales.csv", encoding='latin1')



# Check if 'Date' column exists
if 'Date' in df.columns:
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month_name()
    df['DayOfWeek'] = df['Date'].dt.day_name()
else:
    st.error("The 'Date' column is missing from the dataset.")

# Check if 'Time' column exists
if 'Time' in df.columns:
    # Convert Time to Hour
    df['Hour'] = pd.to_datetime(df['Time']).dt.hour
else:
    st.error("The 'Time' column is missing from the dataset.")

# Check if 'City' column exists
if 'City' in df.columns:
    # Sidebar Filters
    st.sidebar.header("Filters")
    selected_city = st.sidebar.multiselect("Select City", df["City"].unique(), default=df["City"].unique())

    # Filter data
    filtered_df = df[df["City"].isin(selected_city)]

    # Show dataset preview
    if st.checkbox("Show Raw Data"):
        st.write(filtered_df)

    # Sales by Day of the Week
    if 'DayOfWeek' in df.columns and 'Total' in df.columns:
        st.subheader("🛍️ Sales by Day of the Week")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=filtered_df["DayOfWeek"], y=filtered_df["Total"], estimator=sum, ax=ax, palette="viridis")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Sales by Product Line
    if 'Product line' in df.columns:
        st.subheader("📦 Sales by Product Line")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.countplot(y=filtered_df["Product line"], order=filtered_df["Product line"].value_counts().index, palette="coolwarm")
        st.pyplot(fig)

    # Sales Trend Over Time
    if 'Date' in df.columns and 'Total' in df.columns:
        st.subheader("📅 Sales Trend Over Time")
        fig, ax = plt.subplots(figsize=(10, 5))
        filtered_df.groupby("Date")["Total"].sum().plot(ax=ax)
        ax.set_ylabel("Total Sales")
        st.pyplot(fig)

    # Peak Shopping Hours
    if 'Hour' in df.columns and 'Total' in df.columns:
        st.subheader("⏰ Peak Shopping Hours")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=filtered_df["Hour"], y=filtered_df["Total"], estimator=sum, ax=ax, palette="pastel")
        st.pyplot(fig)
else:
    st.error("The 'City' column is missing from the dataset.")