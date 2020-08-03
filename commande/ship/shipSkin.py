import discord
import json
from azurlane.azurapi import AzurAPI
api = AzurAPI()

async def getSkin(ctx, ship, bot=None):
    api.updater.update()
    with open('../json/shipList.json', 'r', encoding='utf8') as input:
        data = input.read()
    nameList = json.loads(data)
    ship = ship.lower()

    embedList = []
    for skin in api.getShip(ship=ship).get("skins"):
        embedBase = discord.Embed(title=api.getShip(ship=ship).get("names").get("en"), description=skin.get("name"))
        embedBase.set_image(url=skin.get("image"))
        embedBase.set_thumbnail(url=skin.get("chibi"))
        embedList.append(embedBase)

    left = '◀'
    right = '▶'

    def predicate(message, l, r):
        def check(reaction, user):
            if reaction.message.id != message.id or user != ctx.author:
                return False
            if l and reaction.emoji == left:
                return True
            if r and reaction.emoji == right:
                return True
            return False

        return check

    index = 0
    msg = None
    action = ctx.send
    if len(embedList) > 1:
        while True:
            try:
                res = await action(embed=embedList[index])
                if res is not None:
                    msg = res
                l = index != 0
                r = index != len(embedList) - 1
                await msg.add_reaction(left)
                await msg.add_reaction(right)
                react, user = await bot.wait_for('reaction_add', check=predicate(msg, l, r), timeout=20)

                if react.emoji == left:
                    if index < 1:
                        print(0)
                        index = len(embedList) - 1
                    else:
                        index -= 1
                elif react.emoji == right:

                    if index == len(embedList) - 1:
                        print("ntm")
                        index = 0
                    index += 1
                    print(len(embedList) - 1)
                    print(index)
                action = msg.edit
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                break
    else:
        await action(embed=embedList[0])

            
            