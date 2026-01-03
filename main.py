import discord
import ezcord
import os

from dotenv import load_dotenv

from utils import greeter_builder
from logging_config import setup_logging
import logging


# SETTINGS 
guild_id = 1333488718576877600
log_channel = 1456840069460525136
im_log_channel = 1456840129153863690
welcome_channel = 1456842380870418564


setup_logging()
logger = logging.getLogger(__name__)
bot = ezcord.Bot(intents=discord.Intents.all(), debug_guilds=None, ready_event=None, language="de")
bot.add_help_command()


@bot.event
async def on_ready():
    logging.info("Discord Bot is online.")
    print("System is up and running.")


@bot.event
async def on_member_join(member):
    logging.info(f"{member} joined {member.guild.name}")
    if guild_id == member.guild.id:
        if member.bot:
            embot = greeter_builder(title="Discord Bot hinzugefügt", description=f"Der Bot {member.mention} wurde hinzugefügt.", color=discord.Color.green(), member=member)
            await bot.get_channel(im_log_channel).send(embed=embot)
            return

        file = discord.File("img/join.gif", filename="join.gif")

        emuser = greeter_builder(title=":wave: Cool das du hier her gefunden hast!", description=f"Hallo {member.mention} wir hoffen das du viel Spaß auf diesen Server haben wirst ;).", color=discord.Color.orange(), member=member, image="join")
        await bot.get_channel(welcome_channel).send(embed=emuser, file=file)
    else:
        logging.warning(f"{member} joined a Server that wasn´t configured")


@bot.event
async def on_member_remove(member):
    logging.info(f"{member} left from {member.guild.name}")
    if guild_id == member.guild.id:
        if member.bot:
            embot = greeter_builder(title="Discord Bot entfernt", description=f"Der Bot {member.mention} wurde entfernt.", color=discord.Color.red(), member=member)
            await bot.get_channel(im_log_channel).send(embed=embot)
            return
        file = discord.File("img/leave.gif", filename="leave.gif")

        emuser = greeter_builder(title=":wave: Tschau! Er war noch viel zu jung um zu sterben.", description=f"Tschau {member.mention} hoffentlich kommst du bald zurück :(.", color=discord.Color.red(), member=member, image="leave")
        await bot.get_channel(welcome_channel).send(embed=emuser, file=file)
    else:
        logging.warning(f"{member} left from a Server that wasn´t configured")



if __name__ == '__main__':
    load_dotenv()
    # bot.load_extension(cogs.chat)
    bot.run(os.getenv("TESTTOKEN"))
