import discord
import requests
import json
import asyncio
import os
from discord.ext import commands

client = commands.Bot(command_prefix = '!')
client.remove_command("help")

all_commands = [
    "!place -> возвращает текущее место в рейтинге",
    "!rm кол-во повторений (дефолт 1, макс. 5) -> приглашает всех на рм",
    "!say текст * кол-во повторений (дефолт 1, макс. 5) -> отправляет tts сообщение с указанным текстом",
    "!crowns название спецоперации сложность (если есть) -> возвращает кол-во очков и время для получения всех корон"
    ]

moderator_commands = [
    "!clear -> очищает канал от сообщений",
    "!ban @ссылка на участника -> лишает участника возможности отправлять любые сообщения",
    "!unban @ссылка на участника -> снимает все ограничения с участника"
    ]

pripyat = [
    [171000, "49:00"],
    [180000, "64:00"],
    [180000, "64:00"]
]

eclipse = [
    [172979, "24:04"],
    [186139, "26:02"],
    [200188, "41:45"]
]

icebreaker = [
    [1006712, "33:10"],
    [1107677, "29:53"],
    [291535, "35:08"]
]

black_shark = [
    [278872, "35:12"],
    [303596, "36:26"],
    [481648, "42:47"]
]

anubis = [
    [739000, "33:00"],
    [926000, "33:00"],
    [1841000, "35:00"]
]

volcano = [
    [1520000, "35:00"],
    [1566000, "33:30"],
    [1513000, "32:00"],
    [1774000, "46:30"]
]

snow_bastion = [
    [365500, "26:30"],
    [450000, "31:30"],
    [446200, "19:00"],
    [1261700, "77:00"]
]

white_shark = [825000, "49:30"]

@client.event
async def on_ready():
    print("Вошли как")
    print(client.user.name)
    await client.change_presence(activity=discord.Game("¯\_(ツ)_/¯"), status=discord.Status.do_not_disturb)

@client.event
async def on_message(message):
    if(message.content.lower().rstrip("!") == "всем привет"):
        await message.channel.send("Приветик :kissing_heart:")

    await client.process_commands(message)

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
async def help(ctx):
    all_commands_msg = "Общие команды:\n"
    moderator_commands_msg = "Команды для модераторов:\n"

    for all_command in all_commands:
        all_commands_msg += "```" + all_command + "```"

    for moderator_command in moderator_commands:
        moderator_commands_msg += "```" + moderator_command + "```"

    full_msg = all_commands_msg + "\n" + moderator_commands_msg

    await ctx.send(full_msg)

    if str(ctx.channel.type) != "private":
        await ctx.message.delete()

@client.command()
async def id(ctx):
    if str(ctx.channel.type) == "private":
        await ctx.send("Ваш ID: " + str(ctx.author.id))

@client.command()
async def get_id(ctx):
    if str(ctx.channel.type) == "private":
        full_content = ctx.message.content.split(" ")
        content = " ".join(full_content[full_content.index("!get_id") + 1:])
        is_break = False

        for guild in client.guilds:
            for member in guild.members:
                if member.name == content:
                    await ctx.send(member.name + "#" + member.discriminator + "\nID: " + str(member.id))
                    is_break = True
                    break
            
            if is_break:
                break

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
            await ctx.send(ctx.author.name + " у тебя нет здесь власти :unamused:")
                
@client.command()
async def rm(ctx, repeat = 1):
    if str(ctx.channel.type) == "private":
        await ctx.send("Данная команда работает только на сервере :worried:")
    else:
        if repeat > 5:
            repeat = 5

        await ctx.message.delete()
        my_msg = await ctx.send("На рм блять\n" * repeat, tts=True)
        await my_msg.delete()

@client.command()
async def say(ctx):
    if str(ctx.channel.type) == "private":
        await ctx.send("Данная команда работает только на сервере :worried:")
    else:
        repeat = 1

        if ctx.message.content.strip() != "!say":
            content = ctx.message.content[ctx.message.content.find(" ") + 1 :].strip()

            if content.find("*") >= 0:
                send_msg = content[: content.rfind("*")].strip()
                repeat = int(content[content.rfind("*") + 1 :].strip())
            else:
                send_msg = content

            if repeat > 5:
                repeat = 5

            await ctx.message.delete()
            my_msg = await ctx.send((send_msg + "\n") * repeat, tts=True)
            await my_msg.delete()

@client.command()
async def ban(ctx, member : discord.Member = None):
    if member is not None:
        if str(ctx.channel.type) == "private":
            await ctx.send("Данная команда работает только на сервере :worried:")
        else:
            is_moderator = False
            moderators = os.environ.get("moderators")
            
            for moderator in str(moderators).split(","):
                if int(moderator) == ctx.author.id:
                    is_moderator = True
                    break
            else:
                await ctx.send(ctx.author.name + " у тебя нет здесь власти :unamused:")
                
            if is_moderator:
                if ctx.author.id == member.id:
                    await ctx.send("Нельзя забанить самого себя :stuck_out_tongue:")
                elif client.user.id == member.id:
                    await ctx.send("Мечтать не вредно :stuck_out_tongue:")
                else:
                    for role in member.roles:
                        if role.name == "АДМИН":
                            await ctx.send("Нельзя забанить админа :stuck_out_tongue:")
                            break
                        elif role.name == "МОДЕРАТОР":
                            await ctx.send("Нельзя забанить модератора :stuck_out_tongue:")
                            break
                    else:
                        role = discord.utils.get(ctx.guild.roles, name="БАН")
                        await member.add_roles(role)
                        await ctx.send(member.name + " теперь не может отправлять сообщения :zipper_mouth:")
                        await ctx.message.delete()

@client.command()
async def unban(ctx, member : discord.Member = None):
    if member is not None:
        if str(ctx.channel.type) == "private":
            await ctx.send("Данная команда работает только на сервере :worried:")
        else:
            moderators = os.environ.get("moderators")
            
            for moderator in str(moderators).split(","):
                if int(moderator) == ctx.author.id:
                    role = discord.utils.get(ctx.guild.roles, name="БАН")
                    await member.remove_roles(role)
                    await ctx.send(member.name + " помилован :kissing_heart:")
                    await ctx.message.delete()
                    break 
            else:
                await ctx.send(ctx.author.name + " у тебя нет здесь власти :unamused:")

@client.command()
async def crowns(ctx):
    content = ctx.message.content[ctx.message.content.find(" ") + 1 :].strip()
    white_shark_flag = False
    send = False

    if content.lower().find("белая акула") >= 0:
        mission_name = content
    else:
        mission_name = content[: content.rfind(" ")].strip()

    if mission_name.lower() == "белая акула":
        white_shark_flag = True
    else:
        mission_difficulty = content[content.rfind(" ") + 1 :].strip()

    if mission_name.lower() == "припять":
        name = "Припять"
        send = True

        if mission_difficulty.lower() == "легко":
            difficulty = "Легко"
            score = pripyat[0][0]
            time = pripyat[0][1]

        if mission_difficulty.lower() == "сложно":
            difficulty = "Сложно"
            score = pripyat[1][0]
            time = pripyat[1][1]

        if mission_difficulty.lower() == "профи":
            difficulty = "Профи"
            score = pripyat[2][0]
            time = pripyat[2][1]

    if mission_name.lower() == "затмение":
        name = "Затмение"
        send = True

        if mission_difficulty.lower() == "легко":
            difficulty = "Легко"
            score = eclipse[0][0]
            time = eclipse[0][1]

        if mission_difficulty.lower() == "сложно":
            difficulty = "Сложно"
            score = eclipse[1][0]
            time = eclipse[1][1]

        if mission_difficulty.lower() == "профи":
            difficulty = "Профи"
            score = eclipse[2][0]
            time = eclipse[2][1]

    if mission_name.lower() == "ледокол":
        name = "Ледокол"
        send = True

        if mission_difficulty.lower() == "легко":
            difficulty = "Легко"
            score = icebreaker[0][0]
            time = icebreaker[0][1]

        if mission_difficulty.lower() == "сложно":
            difficulty = "Сложно"
            score = icebreaker[1][0]
            time = icebreaker[1][1]

        if mission_difficulty.lower() == "профи":
            difficulty = "Профи"
            score = icebreaker[2][0]
            time = icebreaker[2][1]

    if mission_name.lower() == "черная акула":
        name = "Черная акула"
        send = True

        if mission_difficulty.lower() == "легко":
            difficulty = "Легко"
            score = black_shark[0][0]
            time = black_shark[0][1]

        if mission_difficulty.lower() == "сложно":
            difficulty = "Сложно"
            score = black_shark[1][0]
            time = black_shark[1][1]

        if mission_difficulty.lower() == "профи":
            difficulty = "Профи"
            score = black_shark[2][0]
            time = black_shark[2][1]

    if mission_name.lower() == "анубис":
        name = "Анубис"
        send = True

        if mission_difficulty.lower() == "легко":
            difficulty = "Легко"
            score = anubis[0][0]
            time = anubis[0][1]

        if mission_difficulty.lower() == "сложно":
            difficulty = "Сложно"
            score = anubis[1][0]
            time = anubis[1][1]

        if mission_difficulty.lower() == "профи":
            difficulty = "Профи"
            score = anubis[2][0]
            time = anubis[2][1]

    if mission_name.lower() == "вулкан":
        name = "Вулкан"
        send = True

        if mission_difficulty.lower() == "легко":
            difficulty = "Легко"
            score = volcano[0][0]
            time = volcano[0][1]

        if mission_difficulty.lower() == "сложно":
            difficulty = "Сложно"
            score = volcano[1][0]
            time = volcano[1][1]

        if mission_difficulty.lower() == "профи":
            difficulty = "Профи"
            score = volcano[2][0]
            time = volcano[2][1]

        if mission_difficulty.lower() == "хардкор":
            difficulty = "Хардкор"
            score = volcano[3][0]
            time = volcano[3][1]

    if mission_name.lower() == "снежный бастион":
        name = "Снежный бастион"
        send = True

        if mission_difficulty.lower() == "острие":
            difficulty = "Острие"
            score = snow_bastion[0][0]
            time = snow_bastion[0][1]

        if mission_difficulty.lower() == "засада":
            difficulty = "Засада"
            score = snow_bastion[1][0]
            time = snow_bastion[1][1]

        if mission_difficulty.lower() == "зенит":
            difficulty = "Зенит"
            score = snow_bastion[2][0]
            time = snow_bastion[2][1]

        if mission_difficulty.lower() == "марафон":
            difficulty = "Марафон"
            score = snow_bastion[3][0]
            time = snow_bastion[3][1]

    if mission_name.lower() == "белая акула":
        name = "Белая акула"
        send = True
        score = white_shark[0]
        time = white_shark[1]

    if send:
        if white_shark_flag:
            await ctx.send(name + ":\n```Очки: " + "{:,}".format(score).replace(',', ' ') + "\nВремя: " + time + "```")
        else:
            await ctx.send(name + " -> " + difficulty + ":\n```Очки: " + "{:,}".format(score).replace(',', ' ') + "\nВремя: " + time + "```")

    await ctx.message.delete()

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Указанный аргумент не является ссылкой на участника :thinking:")

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Указанный аргумент не является ссылкой на участника :thinking:")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Команда " + ctx.message.content + " не существует :thinking:\nОтправьте !help для получения списка команд!")

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