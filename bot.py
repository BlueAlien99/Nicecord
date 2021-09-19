import re

from discord.ext import commands

from scoreboard import Scoreboard


bot = commands.Bot(command_prefix='.')


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

	scoreboard = Scoreboard(guild.id)
	await scoreboard.update_usernames(bot)
	reply = scoreboard.nice(user.id, user.display_name)

	print('>>>> ---- <<<< ---- >>>> ---- <<<<\n')
	print(f'{guild.name}\n{guild.id}\n{user.display_name}\n{msg.content}\n')
	print(reply)

	await channel.send(reply)


with open('.secret', 'r') as f:
	secret = f.read()

bot.run(secret)
