import datetime

from pyrogram import Client, Filters, ChatPermissions
from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton
from bot import bot
import uuid
import time


def current_time(): return int(round(time.time()))


def ban_log(client, hex, id_user):
    if hex in bot.pending:
        client.get_chat(bot.pending[hex]['chat_id']).kick_member(id_user)
        user = client.get_chat_member(bot.pending[hex]['chat_id'], bot.pending[hex]['user_id']).user
        try:
            client.edit_message_text(bot.pending[hex]['chat_id'], bot.pending[hex]['message_id'],
                                     f"L'utente [{user.first_name}](tg://user?id={user.id}) "
                                     f"\nnon ha accettato i termini entro il tempo previsto.\nL'ho rimosso dal gruppo.")
        except Exception as e:
            print(e)
        del bot.pending[hex]


def uuid_gen(user, chat_id) -> str:
    rand_str = uuid.uuid4().hex
    bot.pending[rand_str] = {
        'user_id': user.id,
        'date': current_time(),
        'chat_id': chat_id
    }
    return rand_str


def update_msg_id(hex, message_id):
    bot.pending[hex]['message_id'] = message_id


def is_valid(hex, seconds=300):
    return current_time() - bot.pending[hex]['date'] <= seconds


def timer_set(id_task: str, job, args: list, seconds=300):
    timer = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    bot.scheduler.add_job(job, 'date', run_date=timer, id=id_task, args=args, replace_existing=True)


@Client.on_message((Filters.group & Filters.new_chat_members) | Filters.command('disclaimer'), group=-1)
def handlerJoin(client, message):
    if message.chat.id == -1001128902578 or message.chat.id == -1001244432522:  # speck and memes or debug
        if message.new_chat_members is not None:
            new_chat_members = message.new_chat_members
        elif message.reply_to_message is not None and bot.admin(message.from_user.id):
            message.delete()
            new_chat_members = [message.reply_to_message.from_user]
        else:
            message.delete()
            new_chat_members = [message.from_user]
        for user in new_chat_members:
            if not user.is_self:
                if not bot.admin(user.id):
                    try:
                        message.chat.restrict_member(user.id, ChatPermissions(can_send_messages=False))

                        uuid_generated = uuid_gen(user, message.chat.id)
                        msg = message.reply(bot.settings['welcome'].format(message.chat.title, user.first_name,
                                                                           user.id) if 'welcome' in bot.settings else 'Welcome',
                                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                                                text="Click Me",
                                                url=f"https://t.me/{bot.settings['my_username']}?start={uuid_generated}"
                                            )]]))
                        update_msg_id(uuid_generated, msg.message_id)
                        timer_set(f"{user.id}_{message.chat.id}", ban_log, args=[client, uuid_generated, user.id])
                        timer_set(f"{message.message_id}_{message.chat.id}", message.delete, args=[])
                    except Exception as e:
                        print(e)

                else:
                    message.reply(
                        f"Un amministratore è entrato nel gruppo. Salutate [{message.from_user.first_name}](tg://user?id={message.from_user.id})!")


@Client.on_message(Filters.command("start") & Filters.private)
def start(client, message):
    split = message.text.split()
    if len(split) == 2:
        if split[1] in bot.pending and message.from_user.id == bot.pending[split[1]]['user_id']:
            if is_valid(split[1]):
                message.reply(bot.settings['disclaimer'], reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        text='Accetto',
                        callback_data=f"accept_{split[1]}"
                    )],
                    [InlineKeyboardButton(
                        text='Declino',
                        callback_data=f"refuse_{split[1]}"
                    )]
                ]), disable_web_page_preview=True)
            else:
                message.reply("Il link non è più valido.")
