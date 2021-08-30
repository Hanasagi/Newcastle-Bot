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
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from ship import buildTime
from ship import shipInfo
from ship import skillInfo
from ship import shipSkin
from ship import shipStat
from webhook_rss import sub as Booru
from webhook_rss import Danbooru
from webhook_rss import twitter
# from webhook_rss import twitter
from CRUD import CRUD
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, remove_all_commands
from credentials import Creds

"""***************************************VARIABLE***************************************"""
c = Creds()
guild_ids = [741227425232453634, 531525155537682442]
bot = commands.Bot(command_prefix=c.get_prefix(2))
slash = SlashCommand(bot, sync_commands=True)
bot.remove_command('help')
db = CRUD()
#[X][1] = show_news [X][2] = danbooru_feed
guild_options = []
task_list=[]
"""***************************************STUFF***************************************"""


def stop_everything(sigNum, frame):
    db.close()
    for task in task_list:
        task.cancel()
    sys.exit(0)


async def print_err(ctx):
    await ctx.send(
        "Something seems to have gone wrong, those kind of things are unfortunately not my forte, maybe we should ask for help ?")
    await ctx.send("<@!142682730776231936>\n```" + str(traceback.format_exc()) + "```")


def reconstruct_string(arg):
    construct = []
    b = ""
    if not isinstance(arg, tuple):
        arg = [arg]
    for a in arg:
        if len(arg) > 1:
            if not "," in a:
                b += a + " "
            else:
                b += a.replace(",", "")
                construct.append(b.strip())
                b = ""
        else:
            break
    if len(arg) > 1:
        construct.append(b.strip())
    else:
        if "," in arg[0]:
            b = arg[0].split(",")
            for x in b:
                construct.append(x.strip())
        else:
            b += arg[0]
            construct.append(b.strip())
    return construct


signal.signal(signal.SIGINT, stop_everything)

"""***************************************COMMANDE***************************************"""


@bot.event
async def on_ready():
    print('{0} online!'.format(bot.user.name))
    rndChar = random.choice(["Essex", "Sandy", "Jules", "Hammann", "Hipper", "Akashi", "Manjuu"])
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("bully " + rndChar + "| n!help"))
    for guild in bot.guilds:
        db.select("options", ["uid","show_news", "danbooru_feed"], "uid", guild.id)
        guild_options.append(db.cursor.fetchall())
    for guild in guild_options:
        print(guild[0][2])
        if guild[0][1] != 0: #news
            db.select("options", ["webhook_url"], "uid", guild[0][0])
            url = db.cursor.fetchall()
            thread_twitter_stream = threading.Thread(target=twitter.checkTweet,
                                             args=(asyncio.get_event_loop(),url[0][0]),
                                             daemon=True)
            thread_twitter_stream.start()
        if guild[0][2] != 0: #danbooru
            db.select("options",["sfw_danbooru_channel","nsfw_danbooru_channel","check_channel"],"uid", guild[0][0])
            result=db.cursor.fetchall()
            guild_channel=bot.get_guild(int(guild[0][0]))
            if result[0][2] != "":
                check = guild_channel.get_channel(int(result[0][2]))
            else:
                check=0
            try:
                db.select("danbooru_list_"+guild[0][0],["*"])
            except mysql.connector.errors.ProgrammingError:
                db.create("danbooru_list_" + guild[0][0], ["name","nsfw","charlist"],["varchar(255)","varchar(3)","json"])
            task = tasks.loop(seconds=60)(booru)
            task.start(guild_channel.get_channel(int(result[0][0])),guild_channel.get_channel(int(result[0][1])),check,guild[0][0])
            task.before_loop(before_booru)
            task.after_loop(after_booru)
            task_list.append(task)
    print(task_list)

@bot.event
async def on_guild_join(guild):
    db.insert("guild", ["uid", "name", "lang"], [str(guild.id), guild.name, "EN"], )
    db.insert("options", ["uid", "show_news", "webhook_url","danbooru_feed","news_channel","check_channel","sfw_danbooru_channel","nsfw_danbooru_channel","last_id"], [str(guild.id), 0, "",0,"","","","",""], )
    db.select("options", ["uid","show_news", "danbooru_feed"], "uid", guild.id)
    guild_options.append(db.cursor.fetchall())
    print(guild_options)

@bot.event
async def on_guild_remove(guild):
    db.delete("guild", "uid", str(guild.id),)
    db.delete("options", "uid", str(guild.id),)
    db.drop("danbooru_list_"+str(guild.id),)
    for g in guild_options:
        if str(guild.id) == str(g[0][0]):
            guild_options.remove(g)



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
        await message.channel.send("Here is my business card, let me know if you got work for me.")
        await message.channel.send(file=thumb, embed=embed)
    await bot.process_commands(message)


@bot.command(name="help")
async def help(ctx, options=""):
    await helpCorner.help(ctx, options)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@bot.command(name="ship")
async def _ship(ctx, *shipName):
    try:
        await ship(ctx, shipName)
    except:
        await print_err(ctx)


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
        ship = reconstruct_string(ship)
        await ctx.send("Please review these documents properly, Commander.")
        await shipInfo.info(ctx, ship[0], bot)
    except:
        await print_err(ctx)


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
    await _skin(ctx, ship)


async def _skin(ctx, ship):
    try:
        ship = reconstruct_string(ship)
        await ctx.send(
            "Don't go spending all our money on outfits. I'd appreciate if you did buy me one, nevertheless.")
        await shipSkin.getSkin(ctx, ship[0], bot)
    except:
        await print_err(ctx)


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
    try:
        await ctx.send(
            "Please don't pay too much attention to these, statistics doesn't embody how we perform on the battlefield.")
        await shipStat.getStats(ctx, ship, level)
    except:
        await print_err(ctx)


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
        await ctx.send(
            "I really hope you're planning to build my sisters in the near future. I really do want to live a laid back life in their company.")
        if arg == "list":
            await buildTime.timeList(ctx, bot)
        elif re.match(r"^\d\d\:\d\d\:\d\d$", arg):
            await buildTime.buildTimer(ctx, arg, bot)
        else:
            await ctx.send(
                "The guide seems to tell you to do it that way : n!build <Timer> (Exemple: n!build 01:25:00). Please try again. ")
    else:
        await ctx.send(
            "The guide seems to tell you to do it that way : n!build <Timer> (Exemple: n!build 01:25:00). Please try again. ")


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@bot.command(name="skill")
async def skill(ctx, arg):
    await skill(ctx, arg)


async def _skill(ctx, arg):
    if arg != ():
        await ctx.send(
            "It is a good thing you are reviewing yor fleet that carefully. Maybe with you we could return to peace sooner that expected..")
        await skillInfo.getSkill(ctx, arg)
    else:
        await ctx.send(
            "The guide seems to tell you to do it that way : n!skill <Nom> (Example: n!skill Cleveland). Please try again.")


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@bot.command(name="test")
async def test(ctx, arg1=""):
    try:
        await _test(ctx, arg1)
    except:
        print(traceback.format_exc())


async def _test(ctx, arg1=""):
    try:
        await testC.testfield(ctx, "","")
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
        if "list" in arg:
            charlist = ""
            for s in datajson["forbiddenChar"]:
                charlist += " " + s.title() + ","
            await ctx.send(charlist)
        else:
            for a in arg:
                ship.append(a)
            for s in ship:
                if s in datajson["forbiddenChar"]:
                    check_done = True
            if not check_done:
                for name in ship:
                    datajson["forbiddenChar"].append(name)
                with open("../json/forbiddenCharacter.json", 'w') as out:
                    json.dump(datajson, out)
                await ctx.send("She has been added on the watchlist. Good for her.")
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
        if not len(arg)==0:
            arg = reconstruct_string(arg)
        await sub(ctx, type, arg)
    except:
        await print_err(ctx)


async def sub(ctx, type, arg):
    try:
        await Booru.sub(ctx, type, arg, db)
    except:
        await print_err(ctx)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@bot.event
async def on_slash_command_error(ctx, err):
    print(err)


async def error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have the right for that. Maybe try asking the higher ups for permissions ?")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("This command does not exist, did you reade carefully the help given to you ?")
        return



async def booru(sfw_channel,nsfw_channel,check_channel,guild_id):
    sleep_counter = 1
    try:
        if check_channel==0:
            await Danbooru.check("","n")
        await Danbooru.post(sfw_channel,nsfw_channel,check_channel, db, guild_id, bot)
    except pybooru.exceptions.PybooruHTTPError:
        time.sleep(60 * sleep_counter)
        for task in task_list:
            task.restart()
        sleep_counter += 1
    except:
        await bot.get_channel(534084645109628938).send(
            "<@!142682730776231936>\n```" + str(traceback.format_exc()) + "```")


async def before_booru():
    print("Début de boucle")
    await bot.wait_until_ready()


async def after_booru():
    print("Fin de boucle")


@bot.command(name="check")
async def check(ctx, state=None):
    await Danbooru.check(ctx, state)


""""***************************************RUN***************************************"""

bot.run(c.get_token(2))
