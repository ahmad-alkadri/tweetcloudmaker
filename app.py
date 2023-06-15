# Importing libraries and packages
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import streamlit as st
import src.helperfuns as hlp

# SECTION - INITIATION -----
# Configuring the initiation of the streamlit app

# Page title
st.set_page_config(page_title="Tweet Cloud Maker")

# Tweet scraper client
twtdig = hlp.TweetDigester()

# Hide the hamburger menu
st.markdown("""
			<style>
			#MainMenu {visibility: hidden;}
			footer {visibility: hidden;}
			</style>
			""",
            unsafe_allow_html=True)

# SECTION - DESCRIPTION PART -----
# This section is dedicated for displaying the short
# description of this web app and how to use it.
st.title("TweetCloud Maker")

with st.expander("Show description"):
    st.header("Description")
    st.write(
        """
        This webapp makes wordcloud based on the tweets of a 
        username, any username, as long as their profile is public 
        and they have tweets in their profile. Go to the sidebar, input the username and the number of 
        tweets that you want to search, and click Submit.""")
        
    st.write("""
        Automatically, every scraping queries will be saved as caches
        for five minutes. If you want to clear all the caches, simply
        click the button clear Cache on the sidebar.
        Below, you'll find the word cloud. The whole process could take 
        between 30—60 seconds and at maximum only 1000 tweets will be scraped
        """
    )

# SECTION - CONFIG PART -----
# Sidebar forms for the config menu
with st.sidebar.form("formquantity"):
    usernamereq = st.text_input(
        label="Input the twitter username",
        value="@jack")
    numtweets = st.number_input(
        label="Number of tweets to be scraped",
        value=100,
        step=1, min_value=1, max_value=1000)
    skipreplies = st.checkbox("Skip replies")
    subt = st.form_submit_button()

st.sidebar.button("clear Cache", on_click=twtdig.clear_cache)

# Scrape the tweets
if subt:
    with st.spinner("Scraping..."):
        try:
            twtdig.get_tweets_user(usernamereq, numtweets, skipreplies)
        except Exception:
            st.error("Error during tweet scraping")

    # SECTION - WORDCLOUD PART -----
    # This section takes the output from the tweet-scraping
    # operations and make the wordcloud from it, including
    # displaying it on the page.

    with st.spinner("Preparing the wordcloud..."):
        alltweetsclean = twtdig.get_cleaned_tweets()

        # Clean up
        wordsclean = ' '.join(alltweetsclean)
        # Capitalize everything
        wordsready = wordsclean.upper()

        # Prepare the mask
        mask = np.array(
            Image.open(
                os.path.join(
                    os.getcwd(), "assets", "twitterlogo.png"
                )
            )
        )
        # Replace the transparent value with white
        maskcorr = np.where(mask == 0, 255, mask)

        # Get the font file
        path2font = os.path.join(
            os.getcwd(), "assets", "cloudfont",
            "NotoSansKR-Medium.otf"
        )

        # Make the word cloud
        try:
            word_cloud = hlp.getwordcloud(
                path2font,
                width=1600,
                height=1600,
                words=wordsready,
                mask=maskcorr
            )
            statcloud = True
        except ValueError as err:
            print(err)
            st.warning("""
                **ERROR: username not found or tweets unsearchable.**
                Please make sure that:\n
                1. the twitter profile exists\n
                2. the twitter profile is public\n
                3. the user has tweeted at least once
            """)
            statcloud = False

        if statcloud:
            st.header("TweetCloud")
            st.markdown("""
                Right-click the image below and select "Save Image As" 
                to get the image.
            """)
            # Make the image
            font_prop = FontProperties(fname=path2font)
            fig, ax = plt.subplots()
            ax.imshow(word_cloud)
            # Text username
            ax.text(
                0.5, 0.925,
                f'{usernamereq}',
                horizontalalignment='center',
                fontsize=7.5,
                font_properties=font_prop,
                color='white',
                transform=ax.transAxes)
            # Text credit
            ax.text(
                0.5, 0.05,
                'tweetcloudmaker.streamlit.app',
                horizontalalignment='center',
                fontsize=5,
                font_properties=font_prop,
                color='white',
                transform=ax.transAxes)
            ax.axis('off')
            ax.set_facecolor('#1DA1F2')
            st.pyplot(fig, pad_inches=0)

st.markdown("---")
st.header("Contact")
st.info("""
	This app is maintained by Ahmad Alkadri. 
	You can learn more about me at my
	[blog](https://ahmad-alkadri.github.io) or 
	[github](https://github.com/ahmad-alkadri). 
    If you have any questions, feel free to raise 
    them as Issues.
""")
