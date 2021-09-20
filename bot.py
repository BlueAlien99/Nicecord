import re

from discord.ext import commands

from scoreboard import Scoreboard

bot = commands.Bot(command_prefix='.')

scoreboards = {}


def get_scoreboard(guild_id):
    if guild_id not in scoreboards:
        scoreboards[guild_id] = Scoreboard(guild_id)
    return scoreboards[guild_id]


@bot.event
async def on_ready():
    print('Bot is ready. Nice.\n')


@bot.event
async def on_message(msg):
    user = msg.author
    guild = msg.guild
    channel = msg.channel

    # remove discord's markdown and whitespaces
    cleanMsg = re.sub(r'(\*|_|~|`|>|\||\s)', '', msg.content)

    if user.bot is True or cleanMsg.lower() != 'nice':
        return

    scoreboard = get_scoreboard(guild.id)
    reply = await scoreboard.nice(user.id, user.display_name, bot)

    print('>>>> ---- <<<< ---- >>>> ---- <<<<\n')
    print(f'{guild.name}\n{guild.id}\n{user.display_name}\n{msg.content}\n')
    print(reply)

    await channel.send(reply)


with open('.secret', 'r') as f:
    secret = f.read()

bot.run(secret)
