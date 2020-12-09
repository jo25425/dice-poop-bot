import discord
import discord.ext.commands as commands
import json
from loguru import logger as _logger

import birthday
from perudocog import Perudo

intents = discord.Intents.default()
intents.members = True


class DicePoopBot(commands.Bot):
    def __init__(
        self,
        command_prefix="!"
    ):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.additions_ready = False

    async def on_ready(self):
        if self.additions_ready:
            return

        _logger.info("Bot started")

        self.add_command(say)
        self.add_command(die)
        _logger.info("Added commands")

        self.add_cog(Perudo())
        _logger.info("Added Perudo Cog")

        self.add_listener(birthday.giphy_spammer, 'on_message')
        _logger.info("Added Birthday Gif Spammer")

        self.additions_ready = True
    
    async def on_message(self, message):
        _logger.debug(message.channel.name)
        _logger.debug(message.channel.guild.name)
        await super().on_message(message)
    

@commands.command()
async def say(ctx, arg):
    await ctx.send(arg)


@commands.command()
async def die(ctx, arg=None):
    await ctx.send("Ok :(")
    await ctx.bot.logout()

if __name__ == '__main__':
    config = json.load(open("config.json"))

    bot = DicePoopBot()
    bot.run(config["bot_token"])
