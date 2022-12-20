import click

from api_management.api_access import get_api_access
from collect_tweets import collect_tweets
from tools.geocodes import geocode
from negativity_score import score
from preprocessing import preprocessing
from sentiments_analysis import sentiment_analysis
from tools.tools import COUNTRIES, GEOCODES
from visualisation.vizualisation import generate_map
from update_status import default_tweet_text, upload_tweet


@click.command()
@click.option('--config-path', default='api_management/config.ini', required=True, help='Path to the config file '
                                                                                        'containing twitter api keys')
@click.option('--tweets-path', default='tweets_by_countries.pkl', required=True, help='Path to the pickle file '
                                                                                      'containing the tweets of each '
                                                                                      'country')
@click.option('--keyword', default='*', help='If the value is different from *, all tweets retrieved will contain '
                                             'keyword')
@click.option('--compute-geocodes', default=True)
@click.option('--nb-tweets-to-collect-by-country', default=3)
@click.option('--collect-only', default=False)
@click.option('--clear', default=False, help="If clear is True, the tweet_by_countries file is cleared before "
                                             "collecting new tweets")
@click.option('--map-output-path', default='visualisation/sentiment_map.png')
@click.option('--update-status', default=False, help='If update-status=True, a publication will be posted with a '
                                                     'default text and the map created ')
def main(
        config_path: str = 'api_management/config.ini',
        tweets_path: str = 'tweets_by_countries.pkl',
        keyword: str = '*',
        compute_geocodes: bool = False,
        nb_tweets_to_collect_by_country: int = 10,
        collect_only: bool = False,
        clear: bool = False,
        map_output_path: str = 'visualisation/sentiment_map.png',
        update_status: bool = True
) -> None:

    api = get_api_access(config_path)

    if compute_geocodes:
        geocodes = geocode(COUNTRIES)
    else:
        geocodes = GEOCODES

    tweets_by_countries = collect_tweets(api, geocodes, tweets_path, keyword, nb_tweets_to_collect_by_country, clear)

    for country in tweets_by_countries.keys():
        print(country, " :", len(tweets_by_countries[country]))

    if not collect_only:
        tweets_by_countries = preprocessing(tweets_by_countries)

        sentiment_scores_by_countries = sentiment_analysis(tweets_by_countries)

        negativity_score_by_countries = score(sentiment_scores_by_countries)
        for key, value in negativity_score_by_countries.items():
            print(key, " :", value)

        generate_map(negativity_score_by_countries, map_output_path)

        if update_status:
            upload_tweet(api, default_tweet_text(keyword), map_output_path)


if __name__ == "__main__":
    main()
