
from discord.utils import get

botReference = None

def init(bot):
    global botReference
    botReference = bot

async def fetchUserName(id, gid):
    fetch_failed = False
    try:
        guild = await botReference.fetch_guild(gid)
        member = await guild.fetch_member(id)
    except:
        fetch_failed = True
    if fetch_failed or member == None or member.nick == None:
        fetch_failed = False
        try:
            user = await botReference.fetch_user(id)
        except:
            fetch_failed = True
        return None if fetch_failed or user == None else user.name
    else:
        return member.nick