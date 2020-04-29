import json
import discord

async def sub(ctx,type,arg):
    alreadypresent = False
    with open("../json/SubBooru.json", "r") as input:
        data = input.read()
    data_list = json.loads(data)

    if "-a" in type:
        charlistpresent = ""
        for data in data_list['data']:
            if str(ctx.author.id) in str(data["name"]):
                alreadypresent = True
                for a in arg:
                    if not a.lower() in data["charlist"]:
                        data["charlist"].append(a.lower().strip())
                    else:
                        charlistpresent += " " + a.title() + ","
        if len(charlistpresent) > 1:
            await ctx.send(charlistpresent[:-1] + " déjà présent")
        if not alreadypresent:
            charlist = []
            for a in arg:
                charlist.append(a.lower().strip())
            data_list['data'].append({"name": ctx.author.id, "nsfw":"yes", "charlist": charlist})

        with open("../json/SubBooru.json", "w") as out:
            json.dump(data_list, out)
        if len(charlistpresent) < 1:
            await ctx.send("Ajouté!")

    elif "-r" in type:
        notpresent = False
        present = False
        charpresent = ""
        charnotpresent = ""
        for data in data_list['data']:
            if str(ctx.author.id) in str(data["name"]):
                for a in arg:
                    if a.lower() in data["charlist"]:
                        present = True
                        charpresent += a.title() + ","
                        if len(data["charlist"]) <= 1:
                            data_list['data'].remove(data)
                        else:
                            data["charlist"].remove(a.lower())
                    else:
                        notpresent = True
                        charnotpresent += " " + a.title() + ","
        if present:
            await ctx.send(charpresent[:-1] + " supprimé de ta liste")
        with open("../json/SubBooru.json", "w") as out:
            json.dump(data_list, out)

        if notpresent:
            await ctx.send("Personnage introuvable :" + charnotpresent[:-1])
    elif "-l" in type:
        listispresent = False
        charlist = ''
        for data in data_list['data']:
            if str(ctx.author.id) in str(data["name"]):
                listispresent = True
                for char in data["charlist"]:
                    charlist += " " + char.title() + ","

        if listispresent:
            await ctx.send("Voici ta liste :" + charlist[:-1])
        else:
            await ctx.send("Tu n'as aucun suivi !")
    elif "-nsfw" in type:
        for data in data_list['data']:
            if str(ctx.author.id) in str(data["name"]):
                if "y" in arg:
                    data["nsfw"]="yes"
                elif "n" in arg:
                    data["nsfw"]="no"
        if "y" in arg:
            await ctx.send("Tu seras maintenant prévenu lors d'une apparition d'un personnage de ta liste dans #nsfw-al-danbooru")
        elif "n" in arg:
            await ctx.send(
                "Tu ne seras maintenant plus prévenu lors d'une apparition d'un personnage de ta liste dans #nsfw-al-danbooru")
    elif "-purge" in type:
        for data in data_list['data']:
            if str(ctx.author.id) in str(data["name"]):
                data_list['data'].remove(data)
                break
        await ctx.send("Liste supprimé !")
    elif "-s" in type:
        if len(arg)>1:
            await ctx.send("Un personnage a la fois !")
            return
        followList=""
        for data in data_list['data']:
            for a in arg:
                if a.lower() in data["charlist"]:
                    followList+=" "+"<@!"+str(data["name"])+">,"
        embed=discord.Embed()
        if(len(followList)<1):
            embed.description="Personne ne suit ce personnage"
        else:
            embed.title="Suivi par : "
            embed.description=followList[:-1]
        await ctx.send(embed=embed)
    with open("../json/SubBooru.json", "w") as out:
        json.dump(data_list, out)