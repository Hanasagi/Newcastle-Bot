from DAO import DAO
import discord
import asyncio
import re

async def timeList(ctx,bot):
    dao = DAO()
    dao.select("ship",["BuildTime"])
    regexNum=re.compile(r"[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?")
    timeList = [item[0] for item in dao.cursor.fetchall() if re.match(r"[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?",str(item[0]))]
    time = set(timeList)
    lt = list(time)
    lt.sort()
    embed = discord.Embed(title="Timer possible")
    embed.description=""
    sBuild=""

    min=0
    max=10
    left = '◀'
    right = '▶'

    def predicate(message, l, r):
        def check(reaction, user):
            if reaction.message.id != message.id or user == bot.user:
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
    while True:
        try:
            for i in range(min, max):
                embed.description += "**" + lt[i] + "**\n"
            res = await action(embed=embed)
            if res is not None:
                msg = res
            l = index != min
            r = index != max
            await msg.add_reaction(left)
            await msg.add_reaction(right)
            react, user = await bot.wait_for('reaction_add', check=predicate(msg, lt, r), timeout=20)
            if react.emoji == left:
                min-=10
                max-=10
                if(min<0):
                    max=len(lt)
                    min=max-10
            elif react.emoji == right:
                min += 10
                max += 10
                if(max>len(lt)):
                    min=0
                    max=10
            action = msg.edit
            embed.description=""
        except asyncio.TimeoutError:
            await msg.clear_reactions()
            break

async def buildTimer(ctx,arg,bot):
    dao = DAO()
    dao.select("ship", ["Name"],"BuildTime",arg)
    nameList = [item[0] for item in dao.cursor.fetchall()]
    embed = discord.Embed(title="Temps de construction : "+arg,description="")

    if(len(nameList)>10):
        min=0
        max=10
        left = '◀'
        right = '▶'

        def predicate(message, l, r):
            def check(reaction, user):
                if reaction.message.id != message.id or user == bot.user:
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
        while True:
            try:
                for i in range(min, max):
                    embed.description += "**" + nameList[i] + "**\n"
                res = await action(embed=embed)
                if res is not None:
                    msg = res
                l = index != min
                r = index != max
                await msg.add_reaction(left)
                await msg.add_reaction(right)
                react, user = await bot.wait_for('reaction_add', check=predicate(msg, l, r), timeout=20)
                if react.emoji == left:
                    if (min < 0):
                        max = len(nameList)
                        min = max - 10
                    if max >= len(nameList):
                        max=len(nameList)-(len(nameList)-10)
                        min=max-10
                    else:
                        min -= 10
                        max -= 10
                elif react.emoji == right:
                    min += 10
                    max += 10
                    if max == len(nameList):
                        max=10
                        min=0
                    elif max > len(nameList):
                        max = len(nameList)
                    if min > len(nameList):
                        min=0
                        max=10
                action = msg.edit
                embed.description = ""
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                break
    else:
        for n in nameList:
            embed.description += n + '\n'
        await ctx.send(embed=embed)