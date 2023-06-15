# Importing libraries and packages
from pytterrator import Client
from wordcloud import WordCloud, STOPWORDS
import streamlit as st
import re
from cachetools import TTLCache

# Initialize the cache object
scraping_cache = TTLCache(maxsize=1000, ttl=300)

class TweetDigester:
    def __init__(self):
        self.client = Client()
        self.arrtweets = [""]

    def wrapper_getprecisenumtweets(
        self, username, numtweet, exclude_replies: bool = False
    ):
        cache_key = (username, numtweet, exclude_replies)

        if cache_key in scraping_cache:
            return scraping_cache[cache_key]

        lis_texts_tweets = self.client.getprecisenumtweetstext(
            screen_name=username,
            count=numtweet,
            exclude_replies=exclude_replies,
            include_rts=False,
            limit_singlereq=20,
        )
        scraping_cache[cache_key] = lis_texts_tweets
        return lis_texts_tweets

    def get_tweets_user(self, username, numtweet, exclude_replies: bool = False):
        self.arrtweets = self.wrapper_getprecisenumtweets(
            username=username,
            numtweet=numtweet,
            exclude_replies=exclude_replies,
        )

    def get_cleaned_tweets(self):
        words = []

        # Pattern to match words with alphanumeric characters, Chinese, Japanese, and Korean characters
        pattern = re.compile(
            r"^[\w\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]+$"
        )

        # Split each text into words and process each word
        for text in self.arrtweets:
            for word in text.split(" "):
                if "http://" in word:  # remove word containing http://
                    continue
                if pattern.match(word):  # add word only if it matches the pattern
                    words.append(word)
        return words

    def clear_cache(self):
        """Clear the cache for wrapper_getprecisenumtweets."""
        scraping_cache.clear()


@st.cache_resource(show_spinner=False)
def getwordcloud(path2font, width, height, words, mask, backgroundcolor="#1DA1F2"):
    wordclo = WordCloud(
        repeat=False,
        font_path=path2font,
        width=width,
        height=height,
        color_func=(lambda *args, **kwargs: "white"),
        background_color=backgroundcolor,
        stopwords=STOPWORDS,
        min_word_length=2,
        mask=mask,
    ).generate(words)
    return wordclo
