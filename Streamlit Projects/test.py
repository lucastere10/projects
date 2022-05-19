### Streamlit webpage
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

### --- HEADER --- ###

"# HEADER"
"## HEADER"
"### HEADER"
"#### HEADER"
"##### HEADER"

df = pd.read_csv('streamlit\superstore.csv',encoding='cp1252')

st.write("Strike")

st.dataframe(data = df)

pd.corr()

#correlation Matrix
df_corr = df.corr()
fig, ax = plt.subplots(figsize=(10,10))
sns.heatmap(df_corr, annot = True, center = 0, cmap = 'twilight_shifted')
ax.set_title('Correlation Matrix', fontsize = 24)
