#!/usr/bin/env pypy

import os
import discord
from bs4 import BeautifulSoup
from google_trans_new import google_translator
import requests

client = discord.Client()

GUILD = client.get_guild(id)


def tb_scanner(link, author):
    translator, page = google_translator(), requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find('div', id="J_Title")  # title.h3.text
    price = soup.find('strong', id="J_StrPrice")  # price.text
    shopname = soup.find('div', class_="tb-shop-info-wrap")  # shopname.strong.text
    thumbnail = soup.find('img')['src']

    # if len(title.h3.text) < 60:
    response = discord.Embed(
        url=link,
        title=translator.translate(title.h3.text, lang_src='ch', lang_tgt='en'),
        color=0x00ff00
    )

    response.set_thumbnail(url="https:" + thumbnail)

    response.add_field(
        name="Price",
        value=price.text,
        inline=True
    )

    response.add_field(
        name="Seller",
        value=translator.translate(shopname.strong.text.strip(), lang_src='ch', lang_tgt='en'),
        inline=True
    )

    response.set_author(
        name=author
    )

    return response


"""def mobile_convert_link(link):
    convert = link.replace("m.intl", "item").replace("/detail/detail", "/item").replace(".html", ".htm")

    convert_split = convert.split("&fb", 1)

    return convert_split[0]"""


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'https://item.taobao.com/item.htm' or 'item.taobao.com/item':
        split = message.content.split()
        links_found = [tb_scanner(split[i], message.author) for i in range(len(split)) if 'https://item.taobao.com/item.htm' in split[i]]

        if len(links_found) == len(split):  # only Link
            for links in range(len(links_found)):
                await message.channel.send(embed=links_found[links])
                await message.delete()

        elif len(links_found) < len(split):  # w/ Text
            for links in range(len(links_found)):
                await message.channel.send(embed=links_found[links])

    elif message.content == 'https://m.intl.taobao.com/detail/detail.html' or "m.intl.taobao.com/detail/detail":
        split = message.content.split()
        links_found = [split[i] for i in range(len(split)) if 'https://m.intl.taobao.com/detail/detail.html' in split[i]]

        if len(links_found) == len(split):  # only Link
            for links in range(len(links_found)):
                convert = links_found[links].replace("m.intl", "item").replace("/detail/detail", "/item").replace(
                    ".html", ".htm")
                convert_split = convert.split("&fb", 1)

                print(convert_split)

                mobile_embed = tb_scanner(convert_split, message.author) #tb_scanner(convert.split("&fb", 1), message.author)

                await message.channel.send(embed=mobile_embed)
                await message.delete()

        elif len(links_found) < len(split):  # w/ Text
            for links in range(len(links_found)):
                convert = links_found[links].replace("m.intl", "item").replace("/detail/detail", "/item").replace(
                    ".html", ".htm")
                convert_split = convert.split("&fb", 1)

                print(convert_split)

                mobile_embed = tb_scanner(convert_split, message.author) #convert_split = convert.split("&fb", 1)

                await message.channel.send(embed=mobile_embed)




client.run(os.environ['DISCORD_TOKEN'])

# "https://item.taobao.com/item.htm"
# "item.taobao.com/item"
