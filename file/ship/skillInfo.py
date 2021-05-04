from DAO import DAO
import discord
import asyncio
import difflib
import json

async def getSkill(ctx,ship):
    with open('../json/shipList.json', 'r', encoding='utf8') as input:
        data = input.read()
    nameList = json.loads(data)
    shipName = ship.rstrip().replace(' ', '_').title()
    if not shipName.lower() in nameList:
        simili = difflib.get_close_matches(shipName, set(nameList))
        embedName = discord.Embed()
        sName = "**Correction possible**\n"
        for i in simili:
            sName += i.replace('_', ' ').title() + "\n"
        if (len(sName) > 24):
            embedName.description = sName
            await ctx.send(embed=embedName)
        else:
            await ctx.send("Format: n!build <Timer> (Exemple: n!build 01:25:00)")
    else:
        dao = DAO()
        dao.select("skill",["Skill1Name","Skill1Desc","Skill2Name","Skill2Desc","Skill3Name","Skill3Desc","Skill4Name","Skill4Desc","Skill5Name","Skill5Desc"],"Name",shipName)
        result = dao.cursor.fetchall()
        for row in result:
            skill1Name = row[0]
            skill1Desc = row[1]
            skill2Name = row[2]
            skill2Desc = row[3]
            skill3Name = row[4]
            skill3Desc = row[5]
            skill4Name = row[6]
            skill4Desc = row[7]
            skill5Name = row[8]
            skill5Desc = row[9]
        embed = discord.Embed(title=shipName)
        if skill1Name != "None":
            embed.add_field(name=skill1Name, value=skill1Desc, inline=False)
        if skill2Name != "None":
            embed.add_field(name=skill2Name, value=skill2Desc, inline=False)
        if skill3Name != "None":
            embed.add_field(name=skill3Name, value=skill3Desc, inline=False)
        if skill4Name != "None":
            embed.add_field(name=skill4Name, value=skill4Desc, inline=False)
        if skill5Name != "None":
            embed.add_field(name=skill5Name, value=skill5Desc, inline=False)
        dao.close()
        await ctx.send(embed=embed)