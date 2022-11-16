# Imports
from textblob import TextBlob
import tweepy
from time import sleep
from langdetect import detect
import langdetect
import pickle 
from tools import LANGUAGES, GEOCODES
import configparser
from tqdm import tqdm

# read config and authentification
config = configparser.ConfigParser()
config.read('/Users/rayanedonni/Documents/Projets_persos/News_by_ai/config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Collect tweets
def collect_tweets(api, geocodes, keyword = '*', nb_tweets_per_country = 5, clear = False) : 
    
    counter = 0
    
    # Handle the tweet collected previously
    # If clear = True, it clears the file tweets_by_countries.py. The variable tweets_by_countries is set to {}
    # If clear = False, it loads the previously collected tweets in the variable tweets_by_countries
    if clear == True : 
        tweets_by_countries = {}
        a_file = open("/Users/rayanedonni/Documents/Projets_persos/News_by_ai/sentiment_analysis/tweets_by_countries.pkl", "wb") #We open the file containing the tweets
        a_file.truncate(0) #Clear the file
        pickle.dump(tweets_by_countries, a_file)
        a_file.close()
    else : 
        try : # Try to load the tweet dictionnary if it already exists
            with open("/Users/rayanedonni/Documents/Projets_persos/News_by_ai/sentiment_analysis/tweets_by_countries.pkl", "rb") as handle :
                data = handle.read()
            tweets_by_countries = pickle.loads(data)
        except : # If it doesn't exist, create an empty dictionnary and save it into a specific directory
            tweets_by_countries = {}
            a_file = open("/Users/rayanedonni/Documents/Projets_persos/News_by_ai/sentiment_analysis/tweets_by_countries.pkl", "wb")
            pickle.dump(tweets_by_countries, a_file)
            a_file.close()
    
    
    # Collect new tweets
    for country in tqdm(geocodes.keys()): 
        
        data_country = []
        blob = TextBlob(country)
        print (country)
        
        # Translate the keyword that (given in english) into each country's language
        if keyword in '*' : 
            new_keyword = keyword
        else : 
            if country not in ["UK", "Ireland", "Switzerland", "Belarus", "Luxembourg"]:
                try : 
                    keyword_translated = TextBlob(keyword).translate(from_lang = 'en', to = LANGUAGES[country])
                    new_keyword = str(keyword_translated)
                except :
                    new_keyword = keyword
            
            elif country == "UK" or country == "Ireland" :
                new_keyword = keyword
            
            elif 'Switzerland' in country : 
                keyword_french = str(TextBlob(keyword).translate(from_lang = 'en', to = 'fr'))
                keyword_deutch = str(TextBlob(keyword).translate(from_lang = 'en', to = 'de'))
                keyword_italian = str(TextBlob(keyword).translate(from_lang = 'en', to = 'it'))
                new_keyword = f'{keyword} OR {keyword_french} OR {keyword_deutch} OR {keyword_italian}'
            
            elif 'Belarus' in country:
                try : 
                    keyword_belarusian = str(TextBlob(keyword).translate(from_lang = 'en', to = 'be'))
                    keyword_russian = str(TextBlob(keyword).translate(from_lang = 'en', to = 'ru'))
                    new_keyword = f'{keyword_belarusian} OR {keyword_russian}'
                except : 
                    keyword_russian = str(TextBlob(keyword).translate(from_lang = 'en', to = 'ru'))
                    new_keyword = f'{keyword_russian}'
                
            elif 'Luxembourg' in country: 
                try : 
                    keyword_deutch = str(TextBlob(keyword).translate(from_lang = 'en', to = 'de'))
                    keyword_french = str(TextBlob(keyword).translate(from_lang = 'en', to = 'fr'))
                    new_keyword = f'{keyword} OR {keyword_deutch} OR {keyword_french}'
                except :
                    new_keyword = keyword
                    
        
        print(new_keyword)
        tweets = tweepy.Cursor(api.search_tweets, q = new_keyword , geocode = geocodes[country], tweet_mode = "extended", count = 100).items(nb_tweets_per_country)

        # Collect tweets
        if country not in ["UK", "Ireland", "Switzerland", "Belarus", "Luxembourg"]:
            for tweet in tweets : 
                try : 
                    counter += 1 
                    print (counter)
                    tweet_text = tweet.full_text
                    tweet_translated = TextBlob(tweet_text).translate(from_lang = LANGUAGES[country], to = 'en') 
                    data_country.append([country, tweet.created_at, tweet.user.screen_name, str(tweet_translated)])
                    #sleep(0.5)
                    
                except :
                    continue
                
        elif country == "UK" or country == "Ireland": 
            for tweet in tweets :  
                counter += 1 
                print (counter)
                tweet_text = tweet.full_text
                data_country.append([country, tweet.created_at, tweet.user.screen_name, tweet_text])
                #sleep(0.5)
        
        # We handle the cas of Switzerland, Luxemburg and Belarus which have multiple official langugages
        elif 'Switzerland' in country : 
            
            for tweet in tweets : 
                tweet_text = tweet.full_text
                blob = TextBlob(tweet_text)
                try : 
                    if detect(tweet_text) == 'de':
                        try : 
                            counter += 1 
                            print (counter)
                            tweet_translated = blob.translate(from_lang = 'de', to = 'en') 
                            data_country.append([country, tweet.created_at, tweet.user.screen_name, str(tweet_translated)])
                            #sleep(0.5)
                        except :
                            continue
                        
                    elif detect(tweet_text) == 'fr':   
                        try : 
                            counter += 1 
                            print (counter)
                            tweet_translated = blob.translate(from_lang = 'fr', to = 'en') 
                            data_country.append([country, tweet.created_at, tweet.user.screen_name, str(tweet_translated)])
                            #sleep(0.5)
                        except :
                            continue
                    
                    elif detect(tweet_text) == 'it':   
                        try : 
                            counter += 1 
                            print (counter)
                            tweet_translated = blob.translate(from_lang = 'it', to = 'en') 
                            data_country.append([country, tweet.created_at, tweet.user.screen_name, str(tweet_translated)])
                            #sleep(0.5)
                        except :
                            continue
                        
                    elif detect(tweet_text) == 'en': 
                        counter += 1 
                        print (counter)
                        tweet_text = tweet.full_text
                        data_country.append([country, tweet.created_at, tweet.user.screen_name, tweet_text])
                        #sleep(0.5)
                        
                    else : 
                        continue
                except langdetect.lang_detect_exception.LangDetectException :
                    continue
                    
                          
        elif 'Belarus' in country : 
            for tweet in tweets : 
                tweet_text = tweet.full_text
                blob = TextBlob(tweet_text)
                try : 
                    if detect(tweet_text) == 'ru':
                        try : 
                            counter += 1 
                            print (counter)
                            tweet_translated = blob.translate(from_lang = 'ru', to = 'en') 
                            data_country.append([country, tweet.created_at, tweet.user.screen_name, str(tweet_translated)])
                            #sleep(0.5)
                        except :
                            continue
                        
                    else:   
                        try : 
                            counter += 1 
                            print (counter)
                            tweet_translated = blob.translate(from_lang = 'be', to = 'en') 
                            data_country.append([country, tweet.created_at, tweet.user.screen_name, str(tweet_translated)])
                            #sleep(0.5)
                        except :
                            continue
                except langdetect.lang_detect_exception.LangDetectException: 
                    continue
                  
        elif 'Luxembourg' in country: 
            for tweet in tweets : 
                tweet_text = tweet.full_text
                blob = TextBlob(tweet_text)
                try : 
                    if detect(tweet_text) == 'de':
                        try : 
                            counter += 1 
                            print (counter)
                            tweet_translated = blob.translate(from_lang = 'de', to = 'en') 
                            data_country.append([country, tweet.created_at, tweet.user.screen_name, str(tweet_translated)])
                            #sleep(0.5)
                        except :
                            continue
                        
                    elif detect(tweet_text) == 'fr':   
                        try : 
                            counter += 1 
                            print (counter)
                            tweet_translated = blob.translate(from_lang = 'fr', to = 'en') 
                            data_country.append([country, tweet.created_at, tweet.user.screen_name, str(tweet_translated)])
                            #sleep(0.5)
                        except :
                            continue
                        
                    elif detect(tweet_text) == 'en': 
                        counter += 1 
                        print (counter)
                        tweet_text = tweet.full_text
                        data_country.append([country, tweet.created_at, tweet.user.screen_name, tweet_text])
                        #sleep(0.5)
                    
                    else:   
                        try : 
                            counter += 1 
                            print (counter)
                            tweet_translated = blob.translate(from_lang = 'lb', to = 'en') 
                            data_country.append([country, tweet.created_at, tweet.user.screen_name, str(tweet_translated)])
                            #sleep(0.5)
                        except :
                            continue
                except langdetect.lang_detect_exception.LangDetectException: 
                    continue
        
        
        # Update the tweets_by_countries dictionnary
        if tweets_by_countries.get(country) : # Check if the value of the key country is not empty
            old_tweets = tweets_by_countries[country]
            updated_tweets = old_tweets + data_country
            tweets_by_countries[country] = updated_tweets
            
        else : 
            tweets_by_countries[country] = data_country               
               
        # Save the updated dictionnary in its specific path
        a_file = open("/Users/rayanedonni/Documents/Projets_persos/News_by_ai/sentiment_analysis/tweets_by_countries.pkl", "wb")
        pickle.dump(tweets_by_countries, a_file)
        a_file.close()

                                        
    print ("----------------------- tweet collected -----------------------")
    return tweets_by_countries


collect_tweets(api, GEOCODES, keyword = '*', nb_tweets_per_country = 5, clear = True)