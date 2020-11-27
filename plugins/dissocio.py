import random

from pyrogram import Filters, Client

associo_words = [
    "[{}](tg://user?id={}) " f"supporta **a pieno** questo memino/affermazione."
]

dissocio_words = [
    "[{}](tg://user?id={}) "
    f"si dissocia **completamente** da questo memino/affermazione.",
    "In caso di un'indagine da parte di qualsiasi entità federale o simile, [{}](tg://user?id={}) "
    "**non ha alcun coinvolgimento con questo gruppo o con le persone in esso**,"
    " non so come è finito qui, probabilmente aggiunto da una terza parte, "
    "**non sostiene alcuna azione** dei membri di questo gruppo.",
]
sarcasm_words = [
    "[{}](tg://user?id={}) "
    f"afferma **fortemente** che questo memino/affermazione presenta del **sarcasmo** "
    f"([Che cos'è?](https://en.wikipedia.org/wiki/Sarcasm))."
]


@Client.on_message(Filters.command("dissocio"))
def dissocio(client, message):
    try:
        message.delete()
    except:
        pass
    if message.reply_to_message is not None:
        output = random.choice(dissocio_words)
        message.reply_to_message.reply(
            output.format(message.from_user.first_name, message.from_user.id),
            disable_web_page_preview=True,
        )


@Client.on_message(Filters.command("associo"))
def associo(client, message):
    try:
        message.delete()
    except:
        pass
    if message.reply_to_message is not None:
        output = random.choice(associo_words)
        message.reply_to_message.reply(
            output.format(message.from_user.first_name, message.from_user.id),
            disable_web_page_preview=True,
        )


@Client.on_message(Filters.command("s"))
def sarcasm(client, message):
    if message.reply_to_message is not None:
        try:
            message.delete()
        except:
            pass
        output = random.choice(sarcasm_words)
        message.reply_to_message.reply(
            output.format(message.from_user.first_name, message.from_user.id),
            disable_web_page_preview=True,
        )
