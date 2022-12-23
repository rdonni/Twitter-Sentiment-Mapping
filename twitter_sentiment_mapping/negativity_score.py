from tqdm import tqdm


def score(sentiment_score_by_countries):

    print('----------------------- Calculating sentiment scores... -----------------------')

    for country in tqdm(sentiment_score_by_countries.keys()):
        if isinstance(sentiment_score_by_countries[country], list):

            negative_count = 0
            neutral_count = 0
            positive_count = 0

            for i in range(len(sentiment_score_by_countries[country])):

                scores = sentiment_score_by_countries[country][i]

                if max(scores) == scores[0]:  # Negative tweet
                    negative_count += 1
                elif max(scores) == scores[1]:  # Neutral tweet
                    neutral_count += 1
                else:  # Positive tweet
                    positive_count += 1

            print(country, negative_count, neutral_count, positive_count)
            sentiment_score = (positive_count - negative_count) / len(sentiment_score_by_countries[country])
            sentiment_score_by_countries[country] = sentiment_score

        else:
            sentiment_score_by_countries[country] = None

    print("----------------------- Sentiment scores calculated -----------------------")
    return sentiment_score_by_countries
