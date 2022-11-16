# Imports 
import pytz 
import datetime
from tqdm import tqdm


# Get the Date
from datetime import date
today = date.today()
today = pytz.UTC.localize(datetime.datetime(today.year, today.month, today.day, 0, 0, 0))


#Tweet preprocessing : to be able to use the model each link is replaced by the expression "http" and each mention is replaced by @user
def preprocessing(tweets_by_countries) : 

    for country in tqdm(tweets_by_countries.keys()) : 
        
        tweets_country = []
        print(country)
        for i in range (len (tweets_by_countries[country])) : 
            
            tweet_words = []
            tweet = tweets_by_countries [country][i][3]
            tweet = tweet.replace("\n", " ")
            
            for word in tweet.split(' ') :
                
                if word.startswith('@') and len(word) > 1:
                    word = "@user"
                elif word.startswith('http') :
                    word = "http"
                else : 
                    pass
                tweet_words.append(word)
                
            tweets_country.append(" ".join(tweet_words))
            
        tweets_by_countries[country] = tweets_country 
        
    print ("----------------------- tweet preprocessed -----------------------")
    return tweets_by_countries