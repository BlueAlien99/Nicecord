import json
import pickle

from pathlib import Path

from utils import fetchUserName

class User:

	def __init__(self, id, name):
		self.id = id
		self.count = 1
		self.name = name

	def __str__(self):
		return f'{self.id} + {self.name} + {self.count}'

	def nice(self):
		self.count += 1

	async def updateName(self, gid):
		name = await fetchUserName(self.id, gid)
		if name != None:
			self.name = name

class Scoreboard:

	def __init__(self, gid):
		self.gid = gid
		try:
			Path('niceData').mkdir(exist_ok = True)
			self.board = pickle.load(open(f'niceData/{gid}.bin', 'rb'))
		except (FileNotFoundError, EOFError):
			self.board = []
		except:
			print('Unexpected error in Scoreboard.__init__. Nice.')
			raise

	def nice(self, id, name):
		i = -1
		try:
			i = [ x.id for x in self.board ].index(id)
			self.board[i].nice()
			while i > 0 and self.board[i].count > self.board[i-1].count:
				self.board[i], self.board[i-1] = self.board[i-1], self.board[i]
				i -= 1
		except ValueError:
			newUser = User(id, name)
			self.board.append(newUser)
			i = len(self.board) - 1
		
		boardDict = list(map(lambda x: vars(x), self.board))

		with open(f'niceData/{self.gid}.json', 'w') as file:
			json.dump(boardDict, file)

		pickle.dump(self.board, open(f'niceData/{self.gid}.bin', 'wb'))

		return self.getLeaderboard(i)

	async def updateUsernames(self):
		for user in self.board:
			await user.updateName(self.gid)

	def getLeaderboard(self, i):
		ret = '𝓷𝓲𝓬𝓮 ☜(ﾟヮﾟ☜)\n\nNice Leaderboard\n'

		for k, x in enumerate(self.board[:3]):
			ret += f'**{k+1}.** {x.name} at **{x.count} nices**\n'

		if i < 3:
			return ret
		elif i > 3:
			ret += '**...**\n'
		
		ret += f'**{i+1}.** {self.board[i].name} at **{self.board[i].count} nices**\n'

		return ret
