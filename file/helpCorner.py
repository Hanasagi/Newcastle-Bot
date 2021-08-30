# coding=utf-8
import discord
import os

json_help = {
    "commande": [
        {
            "name": "build",
            "desc": discord.Embed(title='Commande : Build',
                                  description='Utilisation : **n!build [timer]**\nRenvoie une liste de personnages qui se construise avec le timer demandé.\nExemple :'),
            "image": "https://puu.sh/FWf9N/b89f19c42d.png"
        },
        {
            "name": "ship",
            "desc": discord.Embed(title='Commande : Ship',
                                  description="Utilisation : **n!ship [nom]**\nRenvoie des informations sur le personnage demandé, avec son artwork (si il existe, permet de voir son artwork Retrofit).\nExemple :"),
            "image": "https://puu.sh/FWhTE/5d7993e32c.png"
        },
        {
            "name": "skin",
            "desc": discord.Embed(title='Commande : Skin',
                                  description="Utilisation : **n!skin [nom]**\nPermet de visualiser tous les skins d'un personnage (en comptant son artwork de base et retrofit, s'il existe)\nExemple :"),
            "image": "https://puu.sh/FWivQ/9934bdd552.png"
        },
        {
            "name": "sub",
            "desc": discord.Embed(title='Commande : Sub',
                                  description="Cette commande permet de suivre un ou des personnages et de se faire ping lorsqu'une image apparaît dans le salon #images-al-danbooru et #nsfw-al-danbooru si vous possédez le rôle nsfw, et a cinq utilisations :\nLa première : add,\nqui permet d'ajouter un ou plusieurs personnages a suivre\nUtilisation : **n!sub add [nomX]**\n/!\ Chaque personnage doit être séparé par une virgule pour que cela fonctionne correctement.\nIl est aussi possible de rajouter autant de personnages qu'on veut dans la commande"
                                              "\n\nLa deuxième : remove,\npour supprimer un ou plusieurs personnages. même chose qu'avant, les personnages doivent être séparé par des virgules.\nUtillisation : **n!sub remove [nomX]**"
                                              "\n\nLa troisième : list,\npour afficher la liste des personnages que l'ont suit\nUtilisation : **n!sub list**"
                                              "\n\nLa quatrième : purge,\nelle supprime toute votre liste de suivi d'un seul coup\nUtilisation : **n!sub purge**"
                                              "\n\nEt enfin, la dernière : nsfw,\nElle permet de désactiver (ou activer) les tag dans le salon #nsfw-al-danbooru\nUtilisation :\n**n!sub nsfw y** (pour activer les tags)\nou\n**n!sub nsfw n** (pour désactiver les tags)"),
            "image": ""
        },
        {
            "name": "stat",
            "desc": discord.Embed(title='Commande : Stat',
                                  description="Cette commander permet d'afficher les différentes statistiques d'un personnage.\n"
                                              "Vous pouvez afficher les statistiques de base, de niveau 100 et 120, et retrofit si disponible."
                                              "\n**/!\\\** Si vous voulez savoir les statistiques d'un personnage avec un nom composé (exemple, Prince of Wales), mettez bien le nom entre guillemets, sinon ça ne marchera pas."
                                              "\n\nUtilisation :\n\nStat basique : **n!stat [nom]**\nStat level 100/120 : **n!stat [nom] [level]**\nStat level 100/120 Retrofit : **n!stat [nom] [level]r**\n\nExemple :"),
            "image": "https://puu.sh/G2PMq/359121bf6d.png"
        }
    ]
}


async def help(ctx, options=""):
    if (options == ""):
        embed = discord.Embed(title="Help Corner")
        i = 1
        desc = "Commande disponible :\n\n"
        for data in json_help["commande"]:
            desc += str(i) + ". " + data["name"] + "\n"
            i += 1
        desc += "\n**n!help [commande]** pour obtenir plus de détails sur cette dernière"
        embed.description = desc
        await ctx.send(embed=embed)
    else:
        commandFound = False
        for data in json_help["commande"]:
            if data["name"] == options.lower():
                commandFound = True
                data["desc"].set_image(url=data["image"])
                await ctx.send(embed=data["desc"])
        if not commandFound:
            await ctx.send("Cette commande n'existe pas.")
