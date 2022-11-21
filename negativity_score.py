# Imports 
import numpy as np
from tqdm import tqdm


def score(sentiment_score_by_countries):
    
    
    for country in tqdm(sentiment_score_by_countries.keys()) :
        
        if isinstance(sentiment_score_by_countries[country], list): # if scores are of type list, it means that the sentiment score is not a nan value

            negative_score = 0
            neutral_score = 0
            positive_score = 0
            
            for i in range(len(sentiment_score_by_countries[country])) : 
            
                scores = sentiment_score_by_countries[country][i]

                if max(scores) == scores[0] : # Negative tweet
                    negative_score += 1
                elif max(scores) == scores[1] : # Neutral tweet
                    neutral_score += 1
                else : # Positive tweet
                    positive_score += 1
                
            print (country, negative_score, neutral_score, positive_score)
            score = (positive_score- negative_score)/ len(sentiment_score_by_countries[country])
            sentiment_score_by_countries[country] = score
        
        
        else : # Else the scores are a nan value and so, the sentiment score of the country is also a nan value
            sentiment_score_by_countries[country] = np.nan
        
        
    print ("----------------------- scores calculated -----------------------")
    return sentiment_score_by_countries 