import os
import tempfile
from pathlib import Path

from click.testing import CliRunner

from main import main


def test_main() -> None:
    config_path = os.path.join(Path(__file__).parents[1], 'twitter_sentiment_mapping', 'api_management', 'config.ini')
    tweets_path = os.path.join(tempfile.mkdtemp(), 'tweets.json')
    keyword = '*'
    compute_geocodes = True
    nb_tweets_to_collect_by_country = 3
    traduce_keyword = True
    collect_only = True
    clear = True
    map_output_path = os.path.join(tempfile.mkdtemp(), 'sentiment_map.png')
    update_status = False

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--config-path",
            config_path,
            "--tweets-path",
            tweets_path,
            "--keyword",
            keyword,
            "--compute-geocodes",
            compute_geocodes,
            "--nb-tweets-to-collect-by-country",
            nb_tweets_to_collect_by_country,
            "--traduce-keyword",
            traduce_keyword,
            "--collect-only",
            collect_only,
            "--clear",
            clear,
            "--map-output-path",
            map_output_path,
            "--update-status",
            update_status
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
