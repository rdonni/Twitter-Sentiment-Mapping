from typing import Dict
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

def sentiment_analysis(tweets_by_countries: Dict[str, str]) -> Dict[str, float]:
    
    """
    Take as input a dictionnary dict[country: str, tweets: list[str]] 
    Return sentiment scores of each country in a dict[country: str, score: float]
    """
    
    # Get the maximum number of tweets among all countries
    nb_tweets = [len(tweets_by_countries[country]) for country in tweets_by_countries.keys()]
    max_nb_tweets = max(nb_tweets)
    
    sentiment_score_by_countries = {}
    for country in tweets_by_countries.keys() : 
        # If a country has too few tweets, its score is considered too little negative.
        # We then arbitrarily set its score to None
        if len(tweets_by_countries[country]) < 0.3*max_nb_tweets:
            sentiment_score_by_countries[country] = None
        else : 
            scores_country = []
            for tweet_processed in tqdm(tweets_by_countries[country]) : 
                try :
                    print(country)
                    tweet_tokens = tokenizer(tweet_processed, return_tensors = 'pt')
                    output = model(tweet_tokens['input_ids'], tweet_tokens['attention_mask'])
                    score = softmax(output[0][0].detach().numpy())
                    scores_country.append(score)
                except :
                    print(country)
                    print('failed')
                    pass
            print(country)
            print(scores_country)
            sentiment_score_by_countries[country] = scores_country
    # UK is not quoted in the shape file for vizualisation but United Kingdom is
    sentiment_score_by_countries['United Kingdom'] = sentiment_score_by_countries.pop('UK')
        
    print ("----------------------- sentimental analysis realised -----------------------")
    return sentiment_score_by_countries

 
    