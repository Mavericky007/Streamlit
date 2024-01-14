# Building a Streamlit Dashboard for Bolt SDA Assessment

# Importing necessary packages

import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import requests
import io
import plotly.figure_factory as ff
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore') # helps ignore all warnings in the Dashboard

st.set_page_config(page_title="Bolt SDA Assessment!!!", page_icon=":bar_chart:",layout="wide")

# Inserting an image into the title
# image = Image.open("utilities/Bolt_Logo.png")

t1, t2 = st.columns([1,2])

# with t1:
#     st.image("Bolt_Logo.png", use_column_width=False, width=150)

with t2:
    st.title("Bolt Eats Order Seasonality")
    st.markdown('<style>div.block-container{padding-top:3rem;}</style>',unsafe_allow_html=True)

# enabling the user to upload there own file to analyse data of similar Schema but different time range

# fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))

# if fl is not None:
#     filename = fl.name
#     st.write(filename)
#     df = pd.read_csv(filename)
# else:
url="https://raw.githubusercontent.com/Mavericky007/Streamlit/main/Bolt1/data2.csv"
s=requests.get(url).content
data=pd.read_csv(io.StringIO(s.decode('utf-8')))

# Cleaning the data 

data["Created Date"] = pd.to_datetime(data["Created Date"], format='%d.%m.%Y')

data['Order Value(Gross)'] = data['Order Value € (Gross)'].str.replace('€', '').astype(float)

data['Cancel Reason'] = data['Cancel Reason'].fillna('none')

data['Platform'] = data['Platform'].fillna('unknown')

# Creating date pickers

col1, col2 = st.columns((2))

# Getting the min and max date
startDate = pd.to_datetime(data["Created Date"]).min()
endDate = pd.to_datetime(data["Created Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

# --- Creating the filters in the Sidebar -----

df = data

st.sidebar.header("Choose your filter: ")

# Create for Country
Country = st.sidebar.multiselect("Pick your Country", df["Country"].unique())
if not Country:
    df2 = df.copy()
else:
    df2 = df[df["Country"].isin(Country) & df["Country"] != r'\N']

# Create for City
City = st.sidebar.multiselect("Pick the City", df2["City"].unique())
if not City:
    df3 = df2.copy()
else:
    df3 = df2[df2["City"].isin(City)]

# Create for Order State
Order_State = st.sidebar.multiselect("Pick the Order Status",df3["Order State"].unique())

# Filter the data based on Mega Region, City and Device Type

if not Country and not City and not Order_State:
    filtered_df = df
elif not City and not Order_State:
    filtered_df = df[df["Country"].isin(Country)]
elif not Country and not Order_State:
    filtered_df = df[df["City"].isin(City)]
elif City and Order_State:
    filtered_df = df3[df["City"].isin(City) & df3["Order State"].isin(Order_State)]
elif Country and Order_State:
    filtered_df = df3[df["Country"].isin(Country) & df3["Order State"].isin(Order_State)]
elif Country and City:
    filtered_df = df3[df["Country"].isin(Country) & df3["City"].isin(City)]
elif Order_State:
    filtered_df = df3[df3["Order State"].isin(Order_State)]
else:
    filtered_df = df3[df3["Country"].isin(Country) & df3["City"].isin(City) & df3["Order State"].isin(Order_State)]


# -----------------------Ploting a line chart for seasonality in Ghana-----------------------
    
ghana_df = filtered_df[filtered_df['Country'] == 'Ghana']

datewise_order_data1 = ghana_df.groupby(['Country', 'Created Date']).size().reset_index(name='Total Orders')

st.markdown("## Checking for seasonality in Ghana")

# fitler dataframe for Ghana
# datewise_order_data_ghana = datewise_order_data[datewise_order_data['Country'] == 'Ghana']

fig2 = px.line(datewise_order_data1, x='Created Date', y='Total Orders', height=500, width = 1000, template="gridon")

st.plotly_chart(fig2,use_container_width=True)

text = """
### From the above plot we see some seasonality in Ghana (But look below for the more deepdive)
"""

st.markdown(text)

# ---------------------------Checking for day of the weeks behaviour in Ghana--------------------------


st.markdown("## Checking for day of the week order patern for Ghana")


# creating a column with day of the week
ghana_df['day'] = ghana_df['Created Date'].dt.day_name()

# Aggregate data by Country and Created Date for the total order count
day_order_data = ghana_df.groupby(['Country', 'day']).size().reset_index(name='Total Orders')

# Define the order of the days
days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Convert 'day' column to a categorical type with the specified order
day_order_data['day'] = pd.Categorical(day_order_data['day'], categories=days_order, ordered=True)

# Sort the data frame based on the 'day' column to ensure the order is maintained in the plot
day_order_data = day_order_data.sort_values('day')

fig2 = px.line(day_order_data, x='day', y='Total Orders', height=500, width = 1000, template="gridon")

st.plotly_chart(fig2,use_container_width=True)

text = """
### From the above plot it is evident that Ghana has more inflow of orders on "Tuesday","Wednesday","Thursday"
"""

st.markdown(text)


# -----------------------Ploting a line chart for seasonality in Portugal-----------------------
    
st.markdown("## Checking for seasonality in Portugal")

Portugal_df = filtered_df[filtered_df['Country'] == 'Portugal']

datewise_order_data2 = Portugal_df.groupby(['Country', 'Created Date']).size().reset_index(name='Total Orders')

# fitler dataframe for Ghana
# datewise_order_data_ghana = datewise_order_data[datewise_order_data['Country'] == 'Ghana']

fig2 = px.line(datewise_order_data2, x='Created Date', y='Total Orders', height=500, width = 1000, template="gridon",color_discrete_sequence=["#EE4E34"])

st.plotly_chart(fig2,use_container_width=True)

text = """
### From the above plot we see some seasonality in Portugal (But look below for the more deepdive)
"""

st.markdown(text)

# ---------------------------Checking for day of the weeks behaviour in Portugal--------------------------


st.markdown("## Checking for day of the week order patern for Portugal")


# creating a column with day of the week
Portugal_df['day'] = Portugal_df['Created Date'].dt.day_name()

# Aggregate data by Country and Created Date for the total order count
day_order_data = Portugal_df.groupby(['Country', 'day']).size().reset_index(name='Total Orders')

# Define the order of the days
days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Convert 'day' column to a categorical type with the specified order
day_order_data['day'] = pd.Categorical(day_order_data['day'], categories=days_order, ordered=True)

# Sort the data frame based on the 'day' column to ensure the order is maintained in the plot
day_order_data = day_order_data.sort_values('day')

fig2 = px.line(day_order_data, x='day', y='Total Orders', height=500, width = 1000, template="gridon",color_discrete_sequence=["#EE4E34"])

st.plotly_chart(fig2,use_container_width=True)

text = """
### From the above plot it is evident that Ghana has more inflow of orders on "Wednesday","Thursday","Friday"
"""

st.markdown(text)
