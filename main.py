import click

from twitter_sentiment_mapping.api_management.api_access import get_api_access
from twitter_sentiment_mapping.collect_tweets import collect_tweets
from twitter_sentiment_mapping.negativity_score import score
from twitter_sentiment_mapping.preprocessing import preprocessing
from twitter_sentiment_mapping.sentiments_analysis import sentiment_analysis
from twitter_sentiment_mapping.tools.geocodes import geocode
from twitter_sentiment_mapping.tools.tools import COUNTRIES, GEOCODES
from twitter_sentiment_mapping.update_status import default_tweet_text, upload_tweet
from twitter_sentiment_mapping.visualisation.visualisation import generate_map


@click.command()
@click.option('--config-path', default='twitter_sentiment_mapping/api_management/config.ini', required=True,
              help='Path to the config file '
                   'containing twitter api keys')
@click.option('--tweets-path', default='twitter_sentiment_mapping/tweets_by_countries.json', required=True,
              help='Path to the pickle file '
                   'containing the tweets of each '
                   'country')
@click.option('--keyword', default='*', help='If the value is different from *, all tweets retrieved will contain '
                                             'keyword')
@click.option('--compute-geocodes', default=False)
@click.option('--nb-tweets-to-collect-by-country', default=50)
@click.option('--traduce-keyword', default=True, type=bool,
              help="Some universal words/expressions like the name of a music "
                   "album doesn't need any translation")
@click.option('--collect-only', default=False)
@click.option('--clear', default=False, help="If clear is True, the tweet_by_countries file is cleared before "
                                             "collecting new tweets")
@click.option('--map-output-path', default='twitter_sentiment_mapping/visualisation/sentiment_map.png')
@click.option('--update-status', default=False, help='If update-status=True, a publication will be posted with a '
                                                     'default text and the map created ')
def main(
        config_path: str,
        tweets_path: str,
        keyword: str,
        compute_geocodes: bool,
        nb_tweets_to_collect_by_country: int,
        traduce_keyword: bool,
        collect_only: bool,
        clear: bool,
        map_output_path: str,
        update_status: bool
) -> None:
    api = get_api_access(config_path)

    if compute_geocodes:
        geocodes = geocode(COUNTRIES)
    else:
        geocodes = GEOCODES

    tweets_by_countries = collect_tweets(api, geocodes, tweets_path, keyword, traduce_keyword,
                                         nb_tweets_to_collect_by_country, clear)

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
