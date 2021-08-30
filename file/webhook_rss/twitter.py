import tweepy
import time
import discord
import sys
import inspect
import asyncio
import json
import signal
import traceback
import requests
from credentials import Creds

c = Creds()

API_KEY = c.get_api_key()
API_SECRET_KEY = c.get_api_secret_key()
ACCESS_TOKEN = c.get_access_token()
ACCESS_TOKEN_SECRET = c.get_access_token_secret()

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
auth.secure = True

api = tweepy.API(auth)


# http://gettwitterid.com/?user_name=itanimeirl&submit=GET+USER+ID

def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, loop,url):
        super(MyStreamListener, self).__init__()
        self.loop = loop
        self.url= url

    async def msg_send_wrapper(self, status):
        data = {}

        data["embeds"] = []
        embed = {}

        embed["url"] = "https://twitter.com"
        if hasattr(status, 'text'):
            try:
                embed["description"] = status.extended_tweet['full_text']
            except AttributeError:
                embed["description"] = status.text
        embed["footer"] = {
            "text": str(status.created_at)
        }
        if status.is_quote_status:
            embed["fields"] = [
                {
                    "name": "Quoted Tweet",
                    "value": status.quoted_status_permalink["expanded"]
                }
            ]
        embed["author"] = {
            "name": status.user.name,
            "icon_url": status.user.profile_image_url_https
        }
        if status.user.id == "993682160744738816":
            embed["color"] = 15263976
        elif status.user.id == "864400939125415936":
            embed["color"] = 16777215
        if status.extended_tweet:
            if 'media' in status.extended_tweet["entities"]:
                nb = 0
                for media in status.extended_tweet["entities"]["media"]:
                    print(media)
                    print(media["media_url_https"])
                    if nb < 1:
                        embed["image"] = {
                            "url": media["media_url_https"]
                        }
                        print(media["media_url_https"])
                    else:
                        data["embeds"].append({
                            "url": "https://twitter.com",
                            "image": {
                                "url": media["media_url_https"]
                            }
                        })
                    nb += 1
                data["embeds"].insert(0, embed)
            else:
                data["embeds"].append(embed)
        result = requests.post(self.url, data=json.dumps(data), headers={"Content-Type": "application/json"})

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            pass

        return

    def on_status(self, status):
        if from_creator(status):
            try:
                send_fut = asyncio.run_coroutine_threadsafe(self.msg_send_wrapper(status), self.loop)
                send_fut.result()
            except:
                print(str(traceback.format_exc()))
                pass


def checkTweet(loop,url):
    counter = 1
    print("Twitter stream is running")
    myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener(loop=loop,url=url), tweet_mode='extended')
    while True:
        try:
            myStream.filter(follow=['993682160744738816', '864400939125415936'],stall_warnings=True)
        except:
            print(traceback.format_exc())
            time.sleep(60 * counter)
            counter += 1
            print("Twitter stream has restarted")
            continue
