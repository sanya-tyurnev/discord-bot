import discord
import requests
import json
import os
from discord.ext import commands

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print("Вошли как")
    print(client.user.name)
    await client.change_presence(activity=discord.Game("¯\_(ツ)_/¯"))

@client.command()
async def test(ctx):
    await ctx.send("ок")

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
            is_moderator = False
            
            if moderator == str(ctx.author.id):
                is_moderator = True
                await ctx.channel.purge(limit=None, check=lambda msg: not msg.pinned)
                
            if is_moderator == False:
                await ctx.send("У тебя нет здесь власти :unamused:")
                
token = os.environ.get("token")
client.run(str(token))