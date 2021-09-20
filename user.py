class User:
    def __init__(self, user_id, name, count=1):
        self.id = user_id
        self.count = count
        self.name = name

    def nice(self, name):
        self.count += 1
        self.name = name

    async def update_name(self, bot, guild_id):
        try:
            guild = await bot.fetch_guild(guild_id)
            member = await guild.fetch_member(self.id)

            if member.nick is not None:
                self.name = member.nick
            else:
                self.name = member.name

        except Exception:
            pass
