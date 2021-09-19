import json
import pickle

from pathlib import Path

from user import User


class Scoreboard:
    def __init__(self, guild_id):
        self.guild_id = guild_id
        try:
            Path('niceData').mkdir(exist_ok=True)
            self.board = pickle.load(open(f'niceData/{guild_id}.bin', 'rb'))
        except (FileNotFoundError, EOFError):
            self.board = []
        except Exception:
            print('Unexpected error in Scoreboard.__init__. Nice.')
            raise

    def nice(self, user_id, name):
        try:
            i = [x.id for x in self.board].index(user_id)
            self.board[i].nice()
            while i > 0 and self.board[i].count > self.board[i - 1].count:
                self.board[i], self.board[i - 1] = self.board[i - 1], self.board[i]
                i -= 1
        except ValueError:
            newUser = User(user_id, name)
            self.board.append(newUser)
            i = len(self.board) - 1

        boardDict = list(map(lambda x: vars(x), self.board))

        with open(f'niceData/{self.guild_id}.json', 'w') as file:
            json.dump(boardDict, file)

        pickle.dump(self.board, open(f'niceData/{self.guild_id}.bin', 'wb'))

        return self.get_leaderboard(i)

    async def update_usernames(self, bot):
        for user in self.board:
            await user.update_name(bot, self.guild_id)

    def get_leaderboard(self, i):
        def format_entry(pos, name, count):
            return f'**{pos}.** {name} at **{count} {"nice" if count == 1 else "nices"}**\n'

        ret = '𝓷𝓲𝓬𝓮 ☜(ﾟヮﾟ☜)\n\nNice Leaderboard\n'

        for k, x in enumerate(self.board[:3]):
            ret += format_entry(k + 1, x.name, x.count)

        if i < 3:
            return ret
        elif i > 3:
            ret += '**...**\n'

        ret += format_entry(i + 1, self.board[i].name, self.board[i].count)

        return ret
