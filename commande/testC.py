import discord
import asyncio
import tweepy
from bs4 import BeautifulSoup
import requests
import json
import traceback
from DAO import DAO
from azurlane.azurapi import AzurAPI
from discord_webhook import DiscordWebhook, DiscordEmbed
import requests  # dependency
import json


def create_message(status):
    text = status.full_text
    embed = discord.Embed(description=text)
    embed.set_author(name=status.user.name, icon_url=status.user.profile_image_url_https)
    if status.is_quote_status:
        embed.add_field(name="Quoted status", value=status.quoted_status_permalink.expanded, inline=False)
    if 'media' in status.entities:
        embed.set_image(url=status.entities['media'][0]['media_url_https'])
    embed.set_footer(text=status.created_at)
    return embed


API_KEY = "jwgN3Npn0zDMS7t61pVgdH4YO"
API_SECRET_KEY = "i5MsP9eR8lAIU1XcaQ5bBPVWIKfgg7fnNTIhMOxeNJdkLxQ2UZ"
ACCESS_TOKEN = "449875906-fMdawprd6vA36GW4cWDTBMlikE1w1CYCy2AB7Nk4"
ACCESS_TOKEN_SECRET = "3nCCfSk9hfHe9vsnjpXUA6ZCXYqEojKQdA7KmcOjGWLsQ"

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
auth.secure = True
api = tweepy.API(auth)

def from_creator(status):
    if status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True

async def testfield(ctx, arg1):
    try:
        if arg1 == "1":
            tweet = api.user_timeline(id=993682160744738816, count=1, tweet_mode='extended')[0]
            await ctx.send(embed=create_message(tweet))
        else:
            status = api.user_timeline(id=993682160744738816, count=1, tweet_mode='extended')[0]
            print(status.entities)
            print('media' in status.entities)
            print('extended_entities' in status.entities)
            if from_creator(status):
                #await ctx.send(embed=create_message(status))
                url = "https://discordapp.com/api/webhooks/769624207125905419/l45iB_5NXc4JDHty9A593fmsOmv4maII6TlLfskj5qXhwsXcySCUGf7IzmVMoTITKWlN"  # webhook url, from here: https://i.imgur.com/aT3AThK.png
                data = {}
                # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
                print(type(data))
                # leave this out if you dont want an embed
                data["embeds"] = []
                embed = {}
                print()
                # for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
                embed["url"] ="https://twitter.com"
                embed["description"] = status.full_text
                embed["footer"]= {
                    "text": str(status.created_at)
                }
                if status.is_quote_status:
                    embed["fields"]= [
                        {
                            "name": "Quoted tweet",
                            "value": status.quoted_status_permalink["expanded"]
                        }
                    ]
                embed["author"] = {
                    "name": status.user.name,
                    "icon_url": status.user.profile_image_url_https
                }

                if 'media' in status.entities:
                    nb = 0
                    for media in status.extended_entities["media"]:
                        if nb < 1:
                            embed["image"] = {
                                "url": media["media_url_https"]
                            }
                        else:
                            data["embeds"].append({
                                "url": "https://twitter.com",
                                "image": {
                                    "url": media["media_url_https"]
                                }
                            })
                        nb += 1
                    data["embeds"].insert(0,embed)
                else:
                    data["embeds"].append(embed)
                print(data)

                result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})

                try:
                    result.raise_for_status()
                except requests.exceptions.HTTPError as err:
                    print(err)
                else:
                    pass

    except:
        await ctx.send("<@!142682730776231936>\n```" + str(traceback.format_exc()) + "```")
