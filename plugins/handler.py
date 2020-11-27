from pyrogram import Client, ChatPermissions

from bot import bot


def clear_user(client, hex, id_user, accept):
    if hex in bot.pending:
        if not accept:
            client.get_chat(bot.pending[hex]["chat_id"]).kick_member(id_user)
        else:
            client.get_chat(bot.pending[hex]["chat_id"]).restrict_member(
                id_user,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_stickers=True,
                    can_send_animations=True,
                    can_send_games=True,
                    can_use_inline_bots=True,
                    can_add_web_page_previews=True,
                    can_invite_users=True,
                    can_change_info=True,
                    can_send_polls=True,
                    can_pin_messages=True,
                ),
            )
        try:
            bot.scheduler.remove_job(f"{id_user}_{bot.pending[hex]['chat_id']}")
        except Exception as e:
            print(e)
        try:
            user = client.get_chat_member(
                bot.pending[hex]["chat_id"], bot.pending[hex]["user_id"]
            ).user
            client.edit_message_text(
                bot.pending[hex]["chat_id"],
                bot.pending[hex]["message_id"],
                f"L'utente [{user.first_name}](tg://user?id={user.id})"
                f"\n{'non ' if not accept else ''}ha accettato il disclaimer.\n{'È stato rimosso dal gruppo.' if not accept else ''}",
            )
        except Exception as e:
            print(e)
        del bot.pending[hex]


@Client.on_callback_query()
def callbackAnswer(client, callback_query):
    if "accept" in callback_query.data:
        hex = callback_query.data.split("_")[1]
        if (
            hex in bot.pending
            and bot.pending[hex]["user_id"] == callback_query.from_user.id
        ):
            callback_query.message.edit_text("Okay!\nHai accettato il disclaimer.\n")
            clear_user(client, hex, callback_query.from_user.id, True)
    elif "refuse" in callback_query.data:
        hex = callback_query.data.split("_")[1]
        if (
            hex in bot.pending
            and bot.pending[hex]["user_id"] == callback_query.from_user.id
        ):
            callback_query.message.edit_text(
                "Okay!\nHai rifiutato il disclaimer.\nVerrai rimosso dal gruppo."
            )
            clear_user(client, hex, callback_query.from_user.id, False)
