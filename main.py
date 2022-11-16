# Imports
import pickle

from negativity_score import score
from preprocessing import preprocessing
from sentiments_analysis import sentiment_analysis
from Vizualisation.vizualisation import plot


def main(
    #tweets_path : str,
):
    # Get tweets 
    with open("/Users/rayanedonni/Documents/Projets_persos/News_by_ai/sentiment_analysis/tweets_by_countries.pkl", "rb") as handle :
    #with open(tweets_path, "rb") as handle :
        data = handle.read()
    tweets_by_countries = pickle.loads(data)

    for country in tweets_by_countries.keys() :
        print (country, " :", len (tweets_by_countries[country]))

    # Preprocess tweets
    tweets_by_countries = preprocessing(tweets_by_countries)

    # Sentiment Analysis
    sentiment_scores_by_countries = sentiment_analysis(tweets_by_countries)

    # Negativity score
    negativity_score_by_countries = score(sentiment_scores_by_countries)
    for key,value in negativity_score_by_countries.items() :
        print (key, " :", value)

    # Plot the results on a map
    plot(negativity_score_by_countries)


if __name__ == "__main__":
    main()
    
