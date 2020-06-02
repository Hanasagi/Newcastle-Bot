"""***************************************IMPORT***************************************"""
import discord
import dbConnect
import time
import buildTime
import Danbooru
import al_id
import shipInfo
import testC
import sys
import signal
import skillInfo
import shipSkin
import json
import sub as Booru
from DAO import DAO
from discord.ext import commands, tasks
import random
import re

"""***************************************VARIABLE***************************************"""
bot = commands.Bot(command_prefix='n!')

"""***************************************SIGNAL HANDLING***************************************"""


"""***************************************COMMANDE***************************************"""
@bot.event
async def on_ready():
    print(sys.exc_info())
    print('{0} online!'.format(bot.user.name))
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("bully Jules"))

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

@bot.command(name="ship", help="Envoie les informations du personnage demandé\nExemple : n!ship Ise")
async def ship(ctx,ship1=None,ship2=None,ship3=None,ship4=None):
    if ship1 != None:
        await shipInfo.info(ctx,ship1,ship2,ship3,ship4,bot,False)
    else:
        await ctx.send("Format: n!ship <Nom> (Exemple: n!ship Prinz Eugen)")

@bot.command(name="skin")
async def skin(ctx,ship):
    try:
        await shipSkin.getSkin(ctx,ship,bot)
    except:
        print(sys.exc_info())

@bot.command(name="id",help="list pour récuperer la liste des id enregistrer, add pour rajouter son id\n Exemple : n!id -add @Kurosagi 2974398439 Sandy")
async def idAdd(ctx, method="x", pseudo="x", id="x", server="x"):
  if "add" in method:
      if len(pseudo)==1 or len(id)==1 or len(server)==1:
         await ctx.send("Format: n!id add <Pseudo> <Id> <Serveur> (Exemple: n!id @Kurosagi 123456789 Sandy)\n(Utilisez votre tag discord pour le pseudo)")
      elif not "@" in pseudo:
          await ctx.send("Mauvais format de pseudo, utilisez votre tag discord")
      else:
        await al_id.idAdd(ctx,pseudo, id, server)
  elif "list" in method:
    await al_id.idList(ctx, bot)
  else:
      await ctx.send(embed=discord.Embed(description="**Utilisation possible** :\nn!id list : renvoie la liste d'id enregistrée\nn!id add @Pseudo 'ID' 'SERVEUR' : enregistre une nouvelle id"))

@bot.command(name="send")
@commands.has_role('Admirals')
async def sayBot(ctx,channelId,msg):
    await bot.get_channel(int(channelId)).send(msg)
    await discord.Message.delete(ctx.message)

@bot.command(name="build",help="permet d'obtenir la liste des personnages se construisant avec tel temps, Exemple : n!build 01:25:00. -list pour obtenir la liste de tout les temps possible")
async def build(ctx,arg=None):
    if arg != None:
        if arg=="list":
            await buildTime.timeList(ctx,bot)
        elif re.match(r"^\d\d\:\d\d\:\d\d$",arg):
            await buildTime.buildTimer(ctx,arg,bot)
        else:
            await ctx.send("Format: n!build <Timer> (Exemple: n!build 01:25:00)")
    else:
        await ctx.send("Format: n!build <Timer> (Exemple: n!build 01:25:00)")

@bot.command(name="skill",help="retourne la liste des compétences d'un personnage donné")
async def skill(ctx,*arg):
    if arg != ():
        await skillInfo.getSkill(ctx,arg)
    else:
        await ctx.send("Format: n!skill <Nom> (Exemple: n!skill Cleveland)")

@bot.command(name="test")
async def test(ctx,num,*arg):
    try:
        if num=="1":
            await testC.testfield(ctx,arg)
    except:
        print(sys.exc_info())

@bot.command(name="shiplist")
@commands.has_role('Admirals')
async def updatelist(ctx):
        dao=DAO()
        dao.select("ship", ["Name"])
        nameList = [item[0].lower() for item in dao.cursor.fetchall()]
        nameSet=set(nameList)
        with open('../json/shipList.json', 'w', encoding='utf8') as f:
            outlist = json.dumps(list(nameSet))
            f.write(outlist)
        await ctx.send("Liste mise à jour !")

@bot.command(name="fbi")
@commands.has_role('Admirals')
async def fbi(ctx,*arg):
    with open("../json/forbiddenCharacter.json",'r') as f:
        data = f.read()
    datajson = json.loads(data)
    ship=""
    for a in arg:
        ship +=a+" "
    datajson["forbiddenChar"].append(ship[:-1])
    with open("../json/forbiddenCharacter.json",'w') as out:
        json.dump(datajson,out)
    await ctx.send("Ajouté !")

@bot.command(name="sub")
async def sub(ctx, type, *arg):
    await Booru.sub(ctx,type,arg)

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

"""***************************************LOOP***************************************"""
@tasks.loop(minutes=1)
async def booru():
    try:
        await Danbooru.post(bot.get_channel(668493142349316106), bot.get_channel(668428634201260042))
    except:
        print(sys.exc_info())
@booru.before_loop
async def before_booru():
    print("Début de boucle")
    await bot.wait_until_ready()


@booru.after_loop
async def after_booru():
    print("Fin de boucle")



"""***************************************RUN***************************************"""
booru.start()
bot.run("NTMxODIyMjQ4ODkwNDY2MzA2.XqmRtQ.4cVhVgbQ4e5ZRQhP_pflo0G37I8")
