import telebot
from config import keys, TOKEN
from extensions import ConvertionExeption, CriptoConvertor

bot = telebot.TeleBot(TOKEN)

# Обрабатываются сообщения, содержащие команду '/start'
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Привет! Я Бот-Конвертер валют и я могу:  \n- Показать список доступных валют: /values \
    \n- Вывести конвертацию валюты через команду: \n <имя валюты> \n <в какую валюту перевести> \n <количество переводимой валюты>\n \
- Напомнить, что я могу: /help'
    bot.reply_to(message, text)

# Обрабатываются сообщения, содержащие команду '/help'
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите комманду в формате:\n <имя валюты> \n <в какую валюту перести>\n <количество переводимой валюты>\
    \nУвидеть список всех доступных валют /values"
    bot.reply_to(message, text)

# Обрабатываются сообщения, содержащие команду '/values'
@bot.message_handler(commands=['values'])
def velues(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        velues = message.text.split(' ')

        if len(velues) != 3:
            raise ConvertionExeption('Слишком много параметров. /help')

        quote, base, amount = velues
        total_base = CriptoConvertor.convert(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
