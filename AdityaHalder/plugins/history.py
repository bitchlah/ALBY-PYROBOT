import asyncio
from pyrogram import *
from pyrogram import filters
from pyrogram.types import *
from pyrogram.errors import RPCError
from AdityaHalder.modules.helpers.basics import edit_or_reply
from AdityaHalder.modules.helpers.filters import command
from AdityaHalder.modules.helpers.command import commandpro
from AdityaHalder.modules.helpers.decorators import sudo_users_only, errors
from AdityaHalder.utilities.misc import SUDOERS



@Client.on_message(filters.command(["sg", "sa", "sangmata"], [".", "-", "^", "!", "?"]) & SUDOERS & filters.me)
async def sg(client: Client, message: Message):
    lol = await message.reply("💈 `Harap Tunggu..`")
    if not message.reply_to_message:
        await lol.edit("reply to any message")
    reply = message.reply_to_message
    if not reply.text:
        await lol.edit("reply to any text message")
    chat = message.chat.id
    try:
        await client.send_message("@SangMataInfo_bot", "/start")
    except RPCError:
        await lol.edit("Please unblock @SangMataInfo_bot and try again")
        return
    await reply.forward("@SangMataInfo_bot")
    await asyncio.sleep(2)
    async for opt in client.iter_history("@SangMataInfo_bot", limit=3):
        hmm = opt.text
        if hmm.startswith("Forward"):
            await lol.edit("Bisakah Anda menonaktifkan pengaturan privasi Anda untuk selamanya?")
            return
        else:
            await lol.delete()
            await opt.copy(chat)



__MODULE__ = "Hɪsᴛᴏʀʏ"
__HELP__ = f"""
**🥀 Gᴇᴛ Nᴀᴍᴇ & Usᴇʀɴᴀᴍᴇ Hɪsᴛᴏʀʏ Oғ Aɴʏ Usᴇʀ ✨**

**ᴜsᴀɢᴇ:**
`.history` - **Rᴇᴘʟʏ Tᴏ Aɴʏ Usᴇʀ Tᴏ Gᴇᴛ Hɪsᴛᴏʀʏ.**
"""
