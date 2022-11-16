import tweepy 
import configparser
import cv2

# read config and authentification
config = configparser.ConfigParser()
config.read('/Users/rayanedonni/Documents/Projets_persos/News_by_ai/config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tweet_text='Map of European sentiment of 25th May'
image_path ='/Users/rayanedonni/Documents/Projets_persos/News_by_ai/sentiment_analysis/sentiment_map.png'

im = cv2.imread(image_path)# Read image

new_width = int(im.shape[1]*0.5)
new_height = int(im.shape[0]*0.5)
dim = (new_width, new_height)

imS = cv2.resize(im, dim)  
cv2.imwrite('/Users/rayanedonni/Documents/Projets_persos/News_by_ai/sentiment_analysis/sentiment_map_resized.png', imS)

image_resized_path = '/Users/rayanedonni/Documents/Projets_persos/News_by_ai/sentiment_analysis/sentiment_map_resized.png'

#Generate text tweet with media (image)
upload = api.media_upload(filename = image_resized_path)
media_ids = [upload.media_id_string]
result = api.update_status(media_ids = media_ids, status=tweet_text)