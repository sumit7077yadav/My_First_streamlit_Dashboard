import streamlit as st
import pandas as pd
import plotly.express as px


st.title('Sales Data Dashboard')


try:
    df = pd.read_csv('sales_data.csv')
except FileNotFoundError:
    st.error('Error: The file sales_data.csv was not found. Please make sure it is in the same directory.')
    st.stop()


df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')


st.sidebar.header('Filter Options')

all_categories = df['Category'].unique()
selected_categories = st.sidebar.multiselect(
    'Select Category:',
    options=all_categories,
    default=all_categories
)




all_regions = df['Region'].unique()
selected_regions = st.sidebar.multiselect(
    'Select Region:',
    options=all_regions,
    default=all_regions
)
all_store = df['Store ID'].unique()
selected_stores = st.sidebar.multiselect(
    'Select Store:',
    options=all_store,
    default=all_store
)




min_date = df['Date'].min().date()
max_date = df['Date'].max().date()
date_range = st.sidebar.date_input(
    "Select Date Range:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


if date_range and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = df[
        (df['Category'].isin(selected_categories)) &
        (df['Region'].isin(selected_regions)) &
        (df['Store ID'].isin(selected_stores)) &
        (df['Date'].dt.date >= start_date) &
        (df['Date'].dt.date <= end_date)
    ]
else:
    filtered_df = df[
        (df['Category'].isin(selected_categories)) &
        (df['Region'].isin(selected_regions)) &
        (df['Store ID'].isin(selected_stores))
    ]


if filtered_df.empty:
    st.warning("No data to display. Please adjust your filters.")
else:
  
    col1, col2,col3 = st.columns(3)
    
 
    with col1:
        st.subheader('Units Sold by Category')
       
        sales_by_category = filtered_df.groupby('Category')['Units Sold'].sum().reset_index()

        
        fig_bar = px.bar(
            sales_by_category,
            x='Category',
            y='Units Sold',
            title='Total Units Sold by Category',
            labels={'Units Sold': 'Total Units Sold', 'Category': 'Product Category'},
            color='Category'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    
    with col2:
        st.subheader('Units Sold Over Time')
       
        sales_by_date = filtered_df.groupby('Date')['Units Sold'].sum().reset_index()
        fig_line = px.line(
            sales_by_date,
            x='Date',
            y='Units Sold',
            title='Total Units Sold Over Time',
            labels={'Units Sold': 'Total Units Sold'},
        )
        st.plotly_chart(fig_line, use_container_width=True)

   

# with col3:
#     st.subheader('Units Sold Distribution by Region')


#     sales_distribution = filtered_df.groupby('Region')['Units Sold'].sum().reset_index()

#     fig = px.pie(
#         sales_distribution,
#         names='Region',
#         values='Units Sold',
#         title='Percentage of Units Sold by Region',
#     )
#     st.plotly_chart(fig, use_container_width=True)
# else:
#     st.warning("No data to display for the pie chart. Please adjust your filters.")