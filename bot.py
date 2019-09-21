import discord
from discord.ext import commands

TOKEN = 'tTmRFg8NMIl4wlw5K0e8hniFUJqkT38_'
bot = commands.Bot(command_prefix='!')


@bot.command(pass_context=True)  # разрешаем передавать агрументы
async def test(ctx, arg):  # создаем асинхронную фунцию бота
    await ctx.send(arg)  # отправляем обратно аргумент


bot.run(TOKEN)
