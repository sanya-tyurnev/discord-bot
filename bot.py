import requests
import json
import discord
import asyncio

DISCORD_BOT_TOKEN = "NjI0NTc4MzEyMzE1ODYzMDYw.XYYUGA.7sY3nH3V2xChCg-k8nfk5L6Q324"

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(DISCORD_BOT_TOKEN)

#response = requests.get("http://raptus-statistics.000webhostapp.com/get.php?type=statistics")

#data = json.loads(response.text)

#print(data["points"])
#print(data["rank"])

