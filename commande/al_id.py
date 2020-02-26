import discord
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

async def idList(ctx, bot):
    embed = discord.Embed(title="Liste d'ID")
    cursor.execute("SELECT pseudal, id, serveur FROM id")
    for (pseudal, id, serveur) in cursor:
        user = bot.get_user(int(pseudal[3:-1]))
        value="Id : "+str(id)+" Serveur : "+serveur
        embed.add_field(name=user,value=value,inline=True)
    cursor.close()
    connection.close()
    await ctx.send(embed=embed)

async def idAdd(ctx, pseudo, pid, pserver):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             user='root',
                                             database='alship',
                                             password='')

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor(buffered=True)  # buffered=True évite l'overflow (de ce que j'ai compris)
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        else:
            print(err)
    servList=("Sandy","Lexington","Washington","Avrora")
    if any(serv in pserver.capitalize() for serv in servList):
        cursor.execute("INSERT INTO id(pseudal, id, serveur) VALUES(%s,%s,%s)", (pseudo, pid, pserver.capitalize()))
        await ctx.send("Id ajouté ! ")
    else:
        await ctx.send("Serveur inexistant")
    cursor.close()
    connection.close()
