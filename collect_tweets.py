# Imports
import pickle
from typing import Dict, List, Union, Any

import tweepy
from langdetect import detect
from textblob import TextBlob
from tqdm import tqdm

from tools.tools import LANGUAGES


# Collect tweets
def collect_tweets(api,
                   geocodes: Dict[str, str],
                   tweet_file_path: str,
                   keyword: str = '*',
                   nb_tweets_per_country: int = 5,
                   clear: bool = True,
                   ):
    """
    Return and save a dictionnary containing tweets by country 

    The clear parameter handle the tweet collected previously:
    - if clear = True, it clears the file tweets_by_countries.py containing the tweets.
    The variable tweets_by_countries is set to {}
    - if clear = False, it loads the previously collected tweets in the variable tweets_by_countries
    """

    # Load tweet files if necessary
    tweets_by_countries = load_tweet_files(clear, tweet_file_path)

    # Collect new tweets
    for country in (pbar := tqdm(geocodes.keys())):
        pbar.set_description(f"Processing {country}")

        # Translate the keyword that (given in english) into each country's language
        new_keyword = generate_translated_keyword(keyword, country)

        tweets = tweepy.Cursor(api.search_tweets,
                               q=new_keyword,
                               geocode=geocodes[country],
                               tweet_mode="extended",
                               count=100
                               ).items(nb_tweets_per_country)

        # Collect tweets
        data_country = translate_and_save_tweets(tweets,
                                                 country)

        update_and_save_tweet_file(tweets_by_countries,
                                   country,
                                   data_country,
                                   tweet_file_path)

    print("----------------------- tweet collected -----------------------")
    return tweets_by_countries


def translate_keyword_from_en_to_langage(string: str, langage: str) -> str:
    if langage == 'en':
        return string
    else:
        return str(TextBlob(string).translate(from_lang='en', to=langage))


def translate_tweet_from_langage_to_en(tweet_text: str,langage: str) -> str:
    if detect(tweet_text) == 'en':
        return tweet_text
    else:
        return str(TextBlob(tweet_text).translate(from_lang=langage, to='en'))


def generate_translated_keyword(keyword: str, country: str) -> str:
    if keyword == '*':
        return keyword
    else:
        spoken_langages = eval(LANGUAGES[country])

        if len(spoken_langages) == 1:
            return keyword
        else:
            new_keyword = ''
            for i in range(len(spoken_langages)):
                new_keyword += translate_keyword_from_en_to_langage(keyword, spoken_langages[i])
                if i != len(spoken_langages)-1:
                    new_keyword += ' OR '
            return new_keyword


def translate_and_save_tweets(tweets, country: str) -> List[List[Union[str, Any]]]:

    data_country = []
    for tweet in tqdm(tweets):
        tweet_text = tweet.full_text
        for langage in eval(LANGUAGES[country]):
            try:
                tweet_text = translate_tweet_from_langage_to_en(
                    tweet_text, langage)
                data_country.append([country, tweet.created_at, tweet.user.screen_name, str(tweet_text)])
                continue
            except:
                pass

        # sleep(0.5)
    return data_country


def load_tweet_files(clear: bool, tweet_file_path: str):
    if clear == True:
        tweets_by_countries = {}
        # We open the file containing the tweets
        tweet_file = open(tweet_file_path, "wb")
        tweet_file.truncate(0)  # Clear the file
        pickle.dump(tweets_by_countries, tweet_file)
        tweet_file.close()
    else:
        try:  # Try to load the tweet dictionnary if it already exists
            with open(tweet_file_path, "rb") as handle:
                data = handle.read()
            tweets_by_countries = pickle.loads(data)
        except:  # If it doesn't exist, create an empty dictionnary and save it into a specific directory
            tweets_by_countries = {}
            tweet_file = open(tweet_file_path, "wb")
            pickle.dump(tweets_by_countries, tweet_file)
            tweet_file.close()

    return tweets_by_countries


def update_and_save_tweet_file(tweets_by_countries,
                               country,
                               data_country,
                               tweet_file_path
                               ):

    # Update the tweets_by_countries dictionnary
    # Check if the value of the key country is not empty
    if tweets_by_countries.get(country):
        tweets_by_countries[country] = tweets_by_countries[country] + data_country
    else:
        tweets_by_countries[country] = data_country

    # Save the updated dictionnary in its specific path
    tweet_file = open(tweet_file_path, "wb")
    pickle.dump(tweets_by_countries, tweet_file)
    tweet_file.close()
