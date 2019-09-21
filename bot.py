import discord
from discord.ext import commands

TOKEN = 'NjI0NTc4MzEyMzE1ODYzMDYw.XYYUGA.7sY3nH3V2xChCg-k8nfk5L6Q324'
bot = commands.Bot(command_prefix='!')


@bot.command(pass_context=True)  # разрешаем передавать агрументы
async def test(ctx, arg):  # создаем асинхронную фунцию бота
    await ctx.send(arg)  # отправляем обратно аргумент


bot.run(TOKEN)
