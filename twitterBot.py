import tweepy
from tweepy import StreamListener, Stream
import json
from discord import Webhook, RequestsWebhookAdapter

# Copy your discord webhook url
webhook_url = ""
webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())

# Get these keys and tokens from your twitter dev account
api_key = ""
api_secret_key = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Add the account username you want to stream to this list
list_of_accounts = []

# Getting their IDs
list_of_IDs = []
for screen_name in list_of_accounts:
    list_of_IDs.append(str(api.get_user(screen_name).id))

class StdOutListener(StreamListener):

    def on_data(self, data):
        # process stream data here
        decoded = json.loads(data)
        decodedUserID = decoded['user']['id_str']
        if decodedUserID in list_of_IDs:
            tweeter = "@" + decoded['user']['screen_name']
            message = tweeter + " tweeted:\n" + decoded['text']
            webhook.send(message)

    def on_status(self, status):
        print ("f {status.text} {status.author.screen_name}, {status.created_at}, {status.source}")

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    listener = StdOutListener()
    twitterStream = Stream(auth,listener)
    twitterStream.filter(follow = list_of_IDs)