import discord
import asyncio
from bs4 import BeautifulSoup
import requests
import json
from DAO import DAO
from azurlane.azurapi import AzurAPI
api = AzurAPI()

async def testfield(ctx, arg):
    shipname = ""
    for a in arg:
	    shipname += a
    for skin in api.getShip(ship=shipname).get("skins"):
    	await ctx.send(skin.get("name"))
