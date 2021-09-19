from discord.ext.commands import Bot


async def fetch_username(bot: Bot, user_id, guild_id):
    try:
        guild = await bot.fetch_guild(guild_id)
        member = await guild.fetch_member(user_id)

        if member.nick is not None:
            return member.nick

    except Exception:
        try:
            user = await bot.fetch_user(user_id)
            return user.name

        except Exception:
            pass

    return None
