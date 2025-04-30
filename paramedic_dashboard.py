import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Page config
st.set_page_config(
    page_title="Paramedic Refusal Compliance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("🚑 Paramedic Performance Dashboard")
st.markdown("This dashboard visualizes refusal-of-care vitals compliance performance across paramedics.")

st.markdown("⚠️ **Reminder**: Every refusal should include *two complete sets of vitals* unless explicitly refused by the patient. In those cases, refusal should be clearly documented.")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

paramedics = ['Cameron Conte', 'Levi McGinnis', 'Jake Dawson', 'Joshua Salas',
              'Courtney Rieke', 'Kyle Schlatterer', 'Reuben Ortiz', 'Joshua Jacobs', 'Derek Twardowski']
calls = [55, 45, 35, 31, 27, 27, 25, 24, 16]
raw_pass = [63.64, 51.11, 45.71, 35.48, 37.04, 40.74, 52.00, 29.17, 37.50]
adjusted_pass = [100, 93.33, 68.57, 87.10, 88.89, 88.89, 68.00, 83.33, 81.25]
monthly_rates = {
    'Cameron Conte': [33.33, 80.95, 68.42],
    'Levi McGinnis': [30.77, 73.33, 47.06],
    'Jake Dawson': [37.50, 45.45, 62.50],
    'Joshua Salas': [28.57, 40.00, 41.67],
    'Courtney Rieke': [50.00, 22.22, 37.50],
    'Kyle Schlatterer': [0.00, 44.44, 41.18],
    'Reuben Ortiz': [50.00, 50.00, 60.00],
    'Joshua Jacobs': [44.44, 50.00, 9.09],
    'Derek Twardowski': [50.00, 33.33, 33.33]
}
audit_paramedics = ['Joshua Salas', 'Courtney Rieke', 'Levi McGinnis', 'Jake Dawson',
                    'Kyle Schlatterer', 'Joshua Jacobs', 'Reuben Ortiz', 'Cameron Conte',
                    'Derek Twardowski', 'Joseph Katsiyannis']
minimal = [21, 13, 18, 5, 12, 11, 9, 9, 7, 7]
one_set = [1, 3, 0, 6, 0, 2, 1, 1, 0, 0]
two_sets = [1, 3, 1, 6, 3, 2, 1, 1, 3, 2]
compliance_scores = [74.55, 65, 62, 55, 60, 59, 50, 53, 54]

# Assemble DataFrames
df_calls = pd.DataFrame({'Paramedic': paramedics, 'Total Calls': calls})
df_pass = pd.DataFrame({'Paramedic': paramedics, 'Raw Pass Rate': raw_pass, 'Adjusted Pass Rate': adjusted_pass})
df_monthly = pd.DataFrame(monthly_rates).T.reset_index().melt(id_vars='index', var_name='Month', value_name='Raw Pass Rate')
df_monthly.columns = ['Paramedic', 'Month', 'Raw Pass Rate']
df_audit = pd.DataFrame({
    'Paramedic': audit_paramedics,
    'Minimal to No Vitals': minimal,
    '1 Vital Set': one_set,
    '2 Vital Sets': two_sets
})
df_compliance = pd.DataFrame({'Paramedic': paramedics, 'Compliance Score': compliance_scores})

# Min call volume filter
min_calls = st.sidebar.slider("Minimum Total Calls", min_value=0, max_value=max(calls), value=15)
selected = st.sidebar.multiselect("Select Paramedics", paramedics, default=paramedics)

# Filter data
df_calls = df_calls[df_calls['Paramedic'].isin(selected) & (df_calls['Total Calls'] >= min_calls)]
df_pass = df_pass[df_pass['Paramedic'].isin(df_calls['Paramedic'])]
df_monthly = df_monthly[df_monthly['Paramedic'].isin(df_calls['Paramedic'])]
df_audit = df_audit[df_audit['Paramedic'].isin(df_calls['Paramedic'])]
df_compliance = df_compliance[df_compliance['Paramedic'].isin(df_calls['Paramedic'])]

# Month dropdown
selected_month = st.sidebar.selectbox("Select Month", ["January", "February", "March"])
df_month_selected = df_monthly[df_monthly['Month'] == selected_month]

# Total Calls
fig1 = px.bar(df_calls, x='Paramedic', y='Total Calls', color='Total Calls', color_continuous_scale='Blues')
fig1.update_layout(title="Total Refusal Calls by Paramedic", xaxis_tickangle=45)
st.plotly_chart(fig1, use_container_width=True)

# Raw vs Adjusted
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=df_pass['Paramedic'], y=df_pass['Raw Pass Rate'], name='Raw Pass Rate', marker_color='crimson'))
fig2.add_trace(go.Bar(x=df_pass['Paramedic'], y=df_pass['Adjusted Pass Rate'], name='Adjusted Pass Rate', marker_color='seagreen'))
fig2.update_layout(barmode='group', title='Raw vs Adjusted Pass Rates', yaxis_title='Pass Rate (%)', xaxis_tickangle=45)
fig2.add_annotation(x='Joshua Salas', y=35.48, text="⬅️ Coached 3/15", showarrow=True, arrowhead=1)
st.plotly_chart(fig2, use_container_width=True)

# Monthly trend
fig3 = px.line(df_month_selected, x='Month', y='Raw Pass Rate', color='Paramedic', markers=True)
fig3.update_layout(title=f'Monthly Raw Pass Rate – {selected_month}', yaxis_title='Raw Pass Rate (%)')
st.plotly_chart(fig3, use_container_width=True)

# Manual Audit
fig4 = go.Figure()
fig4.add_trace(go.Bar(x=df_audit['Paramedic'], y=df_audit['Minimal to No Vitals'], name='Minimal to No Vitals', marker_color='orangered'))
fig4.add_trace(go.Bar(x=df_audit['Paramedic'], y=df_audit['1 Vital Set'], name='1 Vital Set', marker_color='dodgerblue'))
fig4.add_trace(go.Bar(x=df_audit['Paramedic'], y=df_audit['2 Vital Sets'], name='2 Vital Sets', marker_color='mediumseagreen'))
fig4.update_layout(barmode='stack', title='Manual Audit Results', yaxis_title='Audited Calls', xaxis_tickangle=45)
st.plotly_chart(fig4, use_container_width=True)

# Compliance Score
fig5 = px.bar(df_compliance, x='Paramedic', y='Compliance Score', color='Compliance Score', color_continuous_scale='Teal')
fig5.update_layout(title='Overall Compliance Score')
st.plotly_chart(fig5, use_container_width=True)

# Download
st.sidebar.download_button("Download Data CSV", df_pass.to_csv(index=False), "pass_rate_data.csv")
