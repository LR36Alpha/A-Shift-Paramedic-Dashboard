import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Paramedic Performance Overview: Vital Sign Acquisition in Refusal Calls")

# Data
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

# Chart 1: Total Call Volume
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.bar(paramedics, calls, color='skyblue')
ax1.set_title('Total Refusal Calls by Paramedic')
ax1.set_xlabel('Paramedic')
ax1.set_ylabel('Total Calls')
plt.xticks(rotation=45, ha='right')
st.pyplot(fig1)

# Chart 2: Raw and Adjusted Pass Rates
fig2, ax2 = plt.subplots(figsize=(12, 6))
x = np.arange(len(paramedics))
width = 0.35
ax2.bar(x - width/2, raw_pass, width, label='Raw Pass Rate', color='lightcoral')
ax2.bar(x + width/2, adjusted_pass, width, label='Adjusted Pass Rate', color='lightgreen')
ax2.set_title('Raw vs. Adjusted Pass Rates by Paramedic')
ax2.set_xlabel('Paramedic')
ax2.set_ylabel('Pass Rate (%)')
ax2.set_xticks(x)
ax2.set_xticklabels(paramedics, rotation=45, ha='right')
ax2.legend()
st.pyplot(fig2)

# Chart 3: Monthly Raw Pass Rate Trends
fig3, ax3 = plt.subplots(figsize=(10, 6))
months = ['January', 'February', 'March']
for paramedic, rates in monthly_rates.items():
    ax3.plot(months, rates, marker='o', label=paramedic)
ax3.set_title('Monthly Raw Pass Rate Trends')
ax3.set_xlabel('Month')
ax3.set_ylabel('Raw Pass Rate (%)')
ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig3)

# Chart 4: Manual Audit Outcomes
fig4, ax4 = plt.subplots(figsize=(12, 6))
ax4.bar(audit_paramedics, minimal, label='Minimal to No Vitals', color='salmon')
ax4.bar(audit_paramedics, one_set, bottom=minimal, label='1 Vital Set', color='lightblue')
ax4.bar(audit_paramedics, two_sets, bottom=np.array(minimal)+np.array(one_set), label='2 Vital Sets', color='lightgreen')
ax4.set_title('Manual Audit Outcomes by Paramedic')
ax4.set_xlabel('Paramedic')
ax4.set_ylabel('Number of Audited Calls')
plt.xticks(rotation=45, ha='right')
ax4.legend()
st.pyplot(fig4)

# Chart 5: Compliance Score
fig5, ax5 = plt.subplots(figsize=(10, 6))
ax5.bar(paramedics, compliance_scores, color='lightseagreen')
ax5.set_title('Compliance Score by Paramedic')
ax5.set_xlabel('Paramedic')
ax5.set_ylabel('Compliance Score (%)')
plt.xticks(rotation=45, ha='right')
st.pyplot(fig5)
