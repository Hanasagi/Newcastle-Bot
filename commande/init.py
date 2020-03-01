"""***************************************IMPORT***************************************"""
import discord
import dbConnect
import time
import buildTime
import Danbooru
import al_id
import shipInfo
import testC
import skillInfo
from DAO import DAO
from discord.ext import commands, tasks
import random
import re

"""***************************************VARIABLE***************************************"""
bot = commands.Bot(command_prefix='n!')

"""***************************************COMMANDE***************************************"""
@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user.name))
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("bully Jules"))

def is_admin():
    async def predicate(ctx):
            return ctx.author.roles and ctx.author.roles.has
    return commands.check(predicate)

@bot.command(name="dbshipset")
@commands.has_role("Bot Master")
async def dbShipupdate(message):
    await dbConnect.dbshiplink(message);

@bot.command(name="dbskillset")
@commands.has_role("Bot Master")
async def dbSkillupdate(message):
    await dbConnect.dbskillset(message);

@bot.command(name="ship", help="Envoie les informations du personnage demandé\nExemple : n!ship Ise")
async def ship(ctx,ship1=None,ship2=None,ship3=None,ship4=None):
    if ship1 != None:
        await shipInfo.info(ctx,ship1,ship2,ship3,ship4,bot,False)
    else:
        await ctx.send("Format: n!ship <Nom> (Exemple: n!ship Prinz Eugen)")

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
@commands.has_role('Admirals')
async def test(ctx):
    await testC.chibre(ctx)

@bot.command(name="shiplist")
@commands.has_role('Admirals')
async def updatelist(ctx):
    try:
        dao=DAO()
        dao.select("ship", ["Name"])
        nameList = [item[0].lower() for item in dao.cursor.fetchall()]
        nameSet=set(nameList)
        with open('shipNameList.txt', 'a+', encoding='utf8') as f:
            for n in nameSet:
                f.write(str(n)+"\n")
        await ctx.send("Liste mise à jour !")
    except:
        await ctx.send("Tu n'as pas les droits")

@updatelist.error
@test.error
@dbSkillupdate.error
@dbShipupdate.error
async def error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Tu n'as pas les droits !")
"""***************************************LOOP***************************************"""
@tasks.loop(minutes=1)
async def example():
    await Danbooru.post(bot.get_channel(668493142349316106), bot.get_channel(668428634201260042))

@example.before_loop
async def before_example():
    print("Début de boucle")
    await bot.wait_until_ready()


@example.after_loop
async def after_example():
    print("Fin de boucle")



"""***************************************RUN***************************************"""
example.start()
bot.run("")
