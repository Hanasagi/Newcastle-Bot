"""***************************************IMPORT***************************************"""
import discord
import json
import helpCorner
import time
import threading
import testC
import sys
import signal
import random
import re
import asyncio
import threading
import welcome_message
import traceback
import random
import pybooru
from db import dbConnect
from ship import buildTime
from db import al_id
from ship import shipInfo
from ship import skillInfo
from ship import shipSkin
from ship import shipStat
from webhook_rss import sub as Booru
from webhook_rss import Danbooru
from webhook_rss import twitter
# from webhook_rss import twitter
from DAO import DAO
from discord.ext import commands, tasks
from credentials import Creds

"""***************************************VARIABLE***************************************"""
c = Creds()
bot = commands.Bot(command_prefix=c.get_prefix(1))
bot.remove_command('help')

"""***************************************SIGNAL HANDLING***************************************"""


def stop_everything(sigNum, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, stop_everything)

"""***************************************COMMANDE***************************************"""


@bot.event
async def on_ready():
    print('{0} online!'.format(bot.user.name))
    rndChar = random.choice(["Essex", "Sandy", "Jules", "Hammann", "Hipper", "Akashi", "Manjuu"])
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("bully " + rndChar))
    thread_twitter_stream = threading.Thread(target=twitter.checkTweet,
                                             args=(asyncio.get_event_loop(),),
                                             daemon=True)
    thread_twitter_stream.start()
    booru.start()


@bot.event
async def on_guild_join(guild):
    data = json.load(open("../json/guildInfo.json", "r"))
    data["guild"].append({"id": guild.id})
    with open("../json/guildInfo.json", "w") as o:
        json.dump(data, o)


@bot.event
async def on_message(message):
    if bot.user.mention in message.content.replace('!', ''):
        embed = discord.Embed()
        thumb = discord.File("../image/NewcastleIcon.png", filename="thumb.png")
        embed.set_thumbnail(url="attachment://thumb.png")
        embed.add_field(name="Préfixe", value=bot.command_prefix, inline=False)
        embed.add_field(name="Créateur", value="@Kurosagi#1904", inline=False)
        embed.add_field(name="Divers", value="**1. n!help** pour obtenir de l'aide\n"
                                             "2. API utilisé : [AzurAPI](https://azurapi.github.io/)", inline=False)
        await message.channel.send(file=thumb, embed=embed)
    await bot.process_commands(message)


@bot.command(name="help")
async def help(ctx, options=""):
    await helpCorner.help(ctx, options)


@bot.command(name="dbshipset")
@commands.has_role("Bot Master")
async def dbShipset(message):
    await dbConnect.dbshiplink(message);


@bot.command(name="dbskillset")
@commands.has_role("Bot Master")
async def dbSkillset(message):
    await dbConnect.dbskillset(message);


@bot.command(name="dbshipupdate")
@commands.has_role("Bot Master")
async def dbShipupdate(message):
    await dbConnect.dbshipupdate(message);


@bot.command(name="ship")
async def ship(ctx, ship1=None, ship2=None, ship3=None, ship4=None):
    try:
        if ship1 != None:
            await shipInfo.info(ctx, ship1, ship2, ship3, ship4, bot, False)
        else:
            await ctx.send("Format: n!ship <Nom> (Exemple: n!ship Prinz Eugen)")
    except:
        await ctx.send("<@!142682730776231936>\n```" + str(traceback.format_exc()) + "```")


@bot.command(name="skin")
async def skin(ctx, ship):
    try:
        await shipSkin.getSkin(ctx, ship, bot)
    except:
        await ctx.send("<@!142682730776231936>\n```" + str(traceback.format_exc()) + "```")


@bot.command(name="stat")
async def skin(ctx, ship, level="baseStats"):
    await shipStat.getStats(ctx, ship, level)


@bot.command(name="id")
async def idAdd(ctx, method="x", pseudo="x", id="x", server="x"):
    if "add" in method:
        if len(pseudo) == 1 or len(id) == 1 or len(server) == 1:
            await ctx.send(
                "Format: n!id add <Pseudo> <Id> <Serveur> (Exemple: n!id @Kurosagi 123456789 Sandy)\n(Utilisez votre tag discord pour le pseudo)")
        elif not "@" in pseudo:
            await ctx.send("Mauvais format de pseudo, utilisez votre tag discord")
        else:
            await al_id.idAdd(ctx, pseudo, id, server)
    elif "list" in method:
        await al_id.idList(ctx, bot)
    else:
        await ctx.send(embed=discord.Embed(
            description="**Utilisation possible** :\nn!id list : renvoie la liste d'id enregistrée\nn!id add @Pseudo 'ID' 'SERVEUR' : enregistre une nouvelle id"))


@bot.command(name="search")
async def danbooru_search(ctx, character, number=1):
    await Danbooru.search_picture(ctx, character, number)


@bot.command(name="send")
@commands.has_role('Admirals')
async def sayBot(ctx, channelId, msg):
    await bot.get_channel(int(channelId)).send(msg)
    await discord.Message.delete(ctx.message)


@bot.command(name="build")
async def build(ctx, arg=None):
    if arg != None:
        if arg == "list":
            await buildTime.timeList(ctx, bot)
        elif re.match(r"^\d\d\:\d\d\:\d\d$", arg):
            await buildTime.buildTimer(ctx, arg, bot)
        else:
            await ctx.send("Format: n!build <Timer> (Exemple: n!build 01:25:00)")
    else:
        await ctx.send("Format: n!build <Timer> (Exemple: n!build 01:25:00)")


@bot.command(name="skill")
async def skill(ctx, *arg):
    if arg != ():
        await skillInfo.getSkill(ctx, arg)
    else:
        await ctx.send("Format: n!skill <Nom> (Exemple: n!skill Cleveland)")


@bot.command(name="test")
async def test(ctx, arg1=None):
    try:
        await testC.testfield(ctx, arg1)
    except:
        await ctx.send("<@!142682730776231936>\n```" + str(traceback.format_exc()) + "```")



@bot.command(name="shiplist")
@commands.has_role('Admirals')
async def updatelist(ctx):
    dao = DAO()
    dao.select("ship", ["Name"])
    nameList = [item[0].lower() for item in dao.cursor.fetchall()]
    nameSet = set(nameList)
    with open('../json/shipList.json', 'w', encoding='utf8') as f:
        outlist = json.dumps(list(nameSet))
        f.write(outlist)
    await ctx.send("Liste mise à jour !")


@bot.command(name="fbi")
@commands.has_role('Admirals')
async def fbi(ctx, *arg):
    with open("../json/forbiddenCharacter.json", 'r') as f:
        data = f.read()
    datajson = json.loads(data)
    ship = ""
    for a in arg:
        ship += a + " "
    datajson["forbiddenChar"].append(ship[:-1])
    with open("../json/forbiddenCharacter.json", 'w') as out:
        json.dump(datajson, out)
    await ctx.send("Ajouté !")


@bot.command(name="sub")
async def sub(ctx, type, *arg):
    try:
        await Booru.sub(ctx, type, arg)
    except:
        await ctx.send("<@!142682730776231936>\n```" + str(traceback.format_exc()) + "```")


@updatelist.error
@test.error
@dbSkillset.error
@dbShipset.error
async def error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Tu n'as pas les droits !")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Commande inexistante")
        return


@tasks.loop(seconds=20)
async def booru():
    sleep_counter=1
    try:
        await Danbooru.post(bot.get_channel(668493142349316106), bot.get_channel(668428634201260042),
                            bot.get_channel(739145500560982034), bot)
    except pybooru.exceptions.PybooruHTTPError:
        time.sleep(60*sleep_counter)
        booru.restart()
        sleep_counter+=1
    except:
        await bot.get_channel(534084645109628938).send(
                "<@!142682730776231936>\n```" + str(traceback.format_exc()) + "```")



@booru.before_loop
async def before_booru():
    print("Début de boucle")
    await bot.wait_until_ready()


@booru.after_loop
async def after_booru():
    print("Fin de boucle")


@bot.command(name="check")
async def check(ctx, state=None):
    await Danbooru.check(ctx, state)


""""***************************************RUN***************************************"""

bot.run(c.get_token(1))