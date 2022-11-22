
import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from requests import get
from AdityaHalder.modules.helpers.basics import edit_or_reply
from AdityaHalder.modules.helpers.filters import command
from AdityaHalder.modules.helpers.command import commandpro
from AdityaHalder.utilities.misc import SUDOERS

@Client.on_message(filters.me & filters.command(["delspam", "deletespam"], [".", "-", "^", "!", "?"]))
async def statspam(client: Client, message: Message):
    yanto = await message.reply_text("💡 Penggunaan:\n `.delspam 10 ALBY`")
    quantity = message.command[1]
    spam_text = ' '.join(message.command[2:])
    quantity = int(quantity)
    await message.delete()
    for i in range(quantity):
        await yanto.delete()
        msg = await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(0.1)
        await msg.delete()
        await asyncio.sleep(0.1)


@Client.on_message(filters.me & filters.command("spam", [".", "-", "^", "!", "?"]))
async def sspam(client: Client, message: Message):
    yanto = await message.reply_text("💡 Penggunaan:\n `.spam 10 ALBY`")
    quantity = message.command[1]
    spam_text = ' '.join(message.command[2:])
    quantity = int(quantity)

    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
        for _ in range(quantity):
            await client.send_message(message.chat.id, spam_text,
                                      reply_to_message_id=reply_to_id)
            await asyncio.sleep(0.15)
        return

    for _ in range(quantity):
        await yanto.delete()
        await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(0.15)


@Client.on_message(filters.me & filters.command(["fastspam", "fspam"], [".", "-", "^", "!", "?"]))
async def fastspam(client: Client, message: Message):
    yanto = await message.reply_text("💡 Penggunaan:\n `.fspam 10 ALBY`")
    quantity = message.command[1]
    spam_text = ' '.join(message.command[2:])
    quantity = int(quantity)
    
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
        for _ in range(quantity):
            await client.send_message(message.chat.id, spam_text,
                                      reply_to_message_id=reply_to_id)
            await asyncio.sleep(0.002)
        return
    
    for _ in range(quantity):
        await yanto.delete()
        await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(0.002)


@Client.on_message(filters.command(["ds", "delayspam"], [".", "-", "^", "!", "?"]) & filters.me)
async def delayspam(client, message):
    chat = message.chat.id
    cilik = "".join(message.text.split(maxsplit=1)[1:]).split(" ", 2)
    userbot = cilik[1:]
    jumlah = int(cilik[0])
    waktu = float(userbot[0])
    pesan = str(userbot[1])
    kk = await message.edit(f"Mulai tunda jumlah spam pesan {jumlah} bersama waktu {waktu}")
    for _ in range(jumlah):
        await client.send_message(chat, pesan)
        await sleep(waktu)
        await kk.delete()
            

@Client.on_message(filters.me & filters.command(["sspam", "stkspam", "spamstk", "stickerspam"], [".", "-", "^", "!", "?"]))
async def spam_stick(client: Client, message: Message):
    if not message.reply_to_message:
        await message.edit_text("Bala ke stiker!")
        return
    if not message.reply_to_message.sticker:
        await message.edit_text(text="**balas stiker dengan jumlah yang ingin Anda spam**")
        return
    else:
        i=0
        times = message.command[1]
        if message.chat.type in ["supergroup", "group"]:
            for i in range(int(times)):
                sticker=message.reply_to_message.sticker.file_id
                await client.send_sticker(
                    message.chat.id,
                    sticker,
                )
                await asyncio.sleep(0.10)

        if umm.chat.type == "private":
            for i in range(int(times)):
                sticker=message.reply_to_message.sticker.file_id
                await client.send_sticker(
                    message.chat.id, sticker
                )
                await asyncio.sleep(0.10)


__MODULE__ = "Spam"
__HELP__ = f"""
**🥀 Tᴇsᴛ Yᴏᴜʀ Bᴏᴛ Wᴏʀᴋɪɴɢ Oʀ Nᴏᴛ.**
`delspam` - **It will Spam then delete it's spam automatically**
`spam` - **Spam Your Custom Message**
`sspam [reply to sticker]` - **Sticker Spam.**
`ds or delayspam  [Jumlah] [Waktu] [Text]` - **Spam text by amount and time**
`fspam or fastspam` - **Spam Your message fastly.**
"""
