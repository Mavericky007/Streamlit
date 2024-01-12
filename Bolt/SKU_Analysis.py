
# Building a Streamlit Dashboard for Bolt SDA Assessment

# Importing necessary packages

import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore') # helps ignore all warnings in the Dashboard

st.set_page_config(page_title="Bolt SDA Assessment!!!", page_icon="/Users/shaikh.jounaid/Desktop/flash.png",layout="wide")

# # Inserting an image into the title
# image = open("Bolt-Logo.png", 'rb')

t1, t2 = st.columns([1, 2])
# with t1:
    # st.image("utilities/Bolt_Logo.png", use_column_width=False, width=150)
with t2:
    st.title("Grocery Stores SKUs Analysis")
    st.markdown('<style>div.block-container{padding-top:3rem;}</style>',unsafe_allow_html=True)

# enabling the user to upload there own file to analyse data of similar Schema but different time range

fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))

if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    os.chdir(r"Bolt/data")
    # df = pd.read_csv("Superstore.csv", encoding = "ISO-8859-1")
    df = pd.read_excel("data1.xlsx")

col1, col2 = st.columns((2))

# df["Time"] = pd.to_datetime(df["Time"])  # Incase the time column was not in datatime format

# Getting the min and max date
startDate = pd.to_datetime(df["Time"]).min()
endDate = pd.to_datetime(df["Time"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Time"] >= date1) & (df["Time"] <= date2)].copy()

# ------------------------------- Creating the Sidebar filters Below -------------------------------

st.sidebar.header("Choose your filter: ")

# Create for Category1
Category1 = st.sidebar.multiselect("Pick your Category level 1", df["Category level 0"].unique())
if not Category1:
    df2 = df.copy()
else:
    df2 = df[df["Category level 0"].isin(Category1)]

# Create for Category2
Category2 = st.sidebar.multiselect("Pick your Category level 2", df2["Category level 1"].unique())
if not Category2:
    df3 = df2.copy()
else:
    df3 = df2[df2["Category level 1"].isin(Category2)]

# Create for Category3
Category3 = st.sidebar.multiselect("Pick your Category level 3",df3["Category level 2"].unique())

# Filter the data based on Category1, Category2 and Category3

if not Category1 and not Category2 and not Category3:
    filtered_df = df
elif not Category2 and not Category3:
    filtered_df = df[df["Category level 0"].isin(Category1)]
elif not Category1 and not Category3:
    filtered_df = df[df["Category level 1"].isin(Category2)]
elif Category2 and Category3:
    filtered_df = df3[df["Category level 1"].isin(Category2) & df3["Category level 2"].isin(Category3)]
elif Category1 and Category3:
    filtered_df = df3[df["Category level 0"].isin(Category1) & df3["Category level 2"].isin(Category3)]
elif Category1 and Category2:
    filtered_df = df3[df["Category level 0"].isin(Category1) & df3["Category level 1"].isin(Category2)]
elif Category3:
    filtered_df = df3[df3["Category level 2"].isin(Category3)]
else:
    filtered_df = df3[df3["Category level 0"].isin(Category1) & df3["Category level 1"].isin(Category2) & df3["Category level 2"].isin(Category3)]

st.markdown("##") # addind one line gap

# -------------------- Calculating the Scorecard values for each dimension in the dataset --------------------

sku_listing = filtered_df[('Unique SKUs Listed')].sum()
sku_sold = filtered_df[('Unique SKUs Sold')].sum()
unit_sold = filtered_df[('# of sold SKU items')].sum()
Gross_Price = filtered_df[('Price before Discount (includ. VAT) (EUR)')].sum()
net_spent = filtered_df[('Discount Value (EUR)')].sum()
net_earning = filtered_df [('Item COGS (net VAT) (EUR)')].sum()

# Calculating the ROC for each

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    # Calculating the ROC for Pageviews
    df = filtered_df.groupby(by = ["Time"], as_index = False)["Unique SKUs Listed"].sum()
    df['RoC'] = df['Unique SKUs Listed'].pct_change() * 100
    df = df.dropna()
    latest_month_roc = df['RoC'].iloc[-1]

    st.metric("Total SKU's Listed",f'{sku_listing:,}', f'{latest_month_roc:.2f}%')

with col2:
    # Calculating the ROC for Pageviews
    df = filtered_df.groupby(by = ["Time"], as_index = False)["Unique SKUs Sold"].sum()
    df['RoC'] = df['Unique SKUs Sold'].pct_change() * 100
    df = df.dropna()
    latest_month_roc = df['RoC'].iloc[-1]

    st.metric("Total SKU's Sold",f'{sku_sold:,}', f'{latest_month_roc:.2f}%')

with col3:
    # Calculating the ROC for Pageviews
    df = filtered_df.groupby(by = ["Time"], as_index = False)["# of sold SKU items"].sum()
    df['RoC'] = df['# of sold SKU items'].pct_change() * 100
    df = df.dropna()
    latest_month_roc = df['RoC'].iloc[-1]

    st.metric("Total Units Sold",f'{unit_sold:,}', f'{latest_month_roc:.2f}%')

with col4:
    # Calculating the ROC for Pageviews
    df = filtered_df.groupby(by = ["Time"], as_index = False)["Price before Discount (includ. VAT) (EUR)"].sum()
    df['RoC'] = df['Price before Discount (includ. VAT) (EUR)'].pct_change() * 100
    df = df.dropna()
    latest_month_roc = df['RoC'].iloc[-1]

    st.metric("Gross Price (before discount)",f'{Gross_Price:,.2f}', f'{latest_month_roc:.2f}%')

with col5:
    # Calculating the ROC for Pageviews
    df = filtered_df.groupby(by = ["Time"], as_index = False)["Discount Value (EUR)"].sum()
    df['RoC'] = df['Discount Value (EUR)'].pct_change() * 100
    df = df.dropna()
    latest_month_roc = df['RoC'].iloc[-1]

    st.metric("Net Spent (discount)",f'{net_spent:,.2f}', f'{latest_month_roc:.2f}%')

with col6:
    # Calculating the ROC for Pageviews
    df = filtered_df.groupby(by = ["Time"], as_index = False)["Item COGS (net VAT) (EUR)"].sum()
    df['RoC'] = df['Item COGS (net VAT) (EUR)'].pct_change() * 100
    df = df.dropna()
    latest_month_roc = df['RoC'].iloc[-1]

    st.metric("Net Earnings",f'{net_earning:,.2f}', f'{latest_month_roc:.2f}%')


#  ------------------------- Ploting the Bar graphs for the Category 0 & sales / waste Analysis -------------------------

col1, col2  = st.columns(2)


with col1:
    cat1_df = filtered_df.groupby(by = ["Category level 0"], as_index = False)["# of sold SKU items"].sum()
    st.subheader("Category wise # units Sold")
    fig = px.bar(cat1_df, x = "Category level 0", y = "# of sold SKU items", text = ['{:,}'.format(x) for x in cat1_df["# of sold SKU items"]],
                 template = "seaborn")

    fig.update_layout(xaxis_title="Category level 1",yaxis_title="Total number of Units Sold")

    st.plotly_chart(fig,use_container_width=True, height = 200)

with col2:
    cat1_df = filtered_df.groupby(by = ["Category level 0"], as_index = False)["Item COGS (net VAT) (EUR)"].sum()
    st.subheader("Category wise Earning")
    fig = px.bar(cat1_df, x = "Category level 0", y = "Item COGS (net VAT) (EUR)", text = ['{:,}'.format(x) for x in cat1_df["Item COGS (net VAT) (EUR)"]],
                 template = "seaborn")

    fig.update_layout(xaxis_title="Category level 1",yaxis_title="Net Earning")

    st.plotly_chart(fig,use_container_width=True, height = 200)

# -------------------------------------- TreeMap for Sold SKU Listings --------------------------------------

# Create a treemap based on Category level 0,Category level 1,Category level 2
st.subheader("Hierarchical view of SKUs Sold using TreeMap")
fig3 = px.treemap(filtered_df, path = ["Category level 0","Category level 1","Category level 2"], values = "# of sold SKU items",hover_data = ["# of sold SKU items"],
                  color = ("Category level 2"))
fig3.update_layout(width = 800, height = 650)
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------------- TreeMap for Sold SKU Listings wasted --------------------------------------

# Create a treemap based on Category level 0,Category level 1,Category level 2
st.subheader("Hierarchical view of SKUs with highest Waste using TreeMap")
fig3 = px.treemap(filtered_df, path = ["Category level 0","Category level 1","Category level 2"], values = "Waste, # of items",hover_data = ["Waste, # of items"],
                  color = ("Category level 2"))
fig3.update_layout(width = 800, height = 650)
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------------- Scatter Plot to understand the Discound effect on categories --------------------------------------

# Create a scatter plot
data1 = px.scatter(filtered_df,
                   x = "Discount Value (EUR)",
                   y = "Price before Discount (includ. VAT) (EUR)",
                   size = "Item COGS (net VAT) (EUR)",
                   hover_data=["Category level 0","Category level 1","Category level 2"])
data1['layout'].update(title="Relationship between Discounts and Sales using Scatter Plot.",
                       titlefont = dict(size=20),xaxis = dict(title="Discounts",titlefont=dict(size=19)),
                       yaxis = dict(title = "Net Price", titlefont = dict(size=19)))
st.plotly_chart(data1,use_container_width=True)

# ----------------------------------------------- END OF CODE -----------------------------------------------
