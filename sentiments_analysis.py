# Imports
import numpy as np
from scipy.special import softmax
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Load the model and tokenizer 
roberta = "cardiffnlp/twitter-roberta-base-sentiment"  #finiteautomata/bertweet-base-sentiment-analysis
model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

labels = ['Negative', 'Neutral', 'Positive']

# Sentiment Analysis with Roberta

def sentiment_analysis (tweets_by_countries):
    
    # Get the maximum number of tweets among all countries
    nb_tweets = []
    for country in tweets_by_countries.keys():
        nb_tweets.append(len(tweets_by_countries[country]))
    max_nb_tweets = max(nb_tweets)
    
    sentiment_score_by_countries = {}
    
    for country in tweets_by_countries.keys() : 
        
        if len(tweets_by_countries[country]) < 0.3*max_nb_tweets:

            sentiment_score_by_countries[country] = np.nan
        
        else : 
            scores_country = []

            for tweet_processed in tqdm(tweets_by_countries[country]) : 
                try :
                    encoded_tweet = tokenizer(tweet_processed, return_tensors = 'pt')
                    output = model(encoded_tweet['input_ids'], encoded_tweet['attention_mask'])

                    score = softmax(output[0][0].detach().numpy())

                    scores_country.append (score)
                except :
                    pass
            if country == 'UK' :
                sentiment_score_by_countries['United Kingdom'] = scores_country # UK is not quoted in the shape file for vizualisation but United Kingdom is

            else :
                sentiment_score_by_countries[country] = scores_country
        

    print ("----------------------- sentimental analysis realised -----------------------")
    return sentiment_score_by_countries

 
    