import sys

from discord_webhook import DiscordEmbed, DiscordWebhook
from loguru import logger

from mycityco2_data_process import const

ERROR_WEBHOOK: str = "https://discord.com/api/webhooks/1126053816933031948/i_thhdAox3mNfzlz4vBPdFUxmocVKYQLXhBkSD-znn524WXdPja9-0fXuy5yyVmHNJ69"
ALERT_WEBHOOK: str = "https://discord.com/api/webhooks/1116702695630311497/7QY_2Il86MTi-E8206B7bS-UAKnDy4G5vyprFTYKja405RpCQxBJAl6rbVSAyiFfWB-b"


def send_discord(
    msg: str,
    title: str = "MyCityCO2 Importer",
    username: str = "Importer Script",
    link: str = None,
    error: bool = False,
):
    if error:
        webhook_url = ERROR_WEBHOOK
    else:
        webhook_url = ALERT_WEBHOOK
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
        backtrace=True,
        diagnose=True,
        colorize=True,
        format=const.settings.LOGORU_FORMAT,
        level=level,
    )
