import sys

from discord_webhook import DiscordEmbed, DiscordWebhook
from loguru import logger

from mycityco2_data_process import const


def send_discord(
    msg: str,
    title: str = "MyCityCO2 Importer",
    username: str = "Importer Script",
    link: str = None,
):
    webhook_url = "https://discord.com/api/webhooks/1116702695630311497/7QY_2Il86MTi-E8206B7bS-UAKnDy4G5vyprFTYKja405RpCQxBJAl6rbVSAyiFfWB-b"
    webhook = DiscordWebhook(url=webhook_url, username=username)

    embed = DiscordEmbed(title=title, color=16712192, description=msg)

    if link:
        embed.set_url(link)

    webhook.add_embed(embed)

    webhook.execute()


def setup(level: const.LogLevels = "DEBUG"):
    # Logger Params
    logger.remove()

    logger.level("FTRACE", no=3, color="<blue>")

    logger.add(
        sys.stdout,
        enqueue=True,
        colorize=True,
        format=const.settings.LOGORU_FORMAT,
        level=level,
    )
