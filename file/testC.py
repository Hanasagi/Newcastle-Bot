import discord
import asyncio
import tweepy
from bs4 import BeautifulSoup
import requests
import json
import traceback
from CRUD import CRUD
from azurlane.azurapi import AzurAPI
import requests  # dependency
from twython import TwythonStreamer
import json
from CRUD import CRUD
from credentials import Creds
from random import randint

embed1 = {
        "embeds":[{
                "description": '/!\ Comprenez que vous êtes sur un serveur communautaire. Nous acceptons tout nouvel arrivant, mais celui-ci doit aussi comprendre que nous avons nos habitudes et discussions entre actifs, et qu’il peut souvent être compliqué de participer sur l’instant. Prenez le train en marche, présentez-vous et réagissez si vous le voulez, nous sommes ici pour nous détendre et rigolons de tout. Si vous avez besoin d’aide, nous sommes parfaitement disposés à vous la fournir dans le channel dédié #al_aide, où nous essayons de véhiculer la meilleure aide possible sans “troller”.'
        +"\n\n- Tout message à caractère discriminatoire, violent, xénophobe, haineux n'est pas autorisé et sera sévèrement puni (on accepte les blagues bien sur, là n'est pas le souci, mais si nous remarquons que cela devient vraiment répétitif nous sévirons)."
             +"\n\n- Le harcèlement que ce soit en MP ou ici sera aussi puni et sans avertissement. De même, si vous-même pensez subir un harcèlement, contactez un modérateur pour vous aider à régler la situation."
             +"\n\n- La publicité, quelle qu'elle soit, est formellement interdite en MP, si des gens vous contactent, informez-en la modération. Si vous souhaitez cependant poster des projets originaux à vous, n'hésitez pas à nous demander, nous sommes très ouverts à cela. Pour tout ce qui est dessins personnels, vous pouvez poster cela dans #vos-creations tant que cela n’est pas NSFW (A ce moment, cela passe par les channels dédiés, soumis aux mêmes règles que ces derniers)."
             +"\n\n- Un français correct et compréhensible est obligatoire, nous ne sommes pas en cours de français, nous vous rassurons, mais essayez un maximum de rendre vos messages lisibles et compréhensible."
              +"\n\n- Divulguer des informations personnelles d’une tierce personne est interdit. Et nous ne vous conseillons par ailleurs de ne pas divulguer les vôtres (A vos risques et périls)."
             }]
}
embed11 = {
"embeds":[{
                "description": "- Les provocations et insultes seront évidemment réprimandées, un petit “ntm” pas de soucis, mais si cela devient répétitif nous n’hésiterons pas à sévir. "
+"\n\n- Le \"spam\" n'est pas autorisé et pourra être puni. De plus, tout message visant à créer une mauvaise ambiance générale seront, eux aussi, puni. Tombe dans cette dernière catégorie tout format multimédia porteur de cette même intention (par exemple les vidéos faisant crasher les clients discord)."
+"\n\n- Pour spoiler utilisez les balises \"\|| le spoil \||\" qui sont présente pour ça, et faites-le dans les channels concernés par ce que vous souhaitez partager. Dans les channels plus généraux, merci d’indiquer la source de ce que vous mettez en spoiler (comme le nom de l’animé ou le jeu en question), afin que les personnes qui ne veulent pas connaitre cette information puisse l’éviter tout en profitant des informations qu’elles jugeront moins sensible."
+"\n\n- Veuillez posséder un pseudo pingable, si votre pseudo de base n'est pas pingable, ajoutez-vous un surnom ici pour qu'on puisse vous ping, ou inversement, si votre surnom n'est pas pingable, faites que votre pseudo discord de base soit pingable lui. Si toutefois vous ne respectez pas cette règle nous n'hésiterons pas à vous mettre un rôle empêchant de vous renommer, et nous mettrons nous même un pseudonyme."
+"\n\n- Si vous avez déjà été banni une fois du serveur, ne demandez pas à revenir, si vous avez été banni, ce n'est pas pour rien, nous ne débannerons pas.Si toutefois nous voyons quelqu'un de banni revenir avec un compte secondaire, nous n'hésiterons pas à bannir ce compte une nouvelle fois."
 }]
}
embed2 = {
        "fields":[{
                "titre":"Informations générales sur les channels",
                "desc":"Pour la plupart des channels, une description a été mise, veillez à la respecter un maximum, faire des hors-sujets arrive à tout le monde, mais si c'est constamment, vous aurez le droit à plusieurs avertissements, suivi de punitions. Bien entendu, si vous avez des doutes sur où poster quelque chose, n'hésitez pas à demander à la modération ou aux actifs."
        },
{
                "titre":"Catégorie Importants",
                "desc":"Ces channels sont là pour vous donner les règles à suivre sur le serveur, ainsi que les différents rôles disponibles en self-service."
        },
{
                "titre":"Catégorie Nouveautés",
                "desc":"Ils représentent les nouveautés en rapport avec le jeu, le bot de Kurosagi (Newcastle Sensei), ainsi que les nouveautés en rapport avec le serveur."
        },
{
                "titre":"Channels principaux",
                "desc":"Ces derniers représentent principalement les channels qui ont un rapport avec Azur lane de manière générale."
        },
{
                "titre":"Channels secondaires",
                "desc":"Ils sont ici pour les sujets qui ne représentent pas l'essence même du serveur"
        },
{
                "titre":"Multimédias",
                "desc":"\n\nIls sont surtout composés des channels d’images. Nous avons pour chaque catégorie un channel SFW (safe for work), et un channel NSFW (not safe for work), RESPECTEZ IMPÉRATIVEMENT CEUX-CI, si vous vous posez la question de si une image est NSFW ou non, c'est qu'elle l'est. Si toutefois vous avez tout de même un doute, n'hésitez pas à demander a la modération, ou tout simplement à poster dans un salon NSFW, il vaut mieux avoir des images SFW dans un salon NSFW que l'inverse."
         +"\n\nDe plus, ils sont divisés de telle manière : "
             +"\n\n- Les salons images et NSFW sont là pour les images n'ayant pas de rapport avec Azur lane (ça peut aller d'une photo de votre jardin, à un personnage de Monogatari, en passant par une image d'Helltaker)."
             +"\n\n- Les salons #images-al et #nsfw-al sont là pour les images ayant un rapport avec Azur lane, de près ou de loin. Lorsque vous postez une image, faites attention à ce qu'elle n'ait pas été postée dans les dernières minutes dans les salons danbooru."
                   },
        ]
}
embed22 = {
        "fields":[{
                "titre":"Multimédias - suite",
                "desc":  '\n\n- Enfin, les salons images-al-danbooru et nsfw-al-danbooru sont des salons dans lesquels le bot de Kurosagi poste les images récupéré du site Danbooru, il est possible de "s\'abonner "au bot si vous souhaitez être mentionné dès que le bot poste vos personnages préférés (n!help pour consulter l\'aide du bot)'
                +"\n\nSi vous souhaitez accéder aux salons NSFW (qui sont cachés de base) il vous suffit de taper \"!nsfw\" dans le salon #bot, si toutefois vous souhaitez ne plus avoir accès aux salons NSFW, nous pouvons vous retirez le rôle."
                +"\n\nDe plus, dans les salons NSFW, il est interdit de poster tout ce qui va être underage ou d'apparence (peu importe l'âge), nous jugerons exclusivement sur le physique et cela sera selon notre ressenti. Si vous n'êtes pas d'accord cela ne changera rien à notre décision. En outre, tout ce qui est viol, torture, et autre images hardcore / illégales sont aussi interdite et passable de punition à commencer par des avertissements sévères et si besoin un ban."
        },
{
                "titre":"Autres-jeux et Voice Channels",
                "desc":"Ils sont présents pour échanger sur les jeux-vidéos, jouer ensemble, discuter, etc… Si nous observons beaucoup d’activité pour un jeu précis dans le salon global de cette sous-section (#autres-jeux), vous pouvez nous le signaler pour créer un salon dédié si nous le jugeons utile. Ces derniers pourront aussi disparaitre dès lors que l’activité n’est plus suffisante."
        },
        ]
}
embed3 = {
        "fields":[{
                "titre":"Admirals",
                "desc":"Ce sont les administrateurs du serveur, ils possèdent tous les droits sur le serveur, j'ai une confiance absolue en eux, si toutefois vous êtes puni par l'un d'entre eux, la faute vous reviendra, je fais confiance en leur jugement."
        },
                {
                        "titre": "Police d'Images",
                        "desc": "Ils sont là au départ pour veiller à ce que les images postées par le bot et les utilisateurs se trouvent dans les bons channels. Néanmoins, ils font partie du staff et ont aussi un rôle de modérateurs, j'ai aussi confiance en leur jugement, si vous êtes punis par l'un d'entre eux, c'est que vous l'aurez sûrement mérité."
                },
{
                "titre":"Rôle de nation",
                "desc":"Chaque nation présente dans le jeu a le droit à un rôle, ils sont tous cumulables (attrapez les tous), mais si vous souhaitez porter la couleur qui correspond à votre nation préférée, vous en avez la possibilité ! Pour cela, rendez-vous dans #nations et ajoutez une réaction au bot \"carl-bot\" pour qu'il vous ajoute le rôle."
        },
        ]
}
async def testfield(ctx, arg1, arg2):
        db = CRUD()
        print(ctx.guild.id)
        db.insert("guild",["uid","name","options"],[str(ctx.guild.id),ctx.guild.name,1],)
        """welcome_img = discord.File("../image/img_placeholder.png", filename="embedimg.png")
        img_1 = discord.File("../image/1.png", filename="titre1.png")
        img_2 = discord.File("../image/2.png", filename="titre2.png")
        img_3 = discord.File("../image/3.png", filename="titre3.png")
        embed_img=discord.Embed(color=0xD8661e)
        embed_img.set_image(url="attachment://embedimg.png")
        embed_titre1 = discord.Embed(color=0xBa0309)
        embed_titre1.set_image(url="attachment://titre1.png")
        embed_titre2 = discord.Embed(color=0x0390ba)
        embed_titre2.set_image(url="attachment://titre2.png")
        embed_titre3 = discord.Embed(color=0x7d03ba)
        embed_titre3.set_image(url="attachment://titre3.png")

        embed_1=discord.Embed(description=embed1["embeds"][0]["description"],color=0xBa0309)
        embed_11 = discord.Embed(description=embed11["embeds"][0]["description"],color=0xBa0309)
        embed_2=discord.Embed(color=0x0390ba)
        for el in embed2["fields"]:
                embed_2.add_field(name=el["titre"],value=el["desc"],inline=False)
        embed_22 = discord.Embed(color=0x0390ba)
        for el in embed22["fields"]:
                embed_22.add_field(name=el["titre"], value=el["desc"], inline=False)
        embed_3 = discord.Embed(color=0x7d03ba)
        for el in embed3["fields"]:
                embed_3.add_field(name=el["titre"], value=el["desc"], inline=False)
        await ctx.send(file=welcome_img, embed=embed_img)
        await ctx.send(file=img_1, embed=embed_titre1)
        await ctx.send(embed=embed_1)
        await ctx.send(embed=embed_11)
        await ctx.send(file=img_2, embed=embed_titre2)
        await ctx.send(embed=embed_2)
        await ctx.send(embed=embed_22)
        await ctx.send(file=img_3, embed=embed_titre3,)
        await ctx.send(embed=embed_3)

async def test2(ctx,arg):
        if ctx.message.guild.get_member(arg) is None:
            print("a")
        else:
            print("b")"""
