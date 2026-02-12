import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("European Bank Customer Churn Dashboard")

# Load dataset
df = pd.read_csv("European_Bank.csv")

# Create segmentation columns
df["AgeGroup"] = pd.cut(df["Age"],
                        bins=[0,30,45,60,100],
                        labels=["<30","30-45","46-60","60+"])

df["TenureGroup"] = pd.cut(df["Tenure"],
                           bins=[-1,2,5,10],
                           labels=["New (0-2)","Mid (3-5)","Long (6-10)"])

df["BalanceSegment"] = pd.cut(df["Balance"],
                              bins=[-1,1,100000,300000],
                              labels=["Zero","Low","High"])

# Sidebar Filters
st.sidebar.header("Filters")
geo_filter = st.sidebar.multiselect("Select Geography",
                                     df["Geography"].unique(),
                                     default=df["Geography"].unique())

df_filtered = df[df["Geography"].isin(geo_filter)]

# KPIs
col1, col2, col3 = st.columns(3)

overall_churn = df_filtered["Exited"].mean() * 100
col1.metric("Overall Churn Rate (%)", round(overall_churn,2))

high_value = df_filtered[df_filtered["Balance"] > 100000]
hv_churn = high_value["Exited"].mean() * 100
col2.metric("High Value Churn (%)", round(hv_churn,2))

inactive = df_filtered[df_filtered["IsActiveMember"] == 0]
inactive_churn = inactive["Exited"].mean() * 100
col3.metric("Inactive Customer Churn (%)", round(inactive_churn,2))

# Charts
st.subheader("Churn by Geography")
geo_churn = df_filtered.groupby("Geography")["Exited"].mean() * 100
fig1 = plt.figure()
geo_churn.plot(kind="bar")
plt.ylabel("Churn Rate (%)")
st.pyplot(fig1)

st.subheader("Churn by Age Group")
age_churn = df_filtered.groupby("AgeGroup")["Exited"].mean() * 100
fig2 = plt.figure()
age_churn.plot(kind="bar")
plt.ylabel("Churn Rate (%)")
st.pyplot(fig2)

st.subheader("Churn by Tenure Group")
tenure_churn = df_filtered.groupby("TenureGroup")["Exited"].mean() * 100
fig3 = plt.figure()
tenure_churn.plot(kind="bar")
plt.ylabel("Churn Rate (%)")
st.pyplot(fig3)

st.subheader("Churn by Balance Segment")
balance_churn = df_filtered.groupby("BalanceSegment")["Exited"].mean() * 100
fig4 = plt.figure()
balance_churn.plot(kind="bar")
plt.ylabel("Churn Rate (%)")
st.pyplot(fig4)

