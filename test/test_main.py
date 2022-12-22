from main import main
from click.testing import CliRunner

def test_main() -> None:
    config_path = ''
    tweets_path = ''
    keyword = '*'
    compute_geocodes = True
    nb_tweets_to_collect = 3
    collect_only = False
    clear = False
    map_output_path = # add temp path
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
            "--nb-tweets-to-collect",
            nb_tweets_to_collect,
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
