import click

from api_access import get_api_access
from collect_tweets import collect_tweets
from negativity_score import score
from preprocessing import preprocessing
from sentiments_analysis import sentiment_analysis
from tools import GEOCODES
from Vizualisation.vizualisation import generate_map


@click.command()
@click.option('--config-path', default='config.ini')
@click.option('--tweets-path', default='/Users/rayanedonni/Documents/Projets_persos/News_by_ai/sentiment_analysis/tweets_by_countries.pkl', required=True)
@click.option('--keyword', default='*')
@click.option('nb-tweets-to-collect-by-country', default=3)
@click.option('clear', default=False)
@click.option('--map-output-path', default='Vizualisation/sentiment_map.jpg')
@click.option()
def main(
    config_path='/Users/rayanedonni/Documents/Projets_persos/News_by_ai/config.ini',
    tweets_path="/Users/rayanedonni/Documents/Projets_persos/News_by_ai/sentiment_analysis/tweets_by_countries.pkl",
    keyword='*',
    nb_tweets_to_collect_by_country=10,
    clear=True,
    map_output_path='Vizualisation/sentiment_map.png'):
    
    api=get_api_access(config_path)
    tweets_by_countries = collect_tweets(api, GEOCODES, tweets_path, keyword, nb_tweets_to_collect_by_country, clear)
    
    for country in tweets_by_countries.keys() :
        print(country, " :", len(tweets_by_countries[country]))

    tweets_by_countries = preprocessing(tweets_by_countries)    

    sentiment_scores_by_countries = sentiment_analysis(tweets_by_countries)

    negativity_score_by_countries = score(sentiment_scores_by_countries)
    for key,value in negativity_score_by_countries.items() :
        print (key, " :", value)

    # Plot the results on a map
    generate_map(negativity_score_by_countries, map_output_path)


if __name__ == "__main__":
    main()
    
