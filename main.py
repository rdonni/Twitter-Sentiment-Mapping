# Imports
import pickle

import click

from negativity_score import score
from preprocessing import preprocessing
from sentiments_analysis import sentiment_analysis
from Vizualisation.vizualisation import generate_map


#@click.command()
#@click.option('--tweets-path', default='/Users/rayanedonni/Documents/Projets_persos/News_by_ai/sentiment_analysis/tweets_by_countries.pkl', required=True)
#@click.option('--map-output-path', default='Vizualisation/sentiment_map.jpg')
#@click.option()
def main(
    tweets_path= "/Users/rayanedonni/Documents/Projets_persos/News_by_ai/sentiment_analysis/tweets_by_countries.pkl",
    map_output_path='Vizualisation/sentiment_map.png'
):
    # Get tweets 
    with open(tweets_path, "rb") as handle :
        data = handle.read()
    tweets_by_countries = pickle.loads(data)

    for country in tweets_by_countries.keys() :
        print(country, " :", len(tweets_by_countries[country]))

    # Preprocess tweets
    tweets_by_countries = preprocessing(tweets_by_countries)    

    # Sentiment Analysis
    sentiment_scores_by_countries = sentiment_analysis(tweets_by_countries)

    # Negativity score
    negativity_score_by_countries = score(sentiment_scores_by_countries)
    for key,value in negativity_score_by_countries.items() :
        print (key, " :", value)

    # Plot the results on a map
    generate_map(negativity_score_by_countries, map_output_path)


if __name__ == "__main__":
    main()
    
