import requests
import json
import discord
import asyncio
import os

client = discord.Client()

@client.event
async def on_ready():
    print("Вошли как")
    print(client.user.name)
    await client.change_presence(activity=discord.Game("¯\_(ツ)_/¯"))

@client.event
async def on_message(message):
    if message.content.startswith('!стата'):
        print("Запрос статы")
        my_msg = await message.channel.send("Секундочку... :wink:")
        await message.delete()

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
             
        await message.channel.send(">>> ```\nОчки: " + "{:,}".format(int(points)).replace(',', ' ') + "\nЛига: " + league + "\nМесто: " + str(rank) + "```\n```\nДо " + next_league + ": " + "{:,}".format(next[0]).replace(',', ' ') + "\nДо " + previous_league + ": " + "{:,}".format(previous[0]).replace(',', ' ') + "```")
        await my_msg.delete()

    if message.content.startswith('!очистить'):
         moderators = os.environ.get("moderators")

         for moderator in str(moderators).split(","):
              is_moderator = False

              if moderator == str(message.author):
                   is_moderator = True

                   try:
                        await message.channel.purge(limit=None, check=lambda msg: not msg.pinned)
                   except AttributeError:
                        await message.channel.send("Невозможно очистить личные сообщения :worried:")

         if is_moderator == False:
              await message.channel.send("У тебя нет здесь власти :unamused:")

    if message.content.startswith('!инфа'):
         await message.channel.send("Доступные команды\n>>> ```\n!стата -> возвращает текущее место в рейтинге\n!очистить -> очищает канал от сообщений```")
         await message.delete()

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