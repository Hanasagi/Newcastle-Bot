from PIL import Image, ImageDraw, ImageFont, ImageOps
import discord
import os
import requests
from io import BytesIO

async def welcome(member):
    W, H = (1000, 500)
    img = Image.open("../image/background.png")
    imdraw = ImageDraw.Draw(img)
    response = requests.get(member.avatar_url)
    img_avatar = Image.open(BytesIO(response.content)).convert('RGBA')
    img_avatar = img_avatar.resize((300,300), Image.ANTIALIAS)


    mask = Image.new('L',(img_avatar.size[0]*3,img_avatar.size[1]*3),0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse((0, 0) + (img_avatar.size[0]*3,img_avatar.size[1]*3), fill=255)
    mask = mask.resize(img_avatar.size, Image.ANTIALIAS)
    img_avatar.putalpha(mask)
    msg="Bienvenue à bord, Commandant " + member.display_name + " !"

    w_text, h_text = imdraw.textsize(msg, font=ImageFont.truetype("Montserrat-Regular.ttf", 35))
    text_offset = ((W - w_text) // 2, (H-h_text)-30)
    w_avatar,h_avatar = img_avatar.size
    img_offset = ((W - w_avatar) // 2, (H - h_avatar) // 4)

    #imdraw.ellipse(((W-w_avatar)//2, (H-h_avatar)// 2, (W+w_avatar)//2, (H+h_avatar)//4), fill=(255,255,255))
    img.paste(img_avatar, img_offset, img_avatar)
    if w_text > W:
        msg = msg.split(',')
        new_h=70
        for i in range(len(msg)):
            print(i)
            w_text, h_text = imdraw.textsize(msg[i], font=ImageFont.truetype("Montserrat-Regular.ttf", 35))
            new_text_offset = ((W - w_text) // 2, (H - h_text) - new_h)
            imdraw.text(new_text_offset, msg[i], (255, 255, 255), font=ImageFont.truetype("Montserrat-Regular.ttf", 35))
            new_h=--10
    else:
        imdraw.text(text_offset, msg, (255, 255, 255), font=ImageFont.truetype("Montserrat-Regular.ttf", 35))
    img.save("../image/img_placeholder.png")

    welcome_img = discord.File("../image/img_placeholder.png", filename="embedimg.png")
    await member.send(file=welcome_img)
    await member.send(content="Je vous invite à lire le règlement dans le canal #bienvenue, puis une fois ceci fait, à vous orienter vers le canal #nations.\nBonne continuation.")

