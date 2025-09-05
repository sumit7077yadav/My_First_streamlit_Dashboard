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

col1, col2 = st.columns(2)
with col1:
 st.subheader('Units Sold by Category')

if not filtered_df.empty:
   
    sales_by_category = filtered_df.groupby('Category')['Units Sold'].sum().reset_index()

   
    fig = px.bar(
        sales_by_category,
        x='Category',
        y='Units Sold',
        title='Total Units Sold by Category',
        labels={'Units Sold': 'Total Units Sold', 'Category': 'Product Category'},
        color='Category'
    )
    st.plotly_chart(fig, use_container_width=True)


    with col2:
     st.subheader('Units Sold by Category')


   
sales_by_category = filtered_df.groupby('Category')['Units Sold'].sum().reset_index()

   
fig = px.line(
        sales_by_category,
        x='Category',
        y='Units Sold',
        title='Total Units Sold by Category',
        labels={'Units Sold': 'Total Units Sold', 'Category': 'Product Category'},
        color='Category'
    )
# with col1:
#         st.write("### Bar Chart of Units Sold by Category")
#         categorical_cols = ['Category', 'Unit Sold']
#         if categorical_cols:
#             category_choice = st.selectbox("Select a Category for the Bar Chart", categorical_cols)
#             units_sold_by_category = df.groupby(category_choice)['Units Sold'].sum().reset_index()
#             fig_bar = px.bar(
#                 units_sold_by_category,
#                 x=category_choice,
#                 y='Units Sold',
#                 title=f"Total Units Sold by {category_choice}",
#                 color_discrete_sequence=px.colors.qualitative.Plotly
#             )
#             st.plotly_chart(fig_bar, use_container_width=True)

# with col2:
#         st.write("### Scatter Plot of Price vs. Units Sold")
#         categorical_cols = ['Region', 'Product ID']
#         if len(numerical_cols):
#             x_axis = st.selectbox("Select X-Axis", numerical_cols, index=0)
#             y_axis = st.selectbox("Select Y-Axis", numerical_cols, index=1)
#             fig_scatter = px.scatter(
#                 df,
#                 x=x_axis,
#                 y=y_axis,
#                 hover_data=df.columns,
#                 title=f"Relationship between {x_axis} and {y_axis}"
#             )
#             st.plotly_chart(fig_scatter, use_container_width=True)

            


    
st.plotly_chart(fig, use_container_width=True)
# else:
#     st.warning("No data to display. Please adjust your filters.")