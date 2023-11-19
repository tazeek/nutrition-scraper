import streamlit as st
import pandas as pd

from web_scraper import NutriScraper

@st.cache_data(ttl="1hr", max_entries=20)
def _convert_df(df):
    return df.to_csv(sep=",", index=False).encode('utf-8')

@st.cache_data(ttl=60, show_spinner=False)
def start_scraping(hyperlink_df):

    # Get the list of URLs
    hyperlink_df = pd.read_csv(food_list)
    links_list = hyperlink_df['Hyperlink'].values.tolist()

    # Initialization
    my_bar = st.progress(0, text="Preparing to scrape..")
    total_links = len(links_list)

    nutri_scraper = NutriScraper()
    product_list = []

    for index, url in enumerate(links_list):

        percentage = int(((index + 1)/total_links) * 100)
        new_product = nutri_scraper.perform_scraping(url)
        product_list.append(new_product)

        my_bar.progress(
            percentage, 
            text=f"{index + 1}/{total_links} scraped"
        )

    column_names = list(product_list[0].keys())
    
    return pd.DataFrame(product_list, columns=column_names)

# Page configurations
st.set_page_config(
    page_title="NutriScraper - Get products scraped",
    page_icon="🛒",
    layout="wide"
)

st.title('Welcome to NutriScraper.')

st.header('Important Notes')
st.markdown(
"""
Current websites supported:
- Woolworths

Please read the following on how to run: https://github.com/tazeek/nutrition-scraper#how-it-works
"""
)


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

    new_products_df = None
    
    try:
        new_products_df = start_scraping(food_list)
    except Exception as e:
        st.error(
            "An error has occurred. \n \
            Please refresh and try again.",
            icon="🚨"
        )
        st.stop()

    # Attach to download button
    st.download_button(
        label="Download the extracted file.",
        data = _convert_df(new_products_df),
        file_name = 'new_food_items.csv',
        mime = 'text/csv'
    )

    # Show the output
    st.write(new_products_df)
    st.balloons()