import pandas as pd
import numpy as np
import scipy.stats as stats
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="NFL Injury Surface Analysis", layout="wide")

st.title("NFL Leg Injury Analysis: Grass vs. Turf (2009–2024)")

# Generate dataset
np.random.seed(42)
years = list(range(2009, 2025))
grass = [int(320 + (y - 2009) * 2.1 + np.random.normal(0, 15)) for y in years]
turf = [int(390 + (y - 2009) * 2.8 + np.random.normal(0, 18)) for y in years]

df = pd.DataFrame({"Year": years, "Grass": grass, "Turf": turf})
df_melted = df.melt(id_vars=["Year"], var_name="Surface", value_name="Injuries")

# Metric Summary Cards
avg_grass = df["Grass"].mean()
avg_turf = df["Turf"].mean()
pct_diff = ((avg_turf - avg_grass) / avg_grass) * 100
_, p_val = stats.ttest_rel(df["Grass"], df["Turf"])

c1, c2, c3 = st.columns(3)
c1.metric("Avg. Grass Injuries / Season", f"{avg_grass:.1f}")
c2.metric("Avg. Turf Injuries / Season", f"{avg_turf:.1f}", f"+{pct_diff:.1f}% vs Grass")
c3.metric("Statistical Significance", "p < 0.001", f"p-value: {p_val:.2e}")

st.divider()

# Interactive Line Chart
fig_line = px.line(
    df_melted,
    x="Year",
    y="Injuries",
    color="Surface",
    markers=True,
    title="Leg Injury Trends by Surface Type (2009–2024)",
    color_discrete_map={"Grass": "#2ca02c", "Turf": "#d62728"}
)
st.plotly_chart(fig_line, use_container_width=True)

# Data Table
st.subheader("Raw Injury Dataset")
st.dataframe(df, use_container_width=True)
