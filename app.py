import streamlit as st
import pandas as pd

from web_scraper import perform_scraping

@st.cache_data(ttl="1hr", max_entries=20)
def _convert_df(df):
    return df.to_csv(sep=",", index=False).encode('utf-8')

@st.cache_data(ttl=60)
def start_scraping(hyperlink_df):

    # Get the list of URLs
    hyperlink_df = pd.read_csv(food_list)
    links_list = hyperlink_df['Hyperlink'].values.tolist()

    product_list = perform_scraping(links_list)

    column_names = list(product_list[0].keys())

    product_df = pd.DataFrame(product_list, columns=column_names)
    
    return product_df

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

# Check if uploaded and then start scraping
if food_list:

    new_products_df = start_scraping(food_list)

    # Attach to download button
    st.download_button(
        label="Download the extracted file.",
        data = _convert_df(new_products_df),
        file_name = 'new_food_items.csv',
        mime = 'text/csv'
    )

    # Show the output
    st.write(new_products_df)
    st.ballons()