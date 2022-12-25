from typing import Dict

from scipy.special import softmax
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def sentiment_analysis(tweets_by_countries: Dict[str, str]) -> Dict[str, float]:
    """
    Take as input a dictionnary dict[country: str, tweets: list[str]] 
    Return sentiment scores of each country in a dict[country: str, score: float]
    """

    # Load the model and tokenizer
    roberta = "cardiffnlp/twitter-roberta-base-sentiment"  # finiteautomata/bertweet-base-sentiment-analysis
    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)

    print("----------------------- Computing sentiment analysis... -----------------------")
    sentiment_score_by_countries = {}
    for country in tweets_by_countries.keys():
        scores_country = []
        for tweet_processed in tqdm(tweets_by_countries[country]):
            try:
                tweet_tokens = tokenizer(tweet_processed, return_tensors='pt')
                output = model(tweet_tokens['input_ids'], tweet_tokens['attention_mask'])
                score = softmax(output[0][0].detach().numpy())
                scores_country.append(score)
            except:
                pass
        sentiment_score_by_countries[country] = scores_country
    # UK is not quoted in the shape file for visualisation but United Kingdom is
    sentiment_score_by_countries['United Kingdom'] = sentiment_score_by_countries.pop('UK')
    sentiment_score_by_countries['Bosnia and Herzegovina'] = sentiment_score_by_countries.pop('Bosnia')
    sentiment_score_by_countries['Republic of Serbia'] = sentiment_score_by_countries.pop('Serbia')
    sentiment_score_by_countries['North Macedonia'] = sentiment_score_by_countries.pop('Macedonia')

    print("----------------------- Sentimental analysis computed -----------------------")
    return sentiment_score_by_countries
