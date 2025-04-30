
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Set Streamlit page configuration
st.set_page_config(
    page_title="🚒 Paramedic Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚒 Paramedic Performance Dashboard")
st.markdown("This dashboard displays refusal call compliance by paramedics, including raw pass rates, audit outcomes, and compliance scores.")

# Data for the dashboard
data = {
    "Paramedic": [
        "Cameron Conte", "Levi McGinnis", "Jake Dawson", "Joshua Salas",
        "Courtney Rieke", "Kyle Schlatterer", "Reuben Ortiz", "Joshua Jacobs", "Derek Twardowski"
    ],
    "Total Calls": [55, 45, 35, 31, 27, 27, 25, 24, 16],
    "Raw Pass Rate": [63.64, 51.11, 45.71, 35.48, 37.04, 40.74, 52.00, 29.17, 37.50],
    "Adjusted Pass Rate": [100, 93.33, 68.57, 87.10, 88.89, 88.89, 68.00, 83.33, 81.25],
    "Compliance Score": [74.55, 65.00, 62.00, 55.00, 60.00, 59.00, 50.00, 53.00, 54.00],
    "Jan Pass Rate": [33.33, 30.77, 37.50, 28.57, 50.00, 0.00, 50.00, 44.44, 50.00],
    "Feb Pass Rate": [80.95, 73.33, 45.45, 40.00, 22.22, 44.44, 50.00, 50.00, 33.33],
    "Mar Pass Rate": [68.42, 47.06, 62.50, 41.67, 37.50, 41.18, 60.00, 9.09, 33.33]
}

df = pd.DataFrame(data)

# Sidebar filters
st.sidebar.header("Filter Options")
min_calls = st.sidebar.slider("Minimum Calls", min_value=0, max_value=60, value=15)
selected_month = st.sidebar.selectbox("Select Month", ["January", "February", "March"])
month_col = {
    "January": "Jan Pass Rate",
    "February": "Feb Pass Rate",
    "March": "Mar Pass Rate"
}[selected_month]

df_filtered = df[df["Total Calls"] >= min_calls]

# Total Calls
fig_calls = px.bar(df_filtered, x="Paramedic", y="Total Calls", color="Total Calls", color_continuous_scale="Blues")
fig_calls.update_layout(title="Total Refusal Calls by Paramedic", xaxis_tickangle=45)
st.plotly_chart(fig_calls, use_container_width=True)

# Raw vs Adjusted
fig_pass = go.Figure()
fig_pass.add_trace(go.Bar(x=df_filtered["Paramedic"], y=df_filtered["Raw Pass Rate"], name="Raw", marker_color="crimson"))
fig_pass.add_trace(go.Bar(x=df_filtered["Paramedic"], y=df_filtered["Adjusted Pass Rate"], name="Adjusted", marker_color="seagreen"))
fig_pass.update_layout(barmode="group", title="Raw vs Adjusted Pass Rates", yaxis_title="%", xaxis_tickangle=45)
st.plotly_chart(fig_pass, use_container_width=True)

# Compliance Score
df_sorted = df_filtered.sort_values(by="Compliance Score", ascending=False)
fig_compliance = px.bar(
    df_sorted,
    x="Paramedic", y="Compliance Score", color="Compliance Score",
    color_continuous_scale=px.colors.sequential.Bluered_r,
    title="Compliance Score (High = Blue, Low = Red)"
)
fig_compliance.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig_compliance, use_container_width=True)

# Monthly View
fig_month = px.bar(
    df_filtered.sort_values(by=month_col, ascending=False),
    x="Paramedic", y=month_col, color=month_col,
    color_continuous_scale="RdYlGn",
    title=f"{selected_month} Raw Pass Rate"
)
fig_month.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig_month, use_container_width=True)

# Download
csv = df.to_csv(index=False)
st.sidebar.download_button("Download Data as CSV", csv, "paramedic_summary.csv", "text/csv")
