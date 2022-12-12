from datetime import date


def todays_date():
    today = date.today()
    return today.strftime("%B %d, %Y")

def default_tweet_text(keyword):
    return f"Sentiment map of {todays_date()} with keyword : {keyword}"

def upload_tweet(api, tweet_text: str, image_path: str) -> None:
    upload = api.media_upload(filename = image_path)
    media_ids = [upload.media_id_string]
    api.update_status(media_ids = media_ids, status=tweet_text)

