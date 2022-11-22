# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de
# PUNYAALBY

from asyncio import sleep
from contextlib import suppress
from random import randint
from typing import Optional

from pyrogram import Client, filters
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import Message


from AdityaHalder.modules.helpers.basics import edit_or_reply
from AdityaHalder.modules.helpers.filters import command
from AdityaHalder.modules.helpers.command import commandpro
from AdityaHalder.utilities.misc import SUDOERS
from AdityaHalder.plugins.broadcast import *


async def get_group_call(
    client: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (await client.send(GetFullChannel(channel=chat_peer))).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.send(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await message.reply(f"**Tidak ada panggilan grup Ditemukan** {err_msg}")
    return False


@Client.on_message(
    filters.command("startvcs", ["."]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.command(["startvc"], [".", "-", "^", "!", "?"]) & filters.me)
async def opengc(client: Client, message: Message):
    flags = " ".join(message.command[1:])
    Cilik = await message.reply("💈 `Memproses!`")
    if flags == "channel":
        chat_id = message.chat.title
    else:
        chat_id = message.chat.id
    try:
        await client.send(
            CreateGroupCall(
                peer=(await client.resolve_peer(chat_id)),
                random_id=randint(10000, 999999999),
            )
        )
        await Cilik.edit(f"✅ Panggilan grup dimulai **Chat ID** : `{chat_id}`")
    except Exception as e:
        await Cilik.edit(f"**INFO:** `{e}`")


@Client.on_message(filters.command("stopvcs", ["."]) & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command(["stopvc"], [".", "-", "^", "!", "?"]) & filters.me)
async def end_vc_(client: Client, message: Message):
    """Mengakhiri panggilan grup"""
    chat_id = message.chat.id
    if not (
        group_call := (
            await get_group_call(client, message, err_msg=", group call already ended")
        )
    ):
        return
    await client.send(DiscardGroupCall(call=group_call))
    await message.reply(f"Panggilan grup berakhir **Chat ID** : `{chat_id}`")


@Client.on_message(
    filters.command("joinvcs", ["."]) & filters.user(DEVS) & ~filters.via_bot
)
@Client.on_message(filters.command("joinvc", [".", "-", "^", "!", "?"]) & filters.me)
async def joinvc(client: Client, message: Message):
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    if message.from_user.id != client:
        Cilik = await message.reply("💈 `Memproses!`")
    else:
        Cilik = await message.reply("💈 `Memproses!`")
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await client.group_call.start(chat_id)
    except Exception as e:
        return await Cilik.edit(f"**ERROR:** `{e}`")
    await Cilik.edit(f"✅ **Bergabung dengan Obrolan Suara**\n└ **Chat ID:** `{chat_id}`")
    await sleep(5)
    await client.group_call.set_is_mute(True)


@Client.on_message(
    filters.command("leavevcs", ["."]) & filters.user(DEVS) & ~filters.via_bot
)
@Client.on_message(filters.command("leavevc", [".", "-", "^", "!", "?"]) & filters.me)
async def leavevc(client: Client, message: Message):
    try:
        await client.group_call.stop()
    except Exception as e:
        return await message.reply(f"**ERROR:** `{e}`")
    await message.reply(
        f"✅ **Meninggalkan Obrolan Suara**\n└ **Chat ID:** `{message.chat.id}`"
    )


__MODULE__ = "vctools"
__HELP__ = f"""
**🥀 Hᴇʏ Hᴇʀᴇ Is Aʟʟ Aʙᴜsᴇ ✨**
**Cᴏᴍᴍᴀɴᴅs:**
`.startvc` - **Untuk Memulai voice chat group.**

`.stopvc` - **Untuk Memberhentikan voice chat group.**

`.joinvc` <chatid/username gc> - **Untuk Bergabung ke voice chat group**

`.leavevc` <chatid/username gc> - **Untuk Turun ke voice chat group**
"""
