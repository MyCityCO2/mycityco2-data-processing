import sys

import requests
from discord_webhook import DiscordEmbed, DiscordWebhook
from loguru import logger

from mycityco2_data_process import const


def send_ntfy(msg: str, title: str = const.settings.NTFY_TITLE):
    if const.settings.NTFY_TOGGLE:
        for topic in const.settings.NTFY_TOPICS:
            requests.post(
                const.settings.NTFY_SERVER + topic,
                data=msg.encode(encoding="utf-8"),
                headers={"Title": title, "Tags": "incoming_envelope"},
            )


def send_discord(
    msg: str,
    title: str = const.settings.NTFY_TITLE,
    username: str = "Importer Script",
    link: str = None,
):
    webhook_url = "https://discord.com/api/webhooks/1116702695630311497/7QY_2Il86MTi-E8206B7bS-UAKnDy4G5vyprFTYKja405RpCQxBJAl6rbVSAyiFfWB-b"
    webhook = DiscordWebhook(url=webhook_url)

    embed = DiscordEmbed(title=title, color=16712192, description=msg)

    if link:
        embed.set_url(link)

    webhook.add_embed(embed)

    webhook.execute()


def setup():
    ### Logger Params ###
    logger.remove()
    logger.add(
        sys.stdout,
        enqueue=True,
        colorize=True,
        format=const.settings.LOGORU_FORMAT,
        level="DEBUG",
    )
    # logger.add(sys.stdout, enqueue=True, colorize=True, format=const.settings.LOGORU_FORMAT, level=const.settings.LOGURU_LEVEL)
    # logger.add(lambda msg: send_ntfy(msg), format="{message}", colorize=False, level=const.settings.NTFY_LEVEL)

    logger.add(
        lambda msg: send_discord(msg),
        format="{message}",
        colorize=False,
        level="CRITICAL",
    )
    ### NTFY ###
    if const.settings.NTFY_TOGGLE:
        logger.debug(
            "Notification will be send to : \n{}".format(
                "\n".join(
                    [
                        "https://ntfy.sh/{}".format(topic)
                        for topic in const.settings.NTFY_TOPICS
                    ]
                )
            )
        )
