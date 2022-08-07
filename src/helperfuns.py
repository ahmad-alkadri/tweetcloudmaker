# Importing libraries and packages
import snscrape.modules.twitter as sntwitter
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import emoji
import streamlit as st


def emojidetect(text):
    stat = any(
        [c in emoji.UNICODE_EMOJI['en'] for c in text]
    )
    return stat


@st.experimental_memo
def gettweetdates(username, startdate, enddate):
    # Creating list to append tweet data
    tweets_list = []
    i = 0
    uname = f'from:{username}'
    sincedate = f'since:{startdate}'
    untildate = f'until:{enddate}'
    scrapestr = ' '.join([
        uname, sincedate, untildate
    ])
    # Using TwitterSearchScraper to scrape data
    # and append tweets to list
    for j, twt in enumerate(
            sntwitter.TwitterSearchScraper(
            scrapestr
            ).get_items()):
        i += 1
        if i > 2000:
            break
        tweets_list.append([
            twt.date,
            twt.id,
            twt.content,
            twt.user.username
        ])

    # Creating a dataframe from the tweets list above
    tweets_df = pd.DataFrame(
        tweets_list,
        columns=[
            'Datetime',
            'Tweet Id',
            'Text',
            'Username'
        ]
    )
    # Return the data
    return tweets_df


@st.experimental_memo
def gettweetamount(username, amount=500):
    # Creating list to append tweet data
    tweets_list = []
    i = 0
    scrapestr = f'from:{username}'
    # Using TwitterSearchScraper to scrape data
    # and append tweets to list
    for j, twt in enumerate(
            sntwitter.TwitterSearchScraper(
            scrapestr
            ).get_items()):
        i += 1
        if i > amount:
            break
        tweets_list.append([
            twt.date,
            twt.id,
            twt.content,
            twt.user.username
        ])

    # Creating a dataframe from the tweets list above
    tweets_df = pd.DataFrame(
        tweets_list,
        columns=[
            'Datetime',
            'Tweet Id',
            'Text',
            'Username'
        ]
    )
    # Return the data
    return tweets_df


@st.experimental_memo
def cleanlststr(texts):
    cleantexts = []
    for words in texts:
        if emojidetect(words) or not(words.isalnum()):
            continue
        else:
            cleantexts.append(words)
    return cleantexts

@st.experimental_singleton
def getwordcloud(path2font, width, height,
                 words, mask, backgroundcolor='#1DA1F2'):
    wordclo = WordCloud(
        repeat=False,
        font_path=path2font,
        width=width,
        height=height,
        color_func=(lambda *args, **kwargs: "white"),
        background_color=backgroundcolor,
        stopwords=STOPWORDS,
        min_word_length=2,
        mask=mask).generate(words)
    return wordclo
