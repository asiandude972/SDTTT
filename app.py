import streamlit as st
import pandas as pd
import plotly.express as px

# Web app title
st.title('Vehicle Dashboard')

# Load dataset and clean data
df = pd.read_csv('vehicles_us (1).csv')
df_cleaned = df.dropna(subset=['price', 'odometer', 'type'])

# Slider for selecting price range
min_price, max_price = int(df_cleaned['price'].min()), int(df_cleaned['price'].max())
price_range = st.slider('Select Price Range', min_value=min_price, max_value=max_price, value=(min_price, max_price), key='price_range')

# Selector for choosing vehicle type
vehicle_types = df_cleaned['type'].unique().tolist()
vehicle_type_selection = st.selectbox('Select Vehicle Type', vehicle_types, key='vehicle_type_selection')

# Combine filters for the DataFrame
df_filtered = df_cleaned[(df_cleaned['price'] >= price_range[0]) & (df_cleaned['price'] <= price_range[1])]
df_filtered = df_filtered[df_filtered['type'] == vehicle_type_selection]

# Display header
st.header('Vehicle Price Distribution')

# Histogram for prices using the filtered dataframe
fig_price = px.histogram(df_filtered, x='price', title='Histogram of Vehicle Prices')

# Checkbox to show/hide the histogram
if st.checkbox('Show Price Histogram'):
    st.plotly_chart(fig_price)

st.header('Price vs Odometer Readings')

# Scatter plot of price vs odometer using the filtered DataFrame
fig_scatter = px.scatter(df_filtered, x='odometer', y='price', title='Scatter Plot of Price vs Odometer Readings')

# Columns for layout
col1, col2 = st.columns(2)

with col1:
    # Put the histogram in column 1
    st.plotly_chart(fig_price)

with col2:
    # Put the scatter plot in column 2
    st.plotly_chart(fig_scatter)

# Selectbox for individual vehicle selection
selected_vehicle = st.selectbox('Select a Vehicle', df_filtered.index)
vehicle_info = df_filtered.loc[selected_vehicle]
st.write(vehicle_info)

# Form for additional user input (optional)
with st.form("my_form"):
    st.write("Inside the form")
    slider_val = st.slider("Form slider", key='form_slider')
    checkbox_val = st.checkbox("Form checkbox", key='form_checkbox')

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)
