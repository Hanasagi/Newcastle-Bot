import discord
import json
import re
from azurlane.azurapi import AzurAPI
api = AzurAPI()

async def getStats(ctx, ship, level):
    try:
        desc=""
        regexN=r'^\d\d\d$'
        regexR=r'^\d\d\dr$'
        if re.match(regexN,level):
            desc += "Level " + level
            level="level"+level;
        elif re.match(regexR,level):
            desc += "Level " + level[:-1] + " Retrofit"
            level = "level" + level[:-1] + "Retrofit"
        else:
            desc+="Base"
        api.updater.update()
        ship = ship.lower()
        stat = api.getShip(ship=ship).get("stats").get(level);
        embed = discord.Embed(title="Stats for "+api.getShip(ship=ship).get("names").get("en"),description=desc)
        embed.set_thumbnail(url=api.getShip(ship=ship).get("thumbnail"))
        for n in stat:
           embed.add_field(name="**"+n.title()+"**",value=stat.get(n),inline=True)
        await ctx.send(embed=embed)
    except:
        await ctx.send("Quelque chose ne va pas [message d'erreur provisoire]")
