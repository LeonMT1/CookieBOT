import configparser
import logging
import random
from datetime import datetime
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands


class GuessNumber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.de = ZoneInfo('Europe/Berlin')
        self.parser = configparser.ConfigParser()
        self.parser.read('config.cfg')
        self.channel = int(self.parser["CHANNELS"]["guess_number_channel"])
        self.number = None
        self.number1 = None
        self.number2 = None
        # maybe noch in datenbank diese daten speichern damit auch nach restart das game noch gleich ist

    async def new_game(self):
        DIFFICULTIES = {
            "einfach": (1, 25, 26, 50, discord.Color.green()),
            "mittel": (1, 50, 51, 100, discord.Color.yellow()),
            "schwer": (1, 100, 101, 200, discord.Color.red()),
        }
        difficulty = random.choice(list(DIFFICULTIES.keys()))
        (one1, two1, one2, two2, color) = DIFFICULTIES[difficulty]

        self.number1 = random.randint(one1, two1)
        self.number2 = random.randint(one2, two2)
        self.number = random.randint(self.number1, self.number2)

        embed = discord.Embed(
            title="Guess the Number",
            description=f"Die Zahl die zu erraten ist befindet sich **zwischen {self.number1} und {self.number2}**.\n Die Schwierigkeit ist **{difficulty}**.",
            color=color,
            timestamp=datetime.now(tz=self.de),
        )
        await self.bot.get_channel(self.channel).send(embed=embed)
        logging.info(f"Guess Number was sent, the number is {self.number}.")


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("guess_number.py is ready")
        await self.new_game()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.channel.id != self.channel:
            return

        try:
            guess = int(message.content)
        except ValueError:
            return

        if guess == self.number:
            embed = discord.Embed(
                title="RICHTIG!",
                description=f"{message.author.mention} hat die Zahl **{self.number}** geschrieben und lag richtig.",
                color=discord.Color.green(),
                timestamp=datetime.now(tz=self.de),
            )
            await self.bot.get_channel(self.channel).send(embed=embed)
            await message.add_reaction("✅")
            await self.new_game()
            logging.info(f"{message.author} wrote the correct number {self.number}")
            # jetzt noch kekse geben
        else:
            await message.add_reaction("❌")
            chance = random.randint(1 ,1)
            if chance == 1:
                if self.number1 <= guess <= self.number2:
                    if guess > self.number:
                        await message.reply("Die gesuchte Zahl ist kleiner.", mention_author=False)
                    else:
                        await message.reply("Die gesuchte Zahl ist größer.", mention_author=False)
                else:
                    await message.reply(f"Deine Zahl liegt nicht in der angegebenen Zahlen spanne. Die gesuchte Zahl liegt zwischen **{self.number1} und {self.number2}**.", mention_author=False)


def setup(bot):
    bot.add_cog(GuessNumber(bot))
