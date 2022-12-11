import telebot
from config import keys, TOKEN
from extensions import ConvertationException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start',])
def start(message: telebot.types.Message):
    text = f'Доброго времени суток, {message.chat.username}, с вами Бот Счетовод! Я конвертирую криптовалюты.\nДля того, чтобы начать работу выберите команду:\n/help - для получения инструкции по работе с ботом\n/values - для получения списка доступных валют'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help',])
def help(message: telebot.types.Message):
    text = "Для начала конвертации валют введите данные в следующем формате:\n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message:telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertationException('Неверное количество параметров.')
        quote, base, amount = values
        total_base = CurrencyConverter.convert(quote, base, amount)
    except ConvertationException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Переводим {quote} в {base}\n{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)

bot.polling()