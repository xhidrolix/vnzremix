# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to the \
    Information Superhighway (yes, Internet). """

import speedtest
import time
from telethon import functions
from datetime import datetime
from userbot import StartTime, bot, CMD_HELP
from userbot.events import register


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(
            seconds, 60) if count < 3 else divmod(
            seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


def speed_convert(size):
    """
    Hi human, you can't read bytes?
    """
    power = 2**10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


@register(outgoing=True, pattern="^.speed$")
async def _(event):
    if event.fwd_from:
        return
    await event.edit("`Test Speed Internet connection` ⚡")
    start = datetime.now()
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    client_infos = response.get("client")
    i_s_p = client_infos.get("isp")
    i_s_p_rating = client_infos.get("isprating")
    response = s.results.share()
    speedtest_image = response
    output = (f"**SpeedTest** completed in {ms}ms\n\n"
              f"`•Download: {speed_convert(download_speed)}\n`"
              f"`•Upload: {speed_convert(upload_speed)}\n`"
              f"`•Ping: {ping_time}\n`"
              f"`•ISP: {i_s_p}\n`"
              f"`•ISP Rating: {i_s_p_rating}\n\n`"
              "**POWERED BY XBOT REMIX 🔥**")
    await bot.send_file(
        event.chat_id,
        speedtest_image,
        caption=output,
        force_document=False,
        allow_cache=False
    )
    await event.delete()


@register(outgoing=True, pattern="^.ping$")
async def pingme(pong):
    """ For .ping command, ping the userbot from any chat.  """
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit("`Pinging....`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(f"**PONG!! 🍭**\n**Pinger** : %sms\n**Bot Uptime** : {uptime}🕛" % (duration))


@register(outgoing=True, pattern="^.pong$")
async def pingme(pong):
    """ For .ping command, ping the userbot from any chat.  """
    start = datetime.now()
    await pong.edit("`gass!`")
    end = datetime.now()
    duration = (end - start).microseconds / 9000
    await pong.edit("`Ping!\n%sms`" % (duration))


@ register(outgoing=True, pattern="^.pink$")
async def pingme(pong):
    """ For .ping command, ping the userbot from any chat.  """
    start = datetime.now()
    await pong.edit("`Croots!`")
    end = datetime.now()
    duration = (end - start).microseconds / 9000
    await pong.edit("**CROOTSS!\n%sms**" % (duration))


@register(outgoing=True, pattern="^.dc$")
async def neardc(event):
    """ For .dc command, get the nearest datacenter information. """
    result = await event.client(functions.help.GetNearestDcRequest())
    await event.edit(f"Country : `{result.country}`\n"
                     f"Nearest Datacenter : `{result.nearest_dc}`\n"
                     f"This Datacenter : `{result.this_dc}`\n\n"
                     "**List Of Telegram Data Centres:**\n"
                     "**DC1 : Miami FL, USA**\n"
                     "**DC2 : Amsterdam, NL**\n"
                     "**DC3 : Miami FL, USA**\n"
                     "**DC4 : Amsterdam, NL**\n"
                     "**DC5 : Singapore, SG**\n")

CMD_HELP.update(
    {"ping": "`.ping`\
    \nUsage: Shows how long it takes to ping your bot.\
    \n\n`.speed`\
    \nUsage: Does a speedtest and shows the results.\
    \n\n`.pong`\
    \nUsage: Shows how long it takes to ping your bot.\
    \n\n`.dc`\
    \nUsage: Shows your telegram datacenter."
     })
