import requests
import json
import discord
import asyncio
import os

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!стата'):
        print("Запрос статы")
        points, rank, league = get_statistics()
        await message.channel.send("Очки: " + "{:,}".format(points).replace(',', ' ') + "\nЛига: " + league + "\nМесто: " + str(rank))

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

    return data["points"], rank, league

TOKEN = os.environ.get("TOKEN")

client.run(str(TOKEN))