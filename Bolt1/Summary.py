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
    st.title("Bolt Eats Order Analysis")
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



#  Calculating the Scorecard values for each stage in the sales converstion

total_orders = filtered_df.count().max()
gross_booking = filtered_df[('Order Value(Gross)')].sum()
avg_delivery_time = filtered_df[('Delivery Time')].mean()
total_restraunts = filtered_df[('Restaurant ID')].nunique()

# inserting metrics in the Analysis
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Calculating the ROC for Gross Bookings
    orders_df = filtered_df.groupby(['Created Date']).size().reset_index(name='Total Orders')
    orders_df['RoC'] = orders_df['Total Orders'].pct_change() * 100
    orders_df = orders_df.dropna()
    latest_month_roc = orders_df['RoC'].iloc[-1]

    st.metric("Total Orders",f'{total_orders:,}', f'{latest_month_roc:.2f}%')

with col2:
    # Calculating the ROC for Trips
    gross_df = filtered_df.groupby(by = ["Created Date"], as_index = False)["Order Value(Gross)"].sum()
    gross_df['RoC'] = gross_df['Order Value(Gross)'].pct_change() * 100
    gross_df = gross_df.dropna()
    latest_month_roc = gross_df['RoC'].iloc[-1]

    st.metric("Gross Bookings", f'${gross_booking:,}', f'{latest_month_roc:.2f}%')

with col3:
    # Calculating the ROC for customers
    del_time = filtered_df.groupby(by = ["Created Date"], as_index = False)["Delivery Time"].mean()
    del_time['RoC'] = del_time['Delivery Time'].pct_change() * 100
    del_time = del_time.dropna()
    latest_month_roc = del_time['RoC'].iloc[-1]

    st.metric("Avg Delivery Time", f'{avg_delivery_time:,.2f} Mins', f'{latest_month_roc:.2f}%')

with col4:
    # Calculating the ROC for Active Orgs
    restraut_df = filtered_df.groupby(by = ["Created Date"], as_index = False)["Restaurant ID"].nunique()
    restraut_df['RoC'] = restraut_df['Restaurant ID'].pct_change() * 100
    restraut_df = restraut_df.dropna()
    latest_month_roc = restraut_df['RoC'].iloc[-1]

    st.metric("Active Restaurants", f'{total_restraunts:,}', f'{latest_month_roc:.2f}%')


# creating columns to add pie chart and column chart

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Country Vs Total Gross Booking")
    fig = px.pie(filtered_df, values = "Order Value(Gross)", names = "Country", hole = 0.5)
    fig.update_traces(text = filtered_df["Country"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)
with col2:
    st.subheader("Order Status Vs Total Orders")
    colors = ['#EEA47F', '#00539C']
    fig = px.pie(filtered_df, names = "Order State", hole = 0.5,color_discrete_sequence=colors)
    fig.update_traces(text = filtered_df["Order State"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)
with col3:
    st.subheader("Platform Vs Total Orders")
    colors = ['#2BAE66', '#FCF6F5']
    fig = px.pie(filtered_df, names = "Platform", hole = 0.5,color_discrete_sequence=colors)
    fig.update_traces(text = filtered_df["Platform"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)


col1, col2, col3 = st.columns(3)


with col1:
    # Display the top cuisines

    top_cuisines = filtered_df['Cuisine'].value_counts().head(10)
    st.markdown("### Here are the top 10 cuisines:")
    # st.write("Here are the top 5 cuisines in the dataset:")
    for i, (cuisine, count) in enumerate(top_cuisines.items(), start=1):
        st.write(f"{i}) {cuisine} - {count:,} Orders Placed")

with col2:
    # Display the top cuisines

    top_restautant = filtered_df['Restaurant Name'].value_counts().head(10)
    st.markdown("### Here are the top 10 Restaurant:")
    # st.write("Here are the top 5 cuisines in the dataset:")
    for i, (Restaurant, count) in enumerate(top_restautant.items(), start=1):
        st.write(f"{i}) {Restaurant} - {count:,} Orders Placed")

with col3:
    try:
        platform_payment_relation = filtered_df.groupby(['Platform', 'Payment Method']).size().unstack().fillna(0)

        # Display the findings
        # st.write("Analysis of Payment Types for Android and iOS Platforms:")
        st.markdown("### Platform & Payment Methods:")
        for platform in platform_payment_relation.index:
            cash_payments = platform_payment_relation.loc[platform, 'cash']
            cashless_payments = platform_payment_relation.loc[platform, 'cashless']
            st.write(f"{platform.capitalize()} Platform:")
            st.write(f"    -  Cash payments: {cash_payments:,.0f}")
            st.write(f"    -  Cashless payments: {cashless_payments:,.0f}")
    except:
        st.write("⚠️ This Info is not filtered down to Country Level for now") # having issues with Portugal filter need to investigate

st.markdown("##")

# ----------------- Creaeting a time serier chat for time Vs Order Value -----------------

st.subheader('Time Series Analysis By Country')

# linechart = pd.DataFrame(filtered_df.groupby(filtered_df["Created Date","Country"])["Order Value(Gross)"].sum()).reset_index(name='Orders Value')
# fig2 = px.line(linechart, x = "Created Date", y="Order Value(Gross)",height=500, width = 1000,template="gridon", color='Country')

linechart = filtered_df.groupby(['Created Date', 'Country'])["Order Value(Gross)"].sum().reset_index(name='Orders Value')

# Plotting the line chart
fig2 = px.line(linechart, x='Created Date', y='Orders Value', color='Country', height=500, width = 1000, template="gridon")

st.plotly_chart(fig2,use_container_width=True)

# --------------------------Plotting a delivery histrogram--------------------------

st.subheader('This is a histogram of delivery up to 60 minutes')
st.write("This Histogram helps us understand the volume of Users that had a potential bad experience")

fig = px.histogram(data[data['Delivery Time'] <= 100], x='Delivery Time', nbins=60, color_discrete_sequence=['#ffd700'])
fig.update_xaxes(title_text='Delivery Time (minutes)')
fig.update_yaxes(title_text='Total Orders')
fig.update_layout(xaxis_range=[0, 60])  # Limiting x-axis to 60 minutes
# fig.update_layout(dragmode='select')
st.plotly_chart(fig, use_container_width=True)

# --------------------------Plotting a delivery histrogram--------------------------

st.subheader('This is a histogram of delivery up to 60 minutes')
st.write("This Histogram helps us understand the volume of Users that had a potential bad experience")

fig = px.histogram(data[data['Delivery Time'] <= 100], x='Delivery Time', nbins=60, color_discrete_sequence=['#ffd700'])
fig.update_xaxes(title_text='Delivery Time (minutes)')
fig.update_yaxes(title_text='Total Orders')
fig.update_layout(xaxis_range=[0, 60])  # Limiting x-axis to 60 minutes
# fig.update_layout(dragmode='select')
st.plotly_chart(fig, use_container_width=True)



st.markdown("## Go to the next tab to look into [Seasonality](https://bolt-order-analysis.streamlit.app/Seasonality#bolt-eats-order-analysis)")


