### Streamlit webpage

#Imports
from doctest import DocFileSuite
from string import hexdigits
from turtle import heading, right

import streamlit as st
from streamlit_lottie import st_lottie
import requests

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as pxrun
import plotly.io as pio


#Page config
st.set_page_config(page_title = "Lucas Caldas | Dashboards", page_icon=":bar_chart:", layout = 'wide')

# --- LOAD ASSETS --- #
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_profile = load_lottie('https://assets7.lottiefiles.com/packages/lf20_npd3g4ks.json')
lottie_skills = load_lottie('https://assets5.lottiefiles.com/packages/lf20_eux2nl1l.json')

# --- HEADER SECTION --- #
st.subheader("I'm Lucas Caldas, aspiring Production Engineer.")

with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.title("Streamlit Dashboard Portfolio")
        st.write(
            """
            Welcome to my dashboard portfolio. \n
            I'm Lucas Caldas, aspiring Production Engineer. \n
            Have interests in Data Science and Machine Learning. \n
            For my personal ML portfolio, please visit the link bellow: \n
            [Learn More >](https://lucastere10.github.io/portfolio/)""")
    with right_column:    
        st_lottie(lottie_profile, height=300,key='skills')

# --- SKILLS SECTION --- #
with st.container():
    st.write("---")
    st.header("Skills")
    left_column, right_column = st.columns(2)
    with left_column:    
        st.write(
        """
        What do I do:
        - Python for Data Science & Machine Learning Algorithms.
        - VBA experiece for Automation & Web Scrapping.
        - Power BI with DAX & Power Query M Languages
        Other experiences including:
        - SQL
        - R Language
        - MS Project
        """)
    with right_column:    
        st_lottie(lottie_skills, height=300,key='profile')

# --- MY PROJECTS --- #
with st.container():
    st.write("---")
    st.header("My Projects") 
    st.write("##")
    image_column, text_column = st.columns((1,2))
    with image_column:
        # insert image
        st.write("")
    with text_column:
        st.subheader("Superstore Streamlit Dashboard")
        st.write(''' - Text Here See Dashboard''')

# --- Contact Me --- #

with st.container():
    st.write('---')
    st.header("Contact Me") 
    st.write('''
    - E-mail:	lucasmedeiroscaldas@yahoo.com.br
    - LinkedIn:	https://www.linkedin.com/in/lucas-caldas50/
    - Github:	https://github.com/lucastere10/
    - Instagram: https://www.instagram.com/lucas.mcaldas/
    - Résumé: [Google Drive](https://drive.google.com/file/d/1lFKemF02INTZ-tgHS3f1Qm5b0wr52bLF/view?usp=sharing)
    ''')
    st.write('Feel free to leave me message:  [Contact Me >](https://lucastere10.github.io/portfolio/contact/)')