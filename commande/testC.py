import discord
import asyncio
from bs4 import BeautifulSoup
import requests
from DAO import DAO

async def chibre(ctx,arg):
    try:
        shipName=''
        if(len(arg)>1):
            for a in arg:
                shipName+=a+" "
        else:
            shipName=arg[0]
        shipName=shipName.rstrip().lower()
        print(shipName)
        namelist = []
        sublist = []
        with open("SubBooru") as f:
            for cnt, line in enumerate(f):
                name = line[0:line.index(":")]
                ship = line[line.index(":")+1:len(line)].replace("\n","").lower()
                print(name)
                shipList = ship.split(",")
                namelist.append(name)
                sublist.append(shipList)
        print(sublist)
        nameList=''
        for i,j in zip(namelist,sublist):
           print(j)
           if any(a in shipName for a in j):
               nameList+="<@!"+i + "> "
        await ctx.send(nameList)
        await ctx.send("Test fast, fail fast, adjust fast.")
    except:
        print("An exception occurred")


async def sub(ctx,arg):
    alreadypresent = False
    with open("SubBooru","a+") as f:
        for cnt, line in enumerate(f):
            if str(ctx.author.id) in line:
                line = line+arg
            """
    try:
        shipList=""
        for a in arg:
            shipList+=a+","
        shipList=shipList[:-1]
        with open('SubBooru', 'a+', encoding='utf8') as f:
                f.write(str(ctx.author.id) + ":" + str(shipList) + "\n")
        await ctx.send("Ajouté!")
    except:
        print("c raté")
        
with open('f1.txt', 'r') as f:
    lines = []
    for line in f:
        if line.startswith("line 3:"):
            split_line = line.split()
            split_line.insert(split_line.index("3:"), "NAME")
            lines.append(' '.join(split_line) + '\n')
        else:
            lines.append(line)
with open('f2.txt', 'w') as f:
    for line in lines:
        f.write(line)
"""