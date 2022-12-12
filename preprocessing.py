import datetime
from datetime import date

import pytz
from tqdm import tqdm

today = date.today()
today = pytz.UTC.localize(datetime.datetime(today.year, today.month, today.day, 0, 0, 0))


#Tweet preprocessing : to be able to use the model each link is replaced by the expression "http" and each mention is replaced by @user
def preprocessing(tweets_by_countries) : 
    for country in tqdm(tweets_by_countries.keys()) : 
        tweets_country = []
        print(country)
        for i in range(len(tweets_by_countries[country])) : 
            tweet = tweets_by_countries[country][i][3].replace("\n", " ")            
            tweet_words = [preprocess_word(word) for word in tweet.split(' ')]                
            tweets_country.append(" ".join(tweet_words))
            
        tweets_by_countries[country] = tweets_country 
        
    print ("----------------------- tweet preprocessed -----------------------")
    return tweets_by_countries



def preprocess_word(token: str):
    if token.startswith('@') and len(token) > 1:
        token = "@user"
    elif token.startswith('http') :
        token = "http"
        
    return token