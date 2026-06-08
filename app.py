import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales & Revenue Analysis Dashboard")
st.subheader("Thiranex Intern Task - Nandini")

# Load data
df = pd.read_csv('sales_data.csv')
df['Revenue'] = df['Quantity'] * df['Price']
df['Date'] = pd.to_datetime(df['Date'])

# Sidebar filters
st.sidebar.header("Filters")
region = st.sidebar.multiselect("Select Region", df['Region'].unique(), default=df['Region'].unique())
category = st.sidebar.multiselect("Select Category", df['Category'].unique(), default=df['Category'].unique())

df_filtered = df[(df['Region'].isin(region)) & (df['Category'].isin(category))]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"{df_filtered['Quantity'].sum():,}")
col2.metric("Total Revenue", f"₹{df_filtered['Revenue'].sum():,}")
col3.metric("Avg Order Value", f"₹{df_filtered['Revenue'].mean():,.0f}")

# Charts
col1, col2 = st.columns(2)
with col1:
    fig1 = px.line(df_filtered.groupby('Date')['Revenue'].sum().reset_index(), 
                   x='Date', y='Revenue', title='Revenue Trend')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(df_filtered.groupby('Product')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False).head(5),
                  x='Product', y='Revenue', title='Top 5 Products')
    st.plotly_chart(fig2, use_container_width=True)

st.dataframe(df_filtered)
