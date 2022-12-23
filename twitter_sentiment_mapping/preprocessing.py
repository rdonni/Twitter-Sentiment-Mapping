from typing import Dict

from tqdm import tqdm


def preprocessing(tweets_by_countries: Dict[str, str]) -> Dict[str, str]:
    """
    Tweet preprocessing : 
    - each link is replaced by the expression "http" 
    - each mention is replaced by @user
    """
    print("----------------------- Preprocessing tweets... -----------------------")

    for country in (pbar := tqdm(tweets_by_countries.keys())):
        pbar.set_description(f"Processing {country}")
        tweets_country = []
        for i in range(len(tweets_by_countries[country])):
            tweet = tweets_by_countries[country][i][3].replace("\n", " ")
            tweet_words = [preprocess_word(word) for word in tweet.split(' ')]
            tweets_country.append(" ".join(tweet_words))

        tweets_by_countries[country] = tweets_country

    print("----------------------- Tweets preprocessed -----------------------")
    return tweets_by_countries


def preprocess_word(token: str) -> str:
    if token.startswith('@') and len(token) > 1:
        token = "@user"
    elif token.startswith('http'):
        token = "http"
    return token
