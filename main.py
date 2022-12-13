import click

from api_management.api_access import get_api_access
from collect_tweets import collect_tweets
from tools.geocodes import geocode
from negativity_score import score
from preprocessing import preprocessing
from sentiments_analysis import sentiment_analysis
from tools.tools import COUNTRIES, GEOCODES
from vizualisation.vizualisation import generate_map
from update_status import default_tweet_text, upload_tweet


#@click.command()
#@click.option('--config-path', default='/Users/rayanedonni/Documents/Projets_persos/News_by_ai/config.ini', required=True)
#@click.option('--tweets-path', default='/Users/rayanedonni/Documents/Projets_persos/News_by_ai/sentiment_analysis/tweets_by_countries.pkl', required=True)
#@click.option('--keyword', default='*')
#@click.option('--compute-geocodes, default=True)
#@click.option('--nb-tweets-to-collect-by-country', default=3)
#@click.option('--clear', default=False)
#@click.option('--map-output-path', default='Vizualisation/sentiment_map.jpg')
#@click.option('--update-status', default=False)
def main(
    config_path: str='/Users/rayanedonni/Documents/Projets_persos/News_by_ai/config.ini',
    tweets_path: str="/Users/rayanedonni/Documents/Projets_persos/News_by_ai/sentiment_analysis/tweets_by_countries.pkl",
    keyword: str='*',
    compute_geocodes: bool= False,
    nb_tweets_to_collect_by_country: int=5,
    clear: bool=True,
    map_output_path: str='vizualisation/sentiment_map.png', 
    update_status: bool=False):
    
    api=get_api_access(config_path)
    
    if compute_geocodes == True:
        geocodes = geocode(COUNTRIES)
    else :
        geocodes = GEOCODES
    
    tweets_by_countries = collect_tweets(api, geocodes, tweets_path, keyword, nb_tweets_to_collect_by_country, clear)
    
    for country in tweets_by_countries.keys() :
        print(country, " :", len(tweets_by_countries[country]))

    tweets_by_countries = preprocessing(tweets_by_countries)    

    sentiment_scores_by_countries = sentiment_analysis(tweets_by_countries)

    negativity_score_by_countries = score(sentiment_scores_by_countries)
    for key,value in negativity_score_by_countries.items() :
        print (key, " :", value)

    generate_map(negativity_score_by_countries, map_output_path)

    if update_status == True:        
        upload_tweet(api, default_tweet_text(keyword), map_output_path)


if __name__ == "__main__":
    main()
