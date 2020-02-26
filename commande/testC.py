import discord
import asyncio
from bs4 import BeautifulSoup
import requests
from DAO import DAO

async def chibre(ctx):
    namelist = []
    sublist = []
    with open("../textfile/SubBooru") as f:
        for cnt, line in enumerate(f):
            print(cnt, line)
            name = line[0:line.index(":")]
            ship = line[line.index(":")+1:len(line)].replace("\n","")
            shipList = ship.split(",")
            namelist.append(name)
            sublist.append(shipList)
    await ctx.send("Test fast, fail fast, adjust fast.")