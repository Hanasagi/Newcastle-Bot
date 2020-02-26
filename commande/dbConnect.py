import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from DAO import DAO
import discord

import re
import unicodedata

import requests
from bs4 import BeautifulSoup

async def dbshiplink(ctx):
    dao = DAO()
    getShipName = requests.get("https://azurlane.koumakan.jp/List_of_Ships").text
    nameHtml = BeautifulSoup(getShipName, "html5lib")  # Recupere tout le code html pour récup le nom des ship
    name = nameHtml.select('table[class*="wikitable sortable"] tr td:nth-of-type(2)')
    r = nameHtml.select('table[class*="wikitable sortable"] tr td:nth-of-type(3)')
    nameSet = set(name)
    for n,o in zip(nameSet,r):
        if not "Unreleased" in o.get_text() or "Izumo" in n.get_text():
            mod = n.get_text()
            if re.search(r'[ ]', n.get_text()):
                mod = n.get_text().replace(' ', '_');
            getShipInfo = requests.get("https://azurlane.koumakan.jp/{}".format(mod)).text
            shipHtml = BeautifulSoup(getShipInfo,
                                     "html5lib")  # Recupere tout le code html pour récup les infos des ship
            """***************************************DB ELEMENT***************************************"""
            classe = shipHtml.select('td > a[title*="class"]:first-child')
            if len(classe)<1:
                classe = shipHtml.select('td > a[title*="Type"]:first-child')
            classeURL = shipHtml.select(
                'div#mw-content-text > div.mw-parser-output div > table.wikitable tr:nth-of-type(3) > td > a[href*="class"]')
            if len(classeURL)<1:
                classeURL = shipHtml.select(
                    'div#mw-content-text > div.mw-parser-output div > table.wikitable tr:nth-of-type(3) > td > a[href*="Type"]')
            image = shipHtml.select('div.adaptiveratioimg > a > img')
            imageKai = shipHtml.select('a.image[href*="Kai"] > img')
            build = shipHtml.select('div div div[style*="flex:1"] > table.wikitable tr > td a[href*="Constr"]')
            chibi = shipHtml.select('a[href*="Chibi"] > img')
            chibiKai = shipHtml.select('img[alt*="KaiChibi"]')
            rarete = shipHtml.select(
                'div#mw-content-text > div.mw-parser-output div ~ div > table.wikitable:first-of-type tr ~ tr td[colspan*="2"] a')
            type = shipHtml.select(
                'div#mw-content-text > div.mw-parser-output div ~ div ~ div > table.wikitable:first-of-type tr ~ tr ~ tr td > a ~ a[title*="Cat"]')
            typeKai = shipHtml.select(
                'div#mw-content-text > div.mw-parser-output div ~ div ~ div > table.wikitable:first-of-type tr ~ tr ~ tr td > a ~ a[title*="Cat"]')
            nation = shipHtml.select(
                'div#mw-content-text > div.mw-parser-output div ~ div ~ div > table.wikitable tr ~ tr th[style*="height:"] ~ td > a ~a')
            pixivName = shipHtml.select('a[title*="Artists"]')
            pixivURL = shipHtml.select('.mw-body-content a[href*="pixiv"]')
            if len(pixivURL) > 1:
                artisteURL = pixivURL[0]['href']
            else:
                artisteURL = "Inconnu"
            if len(build) > 0:
                buildTime = build[0].get_text()
            else:
                buildTime = "Inconnu"
            if len(pixivName) > 1:
                artiste = pixivName[0].get_text()
            else:
                artiste = "Inconnu"
            if len(imageKai) > 0:
                typeKaiS = type[0].get_text()
            if mod == "Fusou" or mod == "Yamashiro" or mod == "Ise" or mod == "Hyuuga":
                typeKaiS = "Aviation Battleship"
                typeS="Battleship"
            if len(type) < 1:
                print(mod)
                break
            typeS=type[0].get_text()

            if len(chibi)>1:
                chibi = chibi[0]['src']
                chibiKai= chibiKai[0]['src']
            else:
                chibi="None"
                chibiKai="None"

            """***************************************""""""""""***************************************"""
            try:
                dao.insert("ship",["Name", "Classe","Image","Chibi","BuildTime","Rarity","Type","Nation","Pixiv","PixivURL","ClasseURL"],
                         [mod, classe[0].get_text(),image[0]['src'], chibi, buildTime, rarete[0]['title'],typeS,nation[0].get_text(),artiste,artisteURL,classeURL[0]['href']])
                if len(imageKai)>0:
                   dao.insert("ship", ["Name", "Classe", "Image", "Chibi", "BuildTime", "Rarity", "Type", "Nation", "Pixiv","PixivURL", "ClasseURL","ImageKai","ChibiKai","TypeKai"],
                              [mod, classe[0].get_text(),image[0]['src'], chibi, buildTime, rarete[0]['title'],typeS,nation[0].get_text(),artiste,artisteURL,classeURL[0]['href'],imageKai[0]['src'],chibiKai,typeKaiS])
            except IndexError:
                 await ctx.send("Erreur")
    dao.close()

async def dbskillset(ctx):
    dao = DAO()
    getShipName = requests.get("https://azurlane.koumakan.jp/List_of_Ships_with_Skills").text
    skillHtml = BeautifulSoup(getShipName, "html5lib")  # Recupere tout le code html pour récup le nom des ship
    name = skillHtml.select('table.wikitable td:nth-of-type(1) div+div a')
    skill1=skillHtml.select('table.wikitable td:nth-of-type(4)')
    skill2 = skillHtml.select('table.wikitable td:nth-of-type(5)')
    skill3 = skillHtml.select('table.wikitable td:nth-of-type(6)')
    skill4 = skillHtml.select('table.wikitable td:nth-of-type(7)')
    skill5 = skillHtml.select('table.wikitable td:nth-of-type(8)')
    for a,x,j,k,l,m in zip(name,skill1,skill2,skill3,skill4,skill5):
        skillList=[]
        skillList.append(a["title"])
        if not x.find("i"):
            skillList.append("None")
            skillList.append("None")
        else:
            skillList.append(x.div.i.get_text())
            skillList.append(x.div.next_sibling.div.next_sibling.get_text())
        if not j.find("i"):
            skillList.append("None")
            skillList.append("None")
        else:
            skillList.append(j.div.i.get_text())
            skillList.append(j.div.next_sibling.div.next_sibling.get_text())
        if not k.find("i"):
            skillList.append("None")
            skillList.append("None")
        else:
            skillList.append(k.div.i.get_text())
            skillList.append(k.div.next_sibling.div.next_sibling.get_text())
        if not l.find("i"):
            skillList.append("None")
            skillList.append("None")
        else:
            skillList.append(l.div.i.get_text())
            skillList.append(l.div.next_sibling.div.next_sibling.get_text())
        if not m.find("i"):
            skillList.append("None")
            skillList.append("None")
        else:
            skillList.append(m.div.i.get_text())
            skillList.append(m.div.next_sibling.div.next_sibling.get_text())
        try:
                dao.insert("skill",
                            ["Name","Skill1Name", "Skill1Desc", "Skill2Name", "Skill2Desc","Skill3Name", "Skill3Desc","Skill4Name", "Skill4Desc","Skill5Name", "Skill5Desc"],skillList)
        except IndexError:
            await ctx.send("Erreur")
        except mysql.connector.errors.DataError:
            print(skillList)
