
from discord.utils import get

botReference = None

def init(bot):
    global botReference
    botReference = bot

async def fetchUserName(id, gid):
    guild = await botReference.fetch_guild(gid)
    member = await guild.fetch_member(id)
    if member == None or member.nick == None:
        user = await botReference.fetch_user(id)
        return None if user == None else user.name
    else:
        return member.nick