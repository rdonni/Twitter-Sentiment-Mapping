import json
import pickle
from typing import Dict, List, Union, Any

import tweepy
from langdetect import detect
from textblob import TextBlob
from tqdm import tqdm

from twitter_sentiment_mapping.tools.tools import LANGUAGES


def collect_tweets(api,
                   geocodes: Dict[str, str],
                   tweet_file_path: str,
                   keyword: str,
                   traduce_keyword: bool,
                   nb_tweets_per_country: int,
                   clear: bool,
                   ):
    """
    Return and save a dictionary containing tweets by country

    The clear parameter handle the tweet collected previously:
    - if clear = True, it clears the file tweets_by_countries.py containing the tweets.
    The variable tweets_by_countries is set to {}
    - if clear = False, it loads the previously collected tweets in the variable tweets_by_countries
    """

    print('----------------------- Collecting tweets... -----------------------')

    # Load tweet files if necessary
    tweets_by_countries = load_tweet_files(clear, tweet_file_path)

    # Collect new tweets
    for country in (pbar := tqdm(geocodes.keys())):
        pbar.set_description(f"Processing {country}")

        # Translate the keyword that (given in english) into each country's language
        new_keyword = generate_translated_keyword(keyword, country, traduce_keyword)

        tweets = tweepy.Cursor(api.search_tweets,
                               q=new_keyword,
                               geocode=geocodes[country],
                               tweet_mode="extended",
                               count=1000
                               ).items(nb_tweets_per_country)

        data_country = translate_and_save_tweets(tweets,
                                                 country)

        update_and_save_tweet_file(tweets_by_countries,
                                   country,
                                   data_country,
                                   tweet_file_path)

    print("----------------------- Tweets collected -----------------------")
    return tweets_by_countries


def translate_keyword_from_en_to_language(string: str, language: str) -> str:
    if language == 'en':
        return string
    else:
        return str(TextBlob(string).translate(from_lang='en', to=language))


def translate_tweet_from_language_to_en(tweet_text: str, language: str) -> str:
    if detect(tweet_text) == 'en':
        return tweet_text
    else:
        return str(TextBlob(tweet_text).translate(from_lang=language, to='en'))


def generate_translated_keyword(keyword: str, country: str, traduce_keyword: bool) -> str:
    if (not traduce_keyword) or (keyword == '*'):
        return keyword
    else:
        spoken_languages = LANGUAGES[country]

        if len(spoken_languages) == 1:
            return keyword
        else:
            new_keyword = ''
            for i in range(len(spoken_languages)):
                try:
                    new_keyword += translate_keyword_from_en_to_language(keyword, spoken_languages[i])
                except:
                    new_keyword += keyword
                if i != len(spoken_languages) - 1:
                    new_keyword += ' OR '
            return new_keyword


def translate_and_save_tweets(tweets, country: str) -> List[List[Union[str, Any]]]:
    data_country = []
    for tweet in tqdm(tweets):
        tweet_text = tweet.full_text
        for language in LANGUAGES[country]:
            try:
                tweet_text = translate_tweet_from_language_to_en(tweet_text, language)
                data_country.append((country, tweet.created_at, tweet.user.screen_name, str(tweet_text)))
                break
            except:
                pass

        # sleep(0.5)
    return data_country


def load_tweet_files(clear: bool, tweet_file_path: str):
    if clear:
        tweets_by_countries = {}
        with open(tweet_file_path, "w") as outfile:
            json.dump(tweets_by_countries, outfile)
    else:
        try:  # Try to load the tweet dictionary if it already exists
            with open(tweet_file_path, "rb") as openfile:
                tweets_by_countries = json.load(openfile)
        except:  # If it doesn't exist, create an empty dictionary and save it into a specific directory
            tweets_by_countries = {}
            with open(tweet_file_path, "w") as outfile:
                json.dump(tweets_by_countries, outfile)

    return tweets_by_countries


def update_and_save_tweet_file(tweets_by_countries,
                               country,
                               data_country,
                               tweet_file_path
                               ):
    # Update the tweets_by_countries dictionary
    # Check if the value of the key country is not empty
    if tweets_by_countries.get(country):
        tweets_by_countries[country] = tweets_by_countries[country] + data_country
    else:
        tweets_by_countries[country] = data_country

    # Save the updated dictionary in its specific path
    tweet_file = open(tweet_file_path, "wb")
    pickle.dump(tweets_by_countries, tweet_file)
    tweet_file.close()
