from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from extra.messages import BAD_REQUEST_MESSAGE, HELP_COMMAND_MESSAGE

import random
from dotenv import load_dotenv
import os


load_dotenv()


def parse_graph(s):
    n = 0
    edges = [[j for j in i.split(' ') if j and j[0] != '/'] for i in s.split(',')]
    n = int(max(max(edges, key = max))) + 1
    G = [[] for i in range(n)]

    for edge in edges:
        a, b = int(edge[0]), int(edge[1])
        G[a].append(b)
        G[b].append(a)
    return G


def dfs(g, v, used):
    used[v] = 1
    for i in g[v]:
        if used[i] == 0:
            dfs(g, i, used)


bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(HELP_COMMAND_MESSAGE)


@dp.message_handler(commands=['degree'])
async def degree(message: types.Message):
    G = parse_graph(message.text)
    await message.reply(str(min(len(x) for x in G if x > 0)) + " " +  str(max(len(x) for x in G)))


@dp.message_handler(commands=['component'])
async def component(message: types.Message):
    G = parse_graph(message.text)
    n = len(G)
    used = [0] * n
    answer = 0
    for i in range(1, n):
        if len(G[i]) > 0 and used[i] == 0:
            dfs(G,  i, used)
            answer += 1
    await message.reply(answer)


@dp.message_handler(commands=['random_graph'])
async def random_graph(message: types.Message):
    n = int(message.text.split()[-1])
    G = []
    for i in range(n):
        G.append([])
        for j in range(n):
            G[i].append(random.randint(0, 1))

    await message.reply(str(G))


@dp.message_handler(commands=['random_tree'])
async def send_welcome(message: types.Message):
    n = int(message.text.split()[-1])
    G = []
    for i in range(2, n + 1):
        G.append(random.randint(1, i - 1))
    await message.reply(str(G))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
