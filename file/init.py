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
import os
import requests
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
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, remove_all_commands
from credentials import Creds

"""***************************************VARIABLE***************************************"""
c = Creds()
guild_ids = [741227425232453634,531525155537682442]
bot = commands.Bot(command_prefix=c.get_prefix(2))
slash = SlashCommand(bot, sync_commands=True)
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
    await remove_all_commands(c.get_id(2),c.get_token(2),guild_ids=guild_ids)
    """thread_twitter_stream = threading.Thread(target=twitter.checkTweet,
                                             args=(asyncio.get_event_loop(),),
                                             daemon=True)
    thread_twitter_stream.start()
    booru.start()"""


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
        embed.add_field(name="PrÃ©fixe", value=bot.command_prefix, inline=False)
        embed.add_field(name="CrÃ©ateur", value="@Kurosagi#1904", inline=False)
        embed.add_field(name="Divers", value="**1. n!help** pour obtenir de l'aide\n"
                                             "2. API utilisÃ© : [AzurAPI](https://azurapi.github.io/)", inline=False)
        await message.channel.send(file=thumb, embed=embed)
    await bot.process_commands(message)


@bot.command(name="help")
async def help(ctx, options=""):
    await helpCorner.help(ctx, options)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@bot.command
async def _ship(ctx, ship):
    await ship(ctx, ship)

"""
@slash.slash(name="ship",
             description="Retourne les informations du wiki pour un personnage", guild_ids=guild_ids, options=[
        create_option(
            name="name",
            description="Entrer le nom du personnage",
            option_type=3,
            required=True,
        )
    ])
async def __ship(ctx, name):
    await ship(ctx, name)
"""

async def ship(ctx, ship):
    try:
        await shipInfo.info(ctx, ship, bot)
    except:
        await ctx.send("<@!142682730776231936>\n```" + str(traceback.format_exc()) + "```")


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
@slash.slash(name="skin",
             description="Affiche les skin d'un personnage", guild_ids=guild_ids, options=[
        create_option(
            name="name",
            description="Entrer le nom du personnage",
            option_type=3,
            required=True,
        )
    ])
async def __skin(ctx, name):
    await _skin(ctx, name)
"""
@bot.command(name="skin")
async def skin(ctx, ship):
    await _skin(ctx,ship)


async def _skin(ctx, ship):
    try:
        await shipSkin.getSkin(ctx, ship, bot)
    except:
        await ctx.send("<@!142682730776231936>\n```" + str(traceback.format_exc()) + "```")


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""
@slash.slash(name="stat",
             description="Affiche les stats d'un personnage", guild_ids=guild_ids, options=[
        create_option(
            name="name",
            description="Entrer le nom du personnage",
            option_type=3,
            required=True,
        ),
        create_option(
            name="stat_type",
            description="Quel type de stat ?",
            option_type=3,
            required=True,
            choices=[
                create_choice(name="Base",value="baseStats"),
                create_choice(name="Level 100", value="100"),
                create_choice(name="Level 120", value="120"),
                create_choice(name="Level 100 Retrofit", value="100r"),
                create_choice(name="Level 120 Retrofit", value="120r"),
            ]
        )
    ])
async def stat(ctx, name, stat_type):
    await _stat(ctx, name, stat_type)
"""

@bot.command(name="stat")
async def stat(ctx, ship, level="baseStats"):
    await _stat(ctx, ship, level)


async def _stat(ctx, ship, level="baseStats"):
    await shipStat.getStats(ctx, ship, level)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""@bot.command(name="id")
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
            description="**Utilisation possible** :\nn!id list : renvoie la liste d'id enregistrÃ©e\nn!id add @Pseudo 'ID' 'SERVEUR' : enregistre une nouvelle id"))"""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@bot.command(name="search")
async def danbooru_search(ctx, character, number=1):
    await Danbooru.search_picture(ctx, character, number)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@bot.command(name="send")
@commands.has_role('Admirals')
async def sayBot(ctx, channelId, msg):
    await bot.get_channel(int(channelId)).send(msg)
    await discord.Message.delete(ctx.message)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""
@slash.slash(name="build", description="Retourne une liste des personnages obtenable à  un temps donné",
             guild_ids=guild_ids, options=[
        create_option(name="timer", description="Format: HH:MM:SS, pour voir tout les temps de construction disponible, écrivez list", option_type=3, required=False)
    ])
async def __build(ctx, timer=None):
    await _build(ctx, timer)
"""

@bot.command(name="build")
async def build(ctx, arg=None):
    await _build(ctx, arg)


async def _build(ctx, arg=None):
    if arg != None:
        if arg == "list":
            await buildTime.timeList(ctx, bot)
        elif re.match(r"^\d\d\:\d\d\:\d\d$", arg):
            await buildTime.buildTimer(ctx, arg, bot)
        else:
            await ctx.send("Format: n!build <Timer> (Exemple: n!build 01:25:00)")
    else:
        await ctx.send("Format: n!build <Timer> (Exemple: n!build 01:25:00)")


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@bot.command(name="skill")
async def skill(ctx, arg):
    await skill(ctx, arg)


async def _skill(ctx, arg):
    if arg != ():
        await skillInfo.getSkill(ctx, arg)
    else:
        await ctx.send("Format: n!skill <Nom> (Exemple: n!skill Cleveland)")


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@bot.command
async def test(ctx, arg1):
    await _test(ctx, arg1)


async def _test(ctx, arg1):
    try:
        await testC.testfield(ctx, arg1)
    except:
        await ctx.send("<@!142682730776231936>\n```" + str(traceback.format_exc()) + "```")


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@bot.command(name="fbi")
@commands.has_any_role('Admirals', "Police d'Images")
async def fbi(ctx, *arg):
    try:
        file = "../json/forbiddenCharacter.json"
        datajson = json.load(open(file))
        ship = []
        check_done = False
        for a in arg:
            ship.append(a)
        print(datajson["forbiddenChar"])
        for s in ship:
            if s in datajson["forbiddenChar"]:
                await ctx.send("Chibre")
                check_done = True
        if not check_done:
            for name in ship:
                datajson["forbiddenChar"].append(name)
            with open("../json/forbiddenCharacter.json", 'w') as out:
                json.dump(datajson, out)
            await ctx.send("AjoutÃ© !")
    except:
        print(traceback.format_exc())


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
@slash.subcommand(base="sub", name="list", description="Affiche ta liste de personnage suivi", guild_ids=guild_ids)
async def __sub_list(ctx):
    await sub(ctx, "list", None)


@slash.subcommand(base="sub", name="add", description="Ajouter un/des personnages à ta liste de suivi",
                  guild_ids=guild_ids, options=[
        create_option(name="names",
                      description="Ajouter une virgule entre chaque personnage",
                      option_type=3, required=True)
    ])
async def __sub_add(ctx, names):
    if "," in names:
        names = names.split(",")
        await sub(ctx, "add", names)
    else:
        list_name = []
        list_name.append(names)
        await sub(ctx, "add", list_name)


@slash.subcommand(base="sub", name="remove", description="Supprime un/des personnage de ta liste de suivi",
                  guild_ids=guild_ids, options=[create_option(name="names",
                                                              description="Ajouter une virgule entre chaque personnage",
                                                              option_type=3, required=True)])
async def __sub_remove(ctx, names):
    if "," in names:
        names=names.split(",")
        await sub(ctx, "remove", name)
    else:
        list_name=[]
        list_name.append(names)
        await sub(ctx, "remove", list_name)



@slash.subcommand(base="sub", name="nsfw",
                  description="Choisir si vous voulez être ping lors de l'apparition d'une image dans le salon nsfw",
                  guild_ids=guild_ids,
                  options=[create_option(name="choice", description="Votre choix",
                                         option_type=3, required=True,
                                         choices=[
                                             create_choice(name="Activer les notifications dans le salon NSFW",
                                                           value="y"),
                                             create_choice(name="Desactiver les notifications dans le salon NSFW",
                                                           value="n")
                                         ])])
async def __sub_nsfw(ctx, choice):
    await sub(ctx, "nsfw", choice)


@slash.subcommand(base="sub", name="purge", description="Vide entièrement ta liste de personnage suivi",
                  guild_ids=guild_ids, )
async def __sub_purge(ctx):
    await sub(ctx, "purge", None)


@slash.subcommand(base="sub", name="search",
                  description="Retourne la liste des personnes qui suivent le personnage demandé",
                  guild_ids=guild_ids, options=[create_option(name="name",
                                                              description="Un seul personnage a la fois",
                                                              option_type=3, required=True)])
async def __sub_search(ctx, name):
    list_name=[]
    list_name.append(name)
    await sub(ctx, "search", list_name)
"""

@bot.command(name="sub")
async def _sub(ctx, type, *arg):
    try:
        arg=reconstruct_string(arg)
        await sub(ctx, type, arg)
    except:
        await ctx.send("<@!142682730776231936>\n```" + str(traceback.format_exc()) + "```")


async def sub(ctx, type, arg):
    try:
        await Booru.sub(ctx, type, arg)
    except:
        await ctx.send("<@!142682730776231936>\n```" + str(traceback.format_exc()) + "```")

def reconstruct_string(arg):
    construct = []
    b = ""
    for a in arg:
        if not "," in a:
            b += a + " "
        else:
            b += a.replace(",", "")
            construct.append(b.strip())
            b = ""
    construct.append(b.strip())
    return construct

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@bot.event
async def on_slash_command_error(ctx, err):
    print(err)


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
    sleep_counter = 1
    try:
        await Danbooru.post(bot.get_channel(668493142349316106), bot.get_channel(668428634201260042),
                            bot.get_channel(739145500560982034), bot)
    except pybooru.exceptions.PybooruHTTPError:
        time.sleep(60 * sleep_counter)
        booru.restart()
        sleep_counter += 1
    except:
        await bot.get_channel(534084645109628938).send(
            "<@!142682730776231936>\n```" + str(traceback.format_exc()) + "```")


@booru.before_loop
async def before_booru():
    print("DÃ©but de boucle")
    await bot.wait_until_ready()


@booru.after_loop
async def after_booru():
    print("Fin de boucle")


@bot.command(name="check")
async def check(ctx, state=None):
    await Danbooru.check(ctx, state)


""""***************************************RUN***************************************"""

bot.run(c.get_token(2))
