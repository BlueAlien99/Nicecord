import asyncio
import json
import pickle
from pathlib import Path

from user import User

NUM_OF_TOP_USERS = 3


class Scoreboard:
    def __init__(self, guild_id):
        self.guild_id = guild_id
        try:
            Path('niceData').mkdir(exist_ok=True)
            try:
                self.board = pickle.load(open(f'niceData/{guild_id}.bin', 'rb'))
            except:
                with open(f'niceData/{guild_id}.json', 'r') as f:
                    backupData = json.load(f)
                    self.board = []
                    for entry in backupData:
                        user = User(entry['id'], entry['name'])
                        user.count = entry['count']
                        self.board.append(user)
        except (FileNotFoundError, EOFError):
            self.board = []
        except Exception:
            print('Unexpected error in Scoreboard.__init__. Nice.')
            raise

    async def nice(self, user_id, user_name, bot):
        try:
            i = [x.id for x in self.board].index(user_id)
            self.board[i].nice(user_name)
            # move the user up in the leaderboard
            while i > 0 and self.board[i].count > self.board[i - 1].count:
                self.board[i], self.board[i - 1] = self.board[i - 1], self.board[i]
                i -= 1
        except ValueError:
            newUser = User(user_id, user_name)
            self.board.append(newUser)
            i = len(self.board) - 1

        await self.update_usernames(bot)

        # not necessary, only so that an admin can read the contents of a "database"
        boardDict = list(map(lambda x: vars(x), self.board))
        with open(f'niceData/{self.guild_id}.json', 'w') as file:
            json.dump(boardDict, file)

        pickle.dump(self.board, open(f'niceData/{self.guild_id}.bin', 'wb'))

        return self.get_leaderboard(i)

    async def update_usernames(self, bot):
        users_to_update = [self.board[i] for i in range(min(NUM_OF_TOP_USERS, len(self.board)))]

        await asyncio.wait([user.update_name(bot, self.guild_id) for user in users_to_update])

    def get_leaderboard(self, curr_user_idx):
        def format_entry(pos, name, count):
            return f'**{pos}.** {name} at **{count} {"nice" if count == 1 else "nices"}**\n'

        ret = '𝓷𝓲𝓬𝓮 ☜(ﾟヮﾟ☜)\n\nNice Leaderboard\n'

        for k, x in enumerate(self.board[:NUM_OF_TOP_USERS]):
            ret += format_entry(k + 1, x.name, x.count)

        if curr_user_idx < NUM_OF_TOP_USERS:
            return ret
        elif curr_user_idx > NUM_OF_TOP_USERS:
            ret += '**...**\n'

        curr_user = self.board[curr_user_idx]
        ret += format_entry(curr_user_idx + 1, curr_user.name, curr_user.count)

        return ret
