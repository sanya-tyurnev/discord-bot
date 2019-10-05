import discord
import requests
import json
import asyncio
import os
from discord.ext import commands

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print("Вошли как")
    print(client.user.name)
    await client.change_presence(activity=discord.Game("¯\_(ツ)_/¯"))

@client.command()
async def place(ctx):
    my_msg = await ctx.send("Секундочку... :wink:")
    
    if str(ctx.channel.type) != "private":
        await ctx.message.delete()

    points, rank, league, next, previous = get_statistics()
    
    if next[1] == 1:
        next_league = "Элиты"
        
    if next[1] == 2:
        next_league = "Платины"
        
    if next[1] == 3:
        next_league = "Золота"
        
    if next[1] == 4:
        next_league = "Серебра"
        
    if next[1] == 5:
        next_league = "Бронзы"
        

    if previous[1] == 2:
        previous_league = "Платины"
        
    if previous[1] == 3:
        previous_league = "Золота"
        
    if previous[1] == 4:
        previous_league = "Серебра"
        
    if previous[1] == 5:
        previous_league = "Бронзы"

    if previous[1] == 6:
        previous_league = "Стали"
             
    await ctx.send(">>> ```\nОчки: " + "{:,}".format(int(points)).replace(',', ' ') + "\nЛига: " + league + "\nМесто: " + str(rank) + "```\n```\nДо " + next_league + ": " + "{:,}".format(next[0]).replace(',', ' ') + "\nДо " + previous_league + ": " + "{:,}".format(previous[0]).replace(',', ' ') + "```")
    await my_msg.delete()

@client.command()
async def info(ctx):
    await ctx.send("Доступные команды\n>>> ```\n!place -> возвращает текущее место в рейтинге\n!clear -> очищает канал от сообщений\n!rm -> приглашает всех на рм\n!say текст -> отправляет tts сообщение с указанным текстом```")

    if str(ctx.channel.type) != "private":
        await ctx.message.delete()

@client.command()
async def id(ctx):
    if str(ctx.channel.type) == "private":
        await ctx.send("Ваш ID: " + str(ctx.author.id))

@client.command()
async def clear(ctx):
    if str(ctx.channel.type) == "private":
        await ctx.send("Невозможно очистить личные сообщения :worried:")
    else:
        moderators = os.environ.get("moderators")
        
        for moderator in str(moderators).split(","):
            if int(moderator) == ctx.author.id:
                await ctx.channel.purge(limit=None, check=lambda msg: not msg.pinned)
                break 
        else:
            await ctx.send(ctx.author.name + "у тебя нет здесь власти :unamused:")    
                
@client.command()
async def rm(ctx):
    if str(ctx.channel.type) != "private":
        await ctx.message.delete()
        my_msg = await ctx.send("На рм блять", tts=True)
        await my_msg.delete()

@client.command()
async def say(ctx):
    content = ctx.message.content.split(" ")
    send_msg = " ".join(content[content.index("!say") + 1:])

    if len(send_msg) > 0:
        await ctx.message.delete()
        my_msg = await ctx.send(send_msg, tts=True)
        await my_msg.delete()

def get_statistics():
    response = requests.get("http://raptus-statistics.000webhostapp.com/get.php?type=bot")
    data = json.loads(response.text)
    
    if data["league"] == 1:
        rank = data["rank"]
        league = "Элитная"

    if data["league"] == 2:
        rank = int(data["rank"]) - 10
        league = "Платиновая"

    if data["league"] == 3:
        rank = int(data["rank"]) - 100
        league = "Золотая"

    if data["league"] == 4:
        rank = int(data["rank"]) - 500
        league = "Серебряная"

    if data["league"] == 5:
        rank = int(data["rank"]) - 1000
        league = "Бронзовая"

    if data["league"] == 6:
        rank = int(data["rank"]) - 2000
        league = "Стальная"
        
    next = [data["next"]["left"], data["next"]["league"]]
    previous = [data["previous"]["left"], data["previous"]["league"]]
    
    return data["points"], rank, league, next, previous

token = os.environ.get("token")
client.run(str(token))