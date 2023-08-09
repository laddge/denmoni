import os
from dotenv import load_dotenv
import discord
from discord import Option
from .generate import gen


def main():
    env_path = os.path.join(os.path.dirname(__file__), "../.env")
    load_dotenv(env_path)

    TOKEN = os.getenv("DISCORD_TOKEN")

    bot = discord.Bot()

    @bot.event
    async def on_ready():
        print(f"ready as {bot.user}")

    @bot.slash_command(description="電車の電光掲示板風のGIFを返します。")
    async def denmoni(
        ctx: discord.ApplicationContext,
        text: Option(str, required=True),
    ):
        await ctx.defer()
        buff = gen(text)
        buff.seek(0)
        await ctx.respond(file=discord.File(fp=buff, filename="output.gif"))

    bot.run(TOKEN)
