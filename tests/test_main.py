from main import main
from click.testing import CliRunner
import tempfile


def test_main() -> None:
    config_path = '/Users/rayanedonni/Documents/Projets_persos/News_by_ai/config.ini'
    tweets_path = tempfile.mkdtemp()
    keyword = '*'
    compute_geocodes = True
    nb_tweets_to_collect = 10
    collect_only = False
    clear = False
    map_output_path = tempfile.mkdtemp()
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
