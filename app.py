import streamlit as st

st.title('Welcome to NutriScraper.')
st.header("File upload section")

# Just in case
cache_clear_button = st.button(
    "Clear cache data",
    type = "primary",
    help = "Clear all in-memory data. Refresh the page after clicking this button"
)

if cache_clear_button:
    st.cache_data.clear()

food_list = st.file_uploader(
    "Upload the URL link file",
    type="csv"
)

# Check if uploaded
if food_list:
    print("Let's get started!")