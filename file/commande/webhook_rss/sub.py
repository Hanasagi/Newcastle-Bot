import json
import discord
import os


async def sub(ctx, type, arg, db):
    alreadypresent = False
    dbName = "danbooru_list_" + str(ctx.guild.id)

    db.select(dbName, ["*"], "name", str(ctx.author.id))
    userlist = db.cursor.fetchall()
    print(userlist)
    if userlist != []:
        list = json.loads(userlist[0][2])

    if "add" in type:
        charlistpresent = ""
        if userlist != []:
            alreadypresent = True
            for a in arg:
                a = a.strip()
                if not a.lower() == "":
                    if not a.lower() in list:
                        list.append(a.lower().strip())
                    else:
                        charlistpresent += " " + a.title() + ","
            db.update(dbName, ["charlist"], ["'" + json.dumps(list) + "'"], "name", str(ctx.author.id))
        if len(charlistpresent) > 1:
            await ctx.send(
                charlistpresent[:-1] + " seems to be already on your list. Is your memory really that short ?")
        if not alreadypresent:
            charlist = []
            for a in arg:
                charlist.append(a.lower().strip())
            db.insert(dbName, ["name", "nsfw", "charlist"], [str(ctx.author.id), "yes", json.dumps(charlist)])

        if len(charlistpresent) < 1:
            await ctx.send(
                "I added them all to your list, the more, the merrier, as they say.")

    elif "remove" in type:
        notpresent = False
        present = False
        charpresent = ""
        charnotpresent = ""
        if userlist != []:
            for a in arg:
                a = a.strip()
                if a.lower() in list:
                    present = True
                    charpresent += a.title() + ","
                    if len(list) <= 1:
                        db.delete(dbName, "name", str(ctx.author.id))
                    else:
                        list.remove(a.lower())
                else:
                    notpresent = True
                    charnotpresent += " " + a.title() + ","
        if present:
            await ctx.send("I removed them from your list. May I know the reason ?")
        db.update(dbName, ["charlist"], ["'" + json.dumps(list) + "'"], "name", str(ctx.author.id))

        if notpresent:
            await ctx.send("These one were not on your list : " + charnotpresent[
                                                                  :-1] + ". How come you made such a simple mistake, perhaps you need to get some sleep ?")

    elif "list" in type:
        listispresent = False
        charlist = ''
        if userlist != []:
            listispresent = True
            for char in list:
                charlist += " " + char.title() + ","

        if listispresent:
            try:
                await ctx.author.send("Here is your list, commander :\n" + charlist[:-1])
            except discord.errors.Forbidden:
                await ctx.send("Here is your list, commander :\n" + charlist[:-1])

        else:
            await ctx.send("Your list is empty. Want me to help you create one ?")

    elif "nsfw" in type:
        if userlist != []:
            if "y" in arg:
                db.update(dbName, ["nsfw"], ["yes"], "name", str(ctx.author.id))
            elif "n" in arg:
                db.update(dbName, ["nsfw"], ["no"], "name", str(ctx.author.id))
    if "y" in arg:
        await ctx.send(
            "You will now be notified when someone from your list appear in #nsfw-al-danbooru")
    elif "n" in arg:
        await ctx.send(
            "You will now never be notified when someone from your list appear in #nsfw-al-danbooru")
    elif "purge" in type:
        if userlist != []:
            db.delete(dbName, "name", str(ctx.author.id))

        await ctx.send("I throw your list in the bin. Make sure to not regret that later.")
    elif "search" in type:
        if len(arg) > 1:
            await ctx.send("Please request one character at a time, i need time to process your request.")
            return
        followList = ""
        db.select(dbName, ["charlist"], "charlist", "JSON_CONTAINS('charlist," + str(arg) + ",$)")
        print(db.cursor.fetchall())
        """for data in data_list['data']:
            for a in arg:
                if a.lower() in data["charlist"]:
                    followList += " " + "<@!" + str(data["name"]) + ">,"
        embed = discord.Embed()
        if (len(followList) < 1):
            embed.description = "She is on nobody list. Maybe you could consider adding her to yours ?"
        else:
            embed.title = "She is on the list of these people : "
            embed.description = followList[:-1]
        await ctx.send(embed=embed)"""
    elif "clear" in type:
        role = discord.utils.find(lambda r: r.name == 'Admirals', ctx.message.guild.roles)
        if role in ctx.author.roles:
            for data in data_list["data"]:
                if ctx.message.guild.get_member(data["name"]) is None:
                    data_list['data'].remove(data)
            await ctx.send("Purge fini")
        else:
            print("You do not have the right for that. Maybe try asking the higher ups for permissions ?")
