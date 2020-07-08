import discord
import discord.ext.commands as commands
import json
from loguru import logger as _logger

from perudocog import Perudo

class DicePoopBot(commands.Bot):
    def __init__(
        self,
        command_prefix="!"
    ):
        super().__init__(command_prefix=command_prefix)

    async def on_ready(self):
        _logger.info("Bot started")

        self.add_command(say)
        _logger.info("Added commands")

        self.add_cog(Perudo())
        _logger.info("Added Perudo Cog")
    
    async def on_message(self, message):
        _logger.debug(message.channel.name)
        _logger.debug(message.channel.guild.name)
        await super().on_message(message)
    

@commands.command()
async def say(ctx, arg):
    await ctx.send(arg)

if __name__ == '__main__':
    config = json.load(open("config.json"))
    bot = DicePoopBot()
    bot.run(config["bot_token"])
