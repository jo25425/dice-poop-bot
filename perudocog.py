import discord
import discord.ext.commands as commands
import random

class PerudoAI:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name

class Perudo(commands.Cog):
    def __init__(
        self,
    ):
        super().__init__()
        self.data = {}

    @commands.command()
    async def init_perudo(self, ctx):
        self.data[ctx.message.channel.id] = {"participants": [ctx.author], "game_started": False}
        await ctx.send("Starting Perudo game, you can join the game using `!join`")

    @commands.command()
    async def add_ai(self, ctx, name="HK_47"):
        self.data[ctx.message.channel.id]["participants"].append(PerudoAI(name=name))
        await ctx.send("Added AI")
    
    @commands.command()
    async def join(self, ctx):
        self.data[ctx.message.channel.id]["participants"].append(ctx.author)
        await ctx.send(f"Added {ctx.author.name}")

    @commands.command()
    async def list_participants(self, ctx):
        message = "Participants: " + " ".join(map(str, self.data[ctx.message.channel.id]["participants"]))
        await ctx.send(message)

    @commands.command()
    async def start_game(self, ctx):
        game_data = self.data[ctx.message.channel.id]
        participants = game_data["participants"]
        await ctx.send("Starting game with the following participants: " + ", ".join(map(str, participants)))

        game_data["player_order"] = random.sample(participants, len(participants))

        await ctx.send("Player order is: " + ", ".join(map(str, game_data["player_order"])))

        game_data["game_started"] = True

    @commands.command()
    async def force_end_game(self, ctx):
        await self.end_game(ctx.message.channel)

    async def end_game(self, channel):
        del self.data[channel.id]