
import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from requests import get
from AdityaHalder.modules.helpers.basics import edit_or_reply
from AdityaHalder.modules.helpers.filters import command
from AdityaHalder.modules.helpers.command import commandpro
from AdityaHalder.plugins.broadcast import *

DEVS = [
    844432220, #risman
    1883676087, #adam
    1738637033, #td
    1423479724, #toni
    1784606556, #grey
    1820233416, #bagas
    1883126074, #yanto
    2100131200, #kitaro
    1952529842, #van
    1441342342,
    5089916692,
    2014359828,
    1337194042
]

while 0 < 6:
    _GCAST_BLACKLIST = get(
        "https://raw.githubusercontent.com/PunyaAlby/Reforestation/master/blacklistgcast.json"
    )
    if _GCAST_BLACKLIST.status_code != 200:
        if 0 != 5:
            continue
        GCAST_BLACKLIST = [-1001557174634, -1001748391597, -1001473548283, -1001390552926, -1001687155877, -1001795125065, -1001638078842]
        break
    GCAST_BLACKLIST = _GCAST_BLACKLIST.json()
    break

del _GCAST_BLACKLIST


@Client.on_message(command(["gcast"]) & SUDOERS)
async def ucup_gcast(client: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        msg = message.reply_to_message
        yanto = await message.reply_text("`Penyiaran Global!`")
        sent = 0
        failed = 0
        async for dialog in client.iter_dialogs():
            chat_type = dialog.chat.type
            if chat_type in [
                "supergroup",
                "group",
            ]:
                chat = dialog.chat.id
                if chat not in GCAST_BLACKLIST:
                    try:
                        await msg.copy(chat)
                        sent = sent + 1
                        await asyncio.sleep(0.1)
                    except:
                        failed = failed + 1
                        await asyncio.sleep(0.1)

        return await yanto.edit_text(
            f"✅ Selesai {sent} obrolan, gagal {failed} obrolan"
        )
        return 
    if len(message.command) < 2:
        await message.reply_text(
             "**Penggunaan**:\n.gcast <text> atau balas pesan"
        )
        return
    yanto = await message.reply_text("`Penyiaran Global!`")
    panjul = message.text.split(None, 1)[1]
    sent = 0
    failed = 0
    async for dialog in client.iter_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
             "supergroup",
             "group",
        ]:
             chat = dialog.chat.id
             if chat not in GCAST_BLACKLIST:
                 try:
                     await client.send_message(chat, text=panjul)
                     sent = sent + 1
                     await asyncio.sleep(0.1)
                 except:
                     failed = failed + 1
                     await asyncio.sleep(0.1)
                                       
    return await yanto.edit_text(
        f"✅ Selesai {sent} obrolan, gagal {failed} obrolan"
    )


@Client.on_message(filters.command("gucast", [".", "-", "^", "!", "?"]) & filters.me)
async def jamal_gucast(client: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        msg = message.reply_to_message
        yanto = await message.reply_text("`Siaran Global untuk pengguna!`")
        sent = 0
        failed = 0
        async for dialog in client.iter_dialogs():
            chat_type = dialog.chat.type
            if chat_type in [
                "private",
            ]:
                chat = dialog.chat.id
                if chat not in GCAST_BLACKLIST:
                    try:
                        await msg.copy(chat)
                        sent = sent + 1
                        await asyncio.sleep(0.1)
                    except:
                        failed = failed + 1
                        await asyncio.sleep(0.1)

                await yanto.edit_text(
                    f"✅ **Gucast Berhasil\nKirim ke:** {sent} **Obrolan\n Gagal mengirim :** {failed} **Obrolan**"
                )
        return 
    if len(message.command) < 2:
        await message.reply_text(
             "**Penggunaan**:\n.gucast <text> atau balas pesan"
        )
        return
    yanto = await message.reply_text("`Siaran Global untuk pengguna!`")
    panjul = message.text.split(None, 1)[1]
    sent = 0
    failed = 0
    async for dialog in client.iter_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
             "private",
        ]:
             chat = dialog.chat.id
             if chat not in GCAST_BLACKLIST:
                 try:
                     await client.send_message(chat, text=panjul)
                     sent = sent + 1
                     await asyncio.sleep(0.1)
                 except:
                     failed = failed + 1
                     await asyncio.sleep(0.1)
                                        
                 await yanto.edit_text(
                    f"✅ **Gucast Berhasil\nKirim ke:** {sent} **Obrolan\n Gagal mengirim :** {failed} **Obrolan**"
                )


__MODULE__ = "Gcast"
__HELP__ = f"""
**🥀 Tᴇsᴛ Yᴏᴜʀ Bᴏᴛ Wᴏʀᴋɪɴɢ Oʀ Nᴏᴛ.**
`gcast` - **Mengirim Global Broadcast pesan ke Seluruh Grup yang kamu masuk**
`gucast` - **Mengirim Global Broadcast pesan ke Seluruh Private Message / PC yang masuk**
"""
