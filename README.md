# Twitter-Sentiment-Mapping

**This project enables the creation of opinion/sentiment maps of European countries (possibly on a specific topic) from a sentiment analysis of tweets.**

This project is composed of several steps:
- First, tweets are retrieved via the twitter API in each of the European countries. We can filter the tweets containing only a certain word to focus on a particular theme. All these tweets are also translated into English thanks to the TextBlob library which is based on the Google Translate API. 
- We then perform a sentiment analysis on these tweets thanks to the hugging face model which is based on bert and which is finetuned on tweets in English.
- From the sentiment of each tweet (positive, negative or neutral) deduced from the sentiment analysis. We compute a score for each country as follows: $Country Sentiment Score = (Number Of Positive Tweets - Number Of Negative Tweets)/Total Number Of Tweets$
- We represent the map of Europe colored according to this score with the geopandas library.
- At the end of this process it is possible to post a tweet containing the map and a personalized text on the tweets account attached to the API keys provided

## Results

Here are some examples of cards that can be obtained with this code.

Here is a map obtained on December 20, 2022, just after the World Cup in Qatar by **filtering tweets containing the word Qatar**. This map was built by collecting 1000 tweets for each country.

<img width="994" alt="Capture d’écran 2022-12-22 à 14 55 50" src="https://user-images.githubusercontent.com/106410831/209149418-0d070d16-716c-4bcd-b786-c4c2541e04d1.png">

## Instalation
First of all, you have to configure the virtual environment:
```python
python3 -m venv /path/to/new/virtual/environment
pip install -r requirements.txt
```
Then you have to fill in the Twitter api keys in the config.ini file:
```python
api_key = XXX
api_key_secret = XXX
access_token = XXX
access_token_secret = XXX
```
These tokens and keys are available on Twiter Developer Platform (https://developer.twitter.com/en).

## Run
To collect tweets on a specific theme, translate them and create a map: 
```python
python main.py --config-path your/config/path --tweets-path your/path/to/save/tweets --keyword your_own_keyword --nb-tweets-to-collect-by-country 50 
```
To collect tweets on a specific theme, translate them, create a map and post a tweet containing the map :
```python
python main.py --config-path your/config/path --tweets-path your/path/to/save/tweets --keyword your_own_keyword --nb-tweets-to-collect-by-country 50 --update-status True
```
To just collect tweets and translate them :
```python
python main.py --config-path your/config/path --tweets-path your/path/to/save/tweets --keyword your_own_keyword --nb-tweets-to-collect-by-country 50 --collect-only True
```
