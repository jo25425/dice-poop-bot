from discord.ext import commands, tasks
import json
import random
import datetime as dt
import asyncio
import collections

from loguru import logger

import giphy_client
from giphy_client.rest import ApiException

import cogs


spam_triggers = [
    'cool',
    'dope',
    'ace',
    'boss',
    'nerd',
    'pro',
    'great',
    'fun',
    'birth',
    'day',
    'today',
    'epic',
    'nice',
    'awesome',
    'gamer',
    'good',
    'wow'
]

config = json.load(open("config.json"))
birthday_list = [("santa#9329", (12, 10))]
birthday_boy = config["birthday_boy"]
giphy_token = config["giphy_token"]
api_instance = giphy_client.DefaultApi()


async def search_gifs(query):
    try:
        response = api_instance.gifs_search_get(giphy_token, query, limit=5, rating='g')
        lst = list(response.data)
        gif = lst[random.randint(0, len(lst)-1)]
        return gif.url

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e


class Birthdays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birthdays = collections.defaultdict(set)
        for user, (month, day) in birthday_list:
            self.birthdays[(month, day)].add(user)
        self.target_time = (0, 0, 30)
        self.channels = set()
        self.check_birthdays.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        matches = [trig for trig in spam_triggers if trig in message.content.lower()]
        if not matches:
            return

        date = dt.datetime.now()
        users = [message.guild.get_member_named(name=name) for name in self.birthdays[(date.day, date.month)]]
        users = [user for user in users if user]
        if len(users) == 0:
            return

        trig = matches[random.randint(0, len(matches)-1)]
        reply = "Speaking of {}... It's {}'s birthday today!".format(trig, users[0].mention)
        gif = await search_gifs(trig)

        await message.channel.send(reply)
        await message.channel.send(gif)

    @commands.command()
    async def look(self, ctx):
        await ctx.send(":eyes:")
        self.channels.add(self.bot.get_channel(ctx.message.channel.id))

    @tasks.loop(hours=24)
    async def check_birthdays(self):
        date = dt.datetime.now()
        users = self.birthdays[(date.day, date.month)]
        for channel in self.channels:
            for user in users:
                mention = channel.guild.get_member_named(name=user)
                if mention:
                    channel.send(f"Hey look, it's {mention.mention}'s birthday! Happy birthday {mention.mention} :tada:")

    @check_birthdays.before_loop
    async def before_loop(self):
        time = dt.datetime.now()
        hour, minute, second = self.target_time
        time_to_wait = ((hour*60 + minute)*60 + second) - ((time.hour*60 + time.minute)*60 + time.second)
        logger.info(f"Waiting {time_to_wait % (60*60*24)}s")
        await asyncio.sleep(time_to_wait % (60*60*24))


cogs.cog_list.append(Birthdays)
