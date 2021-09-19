from utils import fetch_username


class User:
    def __init__(self, user_id, name):
        self.id = user_id
        self.count = 1
        self.name = name

    def __str__(self):
        return f'{self.id} + {self.name} + {self.count}'

    def nice(self):
        self.count += 1

    async def update_name(self, bot, guild_id):
        name = await fetch_username(bot, self.id, guild_id)
        if name is not None:
            self.name = name
