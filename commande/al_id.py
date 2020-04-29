import discord
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from DAO import DAO


async def idList(ctx, bot):
    dao = DAO()
    embed = discord.Embed(title="Liste d'ID")
    dao.select("id",["pseudal","id","serveur"])
    result = dao.cursor.fetchall()
    for row in result:
        user = bot.get_user(int(row[0][3:-1]))
        value="Id : "+str(row[1])+" Serveur : "+row[2]
        embed.add_field(name=user,value=value,inline=True)
    await ctx.send(embed=embed)

async def idAdd(ctx, pseudo, pid, pserver):
    dao = DAO()
    servList=("Sandy","Lexington","Washington","Avrora")
    if any(serv in pserver.capitalize() for serv in servList):
        dao.insert("id",["pseudal","id","serveur"],[pseudo,pid,pserver.capitalize()])
        await ctx.send("Id ajouté ! ")
    else:
        await ctx.send("Serveur inexistant")
