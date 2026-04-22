import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import date

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Nigerian Incidence Dashboard",
    layout="wide",
    page_icon="📊"
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("Gbemisola.csv")

# User profile
st.sidebar.title("User profile")
st.sidebar.write("Ajagunna Gbemisola")
st.sidebar.write("Data analyst")

# Clean Columns
df.columns = df.columns.str.strip()

# Convert Dates
df["Start date"] = pd.to_datetime(df["Start date"], errors="coerce")
df["End date"] = pd.to_datetime(df["End date"], errors="coerce")

# Create Features
df["Duration"] = (df["End date"] - df["Start date"]).dt.days.fillna(0)
df["Year"] = df["Start date"].dt.year

# ---------------- TITLE ----------------
st.title("Nigerian Incidence Dashboard")
st.markdown("Interactive dashboard showing deaths, incidents, trends and affected states.")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Filter Data")

selected_states = st.sidebar.multiselect(
    "Select State(s)",
    options=sorted(df["State"].dropna().unique())
)

start_date = st.sidebar.date_input(
    "Start Date",
    value=df["Start date"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=df["Start date"].max().date()
)

# ---------------- FILTER DATA ----------------
filtered_df = df.copy()

if selected_states:
    filtered_df = filtered_df[
        filtered_df["State"].isin(selected_states)
    ]

filtered_df = filtered_df[
    (filtered_df["Start date"].dt.date >= start_date) &
    (filtered_df["Start date"].dt.date <= end_date)
]

# ---------------- KPI SECTION ----------------
st.subheader("Key Metrics Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Deaths",
    f"{filtered_df['Number of deaths'].sum():,}"
)

col2.metric(
    "Total Incidents",
    f"{filtered_df.shape[0]:,}"
)

col3.metric(
    "Affected States",
    f"{filtered_df['State'].nunique():,}"
)

col4.metric(
    "Avg Duration",
    f"{filtered_df['Duration'].mean():.1f} days"
)

st.markdown("---")

# ---------------- CHARTS ----------------



# Q1. Top 10 deadliest incidents
st.subheader("Q1. Top 10 deadliest incidents")
top10 =filtered_df.nlargest(10, 'Number of deaths')[['Incident','State','Number of deaths']]
fig1= px.bar(top10, x='Incident', y='Number of deaths',
color='State', title="Top 10 Deadliest Incidents")
st.plotly_chart(fig1, use_container_width=True)
st.dataframe(top10)
st.markdown("Insights:The chart reveals that armed conflict and insecurity are the leading causes of mass deaths but environmental disasters and accidents also play a substantial role.")

# Q2. Top 10 states with the highest total deaths
st.subheader("2. Top 10 States with Highest Total Deaths")
q2 =filtered_df.groupby("State")["Number of deaths"].sum().sort_values(ascending=False).head(10).reset_index()
fig2 = px.bar(q2, x="State", y="Number of deaths")
st.plotly_chart(fig2)
st.markdown("Insights:Borno has the highest fatalities by far while states like Anambra and Ogun show much lower totals,highlighting a wide regional gap in death tolls.")

# Q3. Which incidents lasted the longest?
st.subheader("3. Which incidents lasted the longest")
longest_incidents = filtered_df[['Incident','Duration']].sort_values(by='Duration',ascending=False).head(10)
st.bar_chart(longest_incidents.set_index('Incident'))
st.markdown("Insights:Flood disasters lasted far longer than other incidents while auto crashes and police clashes were brief in comparison")

# Q4. How do deaths vary year by year?
st.subheader("4. How do deaths vary year by year")
year_deaths =filtered_df.groupby("Year")["Number of deaths"].sum()
fig4,ax4 = plt.subplots(figsize=(8,4))
ax4.plot(year_deaths.index, year_deaths.values, marker="o", color="navy")
ax4.set_title("Annual Deaths Trend")
ax4.set_xlabel("Year")
ax4.set_ylabel("Number of Deaths")
st.pyplot(fig4)
st.markdown("Insights:Deaths peaked sharply in 2023 to 2024 before dropping steeply in 2025,showing a dramatic shift in annual fatalities.")

# Q5. Which states had the most incidents(not deaths)?
st.subheader("5. Which states had the most incidents(not deaths)")
incident_counts = filtered_df["State"].value_counts().nlargest(5)
fig5,ax5 = plt.subplots(figsize=(5,5))
ax5.pie(incident_counts, labels=incident_counts.index, autopct='%1.1f%%', startangle=90)
ax5.set_title("Top 5 States by Incident Count")
st.pyplot(fig5)
st.markdown("Insights:Lagos holds the largest share of incidents,followed by Ogun and Kaduna while Delta and Benue account for smaller portions.")