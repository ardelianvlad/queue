import telebot
from dao import DBdao as db
from models import Person, Queue
import config

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["queue"])
def new_queue(message):
    try:
        name = " ".join(message.text.split()[1:])
    except Exception as e:
        print(e)
        name = ""
    queue = Queue(name)
    added = db._add_queue(queue)
    if not added:
        bot.send_message(message.chat.id, "Така черга вже існує")
    else:
        qid = db.get_queue_id(queue)
        keyboard = telebot.types.InlineKeyboardMarkup()
        callback_button = telebot.types.InlineKeyboardButton(text="Зайняти чергу", callback_data=str(qid))
        keyboard.add(callback_button)
        bot.send_message(message.chat.id, "Черга «" + queue.name + "»", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        qid = int(call.data)
        queue = db.get_queue(qid)
        user = call.from_user
        first_name = user.first_name or "Anonymous"
        last_name = user.last_name or ""
        new_user = Person(user.id, first_name, last_name)
        order = db.get_order(queue)
        for person in order:
            if person[1] == new_user.id:
                bot.answer_callback_query(call.id)
                return
        else:
            db.add_order(new_user, queue)
        text = "Черга «" + queue.name + "»\n"
        order = db.get_order(queue)
        for i in range(len(order)):
            item = order[i]
            text += str(item[0] + 1) + ". " + item[2] + " " + item[3] + "\n"
        keyboard = telebot.types.InlineKeyboardMarkup()
        callback_button = telebot.types.InlineKeyboardButton(text="Зайняти чергу", callback_data=str(qid))
        keyboard.add(callback_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)
