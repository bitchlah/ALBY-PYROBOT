import asyncio
import importlib
import os
import re

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pytgcalls import idle
from rich.console import Console
from rich.table import Table
from youtubesearchpython import VideosSearch

from AdityaHalder.config import LOG_GROUP_ID, STRING_SESSION
from AdityaHalder import client, robot, pytgcalls, ASSID, ASSNAME, BOT_ID, BOT_NAME, OWNER_ID
from AdityaHalder.modules.helpers.filters import command
from AdityaHalder.modules.helpers.decorators import errors, sudo_users_only
from AdityaHalder.plugins import ALL_MODULES
from AdityaHalder.utilities.inline import paginate_modules
from AdityaHalder.utilities.misc import SUDOERS

loop = asyncio.get_event_loop()
console = Console()
HELPABLE = {}

MSG_ON = """
**ALBY-PYROBOT DIAKTIFKAN**๐
      (\๏ธต/) 
ใโซบ( โขแบโข)โซน 
โโโช โโโโโโโ
โ  **Userbot Version -** `0.2.0@main`
โ  **Ketik** `.alby` **untuk Mengecheck Bot**
โโโโโโโโโโ
"""

async def initiate_bot():
    with console.status(
        "[magenta] Finalizing Booting...",
    ) as status:
        status.update(
            status="[bold blue]Scanning for Plugins", spinner="earth"
        )
        console.print("Found {} Plugins".format(len(ALL_MODULES)) + "\n")
        status.update(
            status="[bold red]Importing Plugins...",
            spinner="bouncingBall",
            spinner_style="yellow",
        )
        for all_module in ALL_MODULES:
            imported_module = importlib.import_module(
                "AdityaHalder.plugins." + all_module
            )
            if (
                hasattr(imported_module, "__MODULE__")
                and imported_module.__MODULE__
            ):
                imported_module.__MODULE__ = imported_module.__MODULE__
                if (
                    hasattr(imported_module, "__HELP__")
                    and imported_module.__HELP__
                ):
                    HELPABLE[
                        imported_module.__MODULE__.lower()
                    ] = imported_module
            console.print(
                f">> [bold cyan]Successfully imported: [green]{all_module}.py"
            )
        console.print("")
        status.update(
            status="[bold blue]Importation Completed!",
        )
    console.print(
        "[bold green] ๐ฅ ALBY PYROBOT Started โจ\n"
    )
    try:
        await robot.send_message(
            LOG_GROUP_ID,
            "<b> ๐ฅ ALBY PYROBOT is Here โจ</b>",
        )
    except Exception as e:
        print(
            "\nBot. Has Failed To Access The Log Group, Be Sure You Have Added Your Bot To Your Log Channel And Promoted As Adminโ"
        )
        console.print(f"\n[red] Stopping Bot")
        return
    a = await robot.get_chat_member(LOG_GROUP_ID, BOT_ID)
    if a.status != "administrator":
        print("Promote Bot As Admin in Logger Group")
        console.print(f"\n[red]sแดแดแดแดษชษดษข สแดแด")
        return
    console.print(f"\nโ[red] Bot Started as {BOT_NAME}")
    console.print(f"โ[green] ID :- {BOT_ID}")
    if STRING_SESSION != "None":
        try:
            await client.send_message(
                LOG_GROUP_ID, 
                MSG_ON,
            )
        except Exception as e:
            print(
                "\nUserBot Account Has Failed To Access The Log Group.โ"
            )
            console.print(f"\n[red] Stopping Bot")
            return
        try:
            await client.join_chat("ruangdiskusikami")
            await client.join_chat("ruangprojects")
        except:
            pass
        console.print(f"โ[red] UserBot Started as {ASSNAME}")
        console.print(f"โ[green] ID :- {ASSID}")
        console.print(f"โ[red] โ ALBY-PYROBOT Complete ๐ฏ ...")
        await idle()
        console.print(f"\n[red] Userbot Stopped")


home_text_pm = f"""**สแดสสแด ,
แดส ษดแดแดแด ษชs {BOT_NAME}.
I Aแด แดสสส แดสสแดสแดแด, Aษด Aแดแด แดษดแดแดแด UsแดสBแดแด Wษชแดส Sแดแดแด Usแดาแดส Fแดแดแดแดสแดs.**"""


@robot.on_message(command(["start"]) & filters.private)
async def start(_, message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/7b2a3fa167686dfaa3da8.jpg",
        caption=f"""**โโโโโโโโโโโโโโโโโโโโโโโโ
๐ฅ Hแดสสแด, I Aแด แดสสส แดสสแดสแดแด ยป Aษด Aแดแด แดษดแดแดแด
Pสแดแดษชแดแด Tแดสแดษขสแดแด Usแดส Bแดแด.

โโโโโโโโโโโโโโโโโโโโโ
โฃโ Oแดกษดแดส'xDโบ : [แดสสส](https://t.me/Punya_Alby)
โฃโ Uแดแดแดแดแดs โบโบ : [Uแดแดแดแดแดs](https://t.me/ruangprojects)
โฃโ Sแดแดแดแดสแด ยป : [Dษชsแดแดs](https://t.me/ruangdiskusikami)
โโโโโโโโโโโโโโโโโโโโโ

๐ Cสษชแดแด Oษด Dแดแดสแดส Bแดแดแดแดษด Tแด Mแดแดแด
Yแดแดส Oแดกษด ยป Gแดษดษชแดs Usแดส Bแดแด.
โโโโโโโโโโโโโโโโโโโโโโโโ**""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "๐ฅ Dแดแดสแดส Aสสส Pสสแดสแดแด โจ", url=f"https://github.com/PunyaAlby/ALBY-PYROBOT")
                ]
                
           ]
        ),
    )
    
    
    
@robot.on_message(command(["help"]) & SUDOERS)
async def help_command(_, message):
    text, keyboard = await help_parser(message.from_user.mention)
    await robot.send_message(LOG_GROUP_ID, text, reply_markup=keyboard)




async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        """**๐ฅ Wแดสแดแดแดแด Tแด Hแดสแด Mแดษดแด Oา :
Gแดษดษชแดs UsแดสBแดแด Vแดส : `2.0` ๐ฅ...

๐ Jแดsแด Cสษชแดแด Oษด Bแดสแดแดก Iษดสษชษดแด
Tแด Gแดแด Gแดษดษชแดs Cแดแดแดแดษดแดs โจ...**
""".format(
            first_name=name
        ),
        keyboard,
    )

@robot.on_callback_query(filters.regex("close") & SUDOERS)
async def close(_, CallbackQuery):
    await CallbackQuery.message.delete()

@robot.on_callback_query(filters.regex("aditya") & SUDOERS)
async def aditya(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await CallbackQuery.message.edit(text, reply_markup=keyboard)


@robot.on_callback_query(filters.regex(r"help_(.*?)") & SUDOERS)
async def help_button(client, query):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""**๐ฅ Wแดสแดแดแดแด Tแด Hแดสแด Mแดษดแด Oา :
Gแดษดษชแดs UsแดสBแดแด Vแดส : `2.0` ๐ฅ...

๐ Jแดsแด Cสษชแดแด Oษด Bแดสแดแดก Iษดสษชษดแด
Tแด Gแดแด Gแดษดษชแดs Cแดแดแดแดษดแดs โจ...**
 """
    if mod_match:
        module = mod_match.group(1)
        text = (
            "{} **{}**:\n".format(
                "**๐ฅ Wแดสแดแดแดแด Tแด Hแดสแด Mแดษดแด Oา :** ", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
        )
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="โช๏ธ สแดแดแด", callback_data="help_back"
                    ),
                    InlineKeyboardButton(
                        text="๐ แดสแดsแด", callback_data="close"
                    ),
                ],
            ]
        )

        await query.message.edit(
            text=text,
            reply_markup=key,
            disable_web_page_preview=True,
        )
    elif home_match:
        out = private_panel()
        await robot.send_message(
            query.from_user.id,
            text=home_text_pm,
            reply_markup=InlineKeyboardMarkup(out[1]),
        )
        await query.message.delete()
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    return await client.answer_callback_query(query.id)


if __name__ == "__main__":
    loop.run_until_complete(initiate_bot())
