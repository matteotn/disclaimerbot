from pyrogram import Filters, Client


@Client.on_message(Filters.command("dissocio"))
def dissocio(client, message):
    message.delete()
    if message.reply_to_message is not None:
        message.reply_to_message.reply(f"[{message.from_user.first_name}](tg://user?id={message.from_user.id}) "
                                       f"si dissocia **completamente** da questo memino/affermazione.")