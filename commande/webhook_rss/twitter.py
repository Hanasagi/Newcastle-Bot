"""
import tweepy
import time
import sys
import inspect
import asyncio
import json
import nest_asyncio
import signal
import functools

API_KEY = ""
API_SECRET_KEY = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
auth.secure = True

myStream = None


def shutdown_tweepy(signum, frame):
    myStream.disconnect()


api = tweepy.API(auth)
nest_asyncio.apply()
signal.signal(signal.SIGINT, shutdown_tweepy)


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, channel):
        super(MyStreamListener, self).__init__()
        self.channel = channel
        self.loop = asyncio.get_event_loop()

    async def send_message(self, status):
        print(status.text)
        await self.channel.send('TWEET: ' + str(status.text))
        return "1"

    def on_status(self, status):
        print(status.text)
        if status.text != "NoneType":
            result = self.loop.run_until_complete(self.send_message(status))
            print("Future:"+result)


def checkTweet(bot):
    global myStream
    myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener(bot))
    myStream.filter(track=['AzurLane_EN','azurlane_staff'], is_async=True)
"""