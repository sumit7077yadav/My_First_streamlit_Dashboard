import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(layout="wide")
st.title(" Sales Data Dashboard")

# Load data function
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found.")
        return None

file_path = "C:/Users/EX0065/Downloads/streamlit/sales_data.csv"


df = load_data(file_path)

if df is not None:
    
    st.header("Data Overview")

    st.write("### Raw Data")
    st.dataframe(df.head(10))

    st.write("### Descriptive Statistics")
    st.dataframe(df.describe())

   
    st.header("Data Visualizations")

   

    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

  

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        st.write("### Bar Chart of Units Sold by Category")
        categorical_cols = ['Category', 'Unit Sold']
        if categorical_cols:
            category_choice = st.selectbox("Select a Category for the Bar Chart", categorical_cols)
            units_sold_by_category = df.groupby(category_choice)['Units Sold'].sum().reset_index()
            fig_bar = px.bar(
                units_sold_by_category,
                x=category_choice,
                y='Units Sold',
                title=f"Total Units Sold by {category_choice}",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.write("### Scatter Plot of Price vs. Units Sold")
        categorical_cols = ['Region', 'Product ID']
        if len(numerical_cols):
            x_axis = st.selectbox("Select X-Axis", numerical_cols, index=0)
            y_axis = st.selectbox("Select Y-Axis", numerical_cols, index=1)
            fig_scatter = px.scatter(
                df,
                x=x_axis,
                y=y_axis,
                hover_data=df.columns,
                title=f"Relationship between {x_axis} and {y_axis}"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

            

        with col3:
            st.write("### line Chart of Units Sold by Category")
            if categorical_cols:
                category_choice = st.selectbox("Select a Category for the  line  Chart", categorical_cols, index=0)
                units_sold_by_category = df.groupby(category_choice)['Units Sold'].sum().reset_index()
                fig_line = px.line(
                    units_sold_by_category,
                x=category_choice,
                y='Units Sold',
                title=f"Total Units Sold by {category_choice}",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            st.plotly_chart(fig_line, use_container_width=True)

    with col4:
        
         st.write("### Pie Chart of Units Sold by Category")
    categorical_cols = ['Category', 'Product ID',"Region"]
    
    if categorical_cols:
        category_choice = st.selectbox(
            "Select a Category for the Pie Chart",
            categorical_cols,
            key="pie_chart"
        )
        
        
        units_sold_by_category = df.groupby(category_choice)['Units Sold'].sum().reset_index()
        
        fig_pie = px.pie(
        
            units_sold_by_category,
            names=category_choice,
            values='Units Sold',
            title=f"Total Units Sold by {category_choice}",
            color_discrete_sequence=px.colors.qualitative.Plotly,
            height=400,  # You can adjust this value
            width=500
        )
        st.plotly_chart(fig_pie, use_container_width=True)

       



    

        
        
   
        
        
        





    # st.markdown("---")
    # st.header("Download Data")

    # csv = df.to_csv(index=False).encode('utf-8')
    # st.download_button(
    #     label="Download Data as CSV",
    #     data=csv,
    #     file_name="sales_data_download.csv",
    #     mime="text/csv",
    # )
