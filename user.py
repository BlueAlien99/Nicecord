class User:
    @staticmethod
    def from_json(entry):
        keys = ['id', 'name', 'count']
        if all(entry.get(key) for key in keys):
            return User(*(entry[key] for key in keys))
        else:
            return None

    def __init__(self, user_id, name, count=1):
        self.id = user_id
        self.name = name
        self.count = count

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
