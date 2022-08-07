# Importing libraries and packages
import os
from PIL import Image
import numpy as np
import requests
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import streamlit as st
import src.helperfuns as hlp
from datetime import datetime
from dateutil.relativedelta import relativedelta

# SECTION - INITIATION -----
# Configuring the initiation of the streamlit app

# Page title
st.set_page_config(page_title="Tweet Cloud Maker")

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
st.header("Description")
st.markdown(
    """
	This webapp makes wordcloud based on the tweets of a 
	username, any username, as long as their profile is public 
	and they have tweets in their profile. 
	
	Go to the sidebar on the left and select the 
	scraping mode that you want, input the username and the number of 
	tweets that you want to search *or* the date interval, and 
	click Submit. Below, you'll find the word cloud. **Warnings**:
	
	+ the whole process could take between 30—60 seconds
	+ at maximum only 2000 tweets will be scraped
	"""
)

# SECTION - CONFIG PART -----
# This section is dedicated to parts used for configuring
# the twitter scrape, starting from selecting the mode
# of search (either through scraping based on the number
# of last tweets or selecting tweets within a certain
# interval date)

modescrape = st.sidebar.selectbox(
    "Select scraping mode:",
    ["Date interval", "Number of last tweets"],
    index=1)

# Prepare the interval date
nowdate = datetime.now()
ayearago = nowdate - relativedelta(years=1)

# Sidebar forms for the config menu
if modescrape == "Number of last tweets":
    with st.sidebar.form("formquantity"):
        usernamereq = st.text_input(
            label="Input the twitter username",
            value="@jack")
        numtweets = st.number_input(
            label="Number of tweets to be scraped",
            value=100,
            step=1, min_value=1, max_value=2000)
        subt = st.form_submit_button()
elif modescrape == "Date interval":
    with st.sidebar.form("formdate"):
        usernamereq = st.text_input(
            label="Input the twitter username",
            value="@jack")
        datestart = st.date_input("Start date:",
                                  value=ayearago,
                                  min_value=ayearago,
                                  max_value=nowdate)
        dateend = st.date_input("End date:",
                                value=nowdate,
                                min_value=ayearago,
                                max_value=nowdate)
        dateend_str = dateend.strftime("%Y-%m-%d")
        datestart_str = datestart.strftime("%Y-%m-%d")
        subt = st.form_submit_button()

# Button to clear caches
st.sidebar.info("""Click the button below to clear all cached tweets 
    that were scraped""")
clcbut = st.sidebar.button("Clear Cache")

if clcbut:
    st.experimental_memo.clear()
    st.experimental_singleton.clear()

# SECTION - SCRAPING PART -----
# This section is dedicated to the tweet-scraping operations.
# It takes the input by users made on the CONFIG section

# Scrape the tweets
if modescrape == "Number of last tweets" and subt:
    dft = hlp.gettweetamount(
        username=usernamereq.replace("@", ""),
        amount=numtweets
    )
elif modescrape == "Date interval" and subt:
    dft = hlp.gettweetdates(
        username=usernamereq.replace("@", ""),
        startdate=datestart_str,
        enddate=dateend_str
    )

# SECTION - WORDCLOUD PART -----
# This section takes the output from the tweet-scraping
# operations and make the wordcloud from it, including
# displaying it on the page.

if 'dft' in globals():
    tweets = dft['Text'].to_list()

    alltweets = " ".join(tweets)
    alltweets = alltweets.replace("\n", "")
    # Split to list of texts
    alltweets = alltweets.split(" ")
    # Clean up
    alltweetsclean = hlp.cleanlststr(alltweets)
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
            'tweetcloudmaker.herokuapp.com',
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
	[blog](https://ahmadalkadri.com) or 
	[github](https://github.com/ahmad-alkadri). 
    If you have any questions, feel free to raise 
    them as Issues.
""")