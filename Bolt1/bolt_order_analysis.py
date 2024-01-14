# Building a Streamlit Dashboard for Bolt SDA Assessment

# Importing necessary packages

import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import requests
import io

warnings.filterwarnings('ignore') # helps ignore all warnings in the Dashboard

st.set_page_config(page_title="Bolt SDA Assessment!!!", page_icon="/Users/shaikh.jounaid/Desktop/flash.png",layout="wide")

# Inserting an image into the title
# image = Image.open("utilities/Bolt_Logo.png")

t1, t2 = st.columns([1,2])

# with t1:
#     st.image(image, use_column_width=False, width=150)

with t2:
    st.title("Grocery Stores SKUs Analysis")
    st.markdown('<style>div.block-container{padding-top:3rem;}</style>',unsafe_allow_html=True)

# enabling the user to upload there own file to analyse data of similar Schema but different time range

fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))

if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename)
else:
    url="https://raw.githubusercontent.com/Mavericky007/Streamlit/main/Bolt1/data2.csv"
    s=requests.get(url).content
    df=pd.read_csv(io.StringIO(s.decode('utf-8')))
    # df = pd.read_csv("data1.csv")
    # os.chdir(r"Bolt/data")
    # df = pd.read_excel("data1.xlsx")
