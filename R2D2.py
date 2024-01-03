import telebot
from config import keys
import os
from dotenv import load_dotenv, find_dotenv
from extensions import ApiExeption, CriptoConverter

load_dotenv(find_dotenv())

# CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker",
#                  "video", "video_note", "voice", "location", "contact",
#                  "new_chat_members", "left_chat_member", "new_chat_title",
#                  "new_chat_photo", "delete_chat_photo",
#                  "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
#                  "migrate_from_chat_id", "pinned_message"]


bot = telebot.TeleBot(os.getenv('TOKEN'))


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=["start", "help"])
def handle_start_help(message: telebot.types.Message):
    bot.reply_to(message, "-Чтобы произвести обмен валют отправьте сообщение \
боту в виде <имя валюты, цену которой хотите узнать> <имя валюты, в которой надо \
узнать цену первой валюты> <количество первой валюты> через пробел \n-Наберите /start \
или /help чтобы ознакомиться с инструкцией. \n-Команда /values - позволит увидеть перечень \
доступных для обмена валют.")


# Обрабатывается все документы и аудиозаписи
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message: telebot.types.Message):
    bot.reply_to(message, "-Мною не предусмотрено чтенние данных из подобных файлов")


@bot.message_handler(content_types=['voice', ])
def voice(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'У тебя очень красивый голос!')


@bot.message_handler(content_types=['photo', ])
def say_lmao(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Nice meme XDD')


@bot.message_handler(commands=["values"])
def handle_values(message: telebot.types.Message):
    text = "Доступны следующие валюты:"
    for key in keys.keys():
        text = "\n".join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ApiExeption("Количество параметров не соответсвует требуемому \n \
Я бы хотел с Вами поговорить на разные темы, но я создан лишь предоставлять курсы валют, \
если Вы видите это сообщение-проверте правописание введеных доступных валют.")
        base, quote, amount = values
        total_base = CriptoConverter.get_price(base, quote, amount)
    except ApiExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')
    except Exception as e:
        bot.reply_to(message.chat.id, f'Не удалось обработать команду\n {e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
