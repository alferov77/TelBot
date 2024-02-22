import telebot
from config import TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

keys = {
    ' - доллары': 'USD',
    ' - евро': 'EUR',
    ' - рубли': 'RUB',
}

@bot.message_handler(commands=['start', 'help'])
def start_help(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! '
                                      f'Для отображения актуального курса валют '
                                      f'напишите сообщение в виде (в строку через пробелы): '
                                      f'<имя валюты, цену которой он хочет узнать> '
                                      f'<имя валюты, в которой надо узнать цену первой валюты> '
                                      f'<количество первой валюты>. '
                                      f'Список всех доступных валют вы можете увидеть введя /values ')

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(func=lambda message: True)
def handle_messages(message: telebot.types.Message):
    chat_id = message.chat.id
    try:
        parts = message.text.lower().split()
        base_currency_name = keys.get(parts[0])
        target_currency_name = keys.get(parts[1])
        amount = int(parts[2])

        if not base_currency_name or not target_currency_name:
            raise APIException("Неверное имя валюты")

        rate = CurrencyConverter.get_exchange_rate(CurrencyConverter.api_key, base_currency_name, target_currency_name)
        converted_amount = amount * rate
        bot.send_message(chat_id, f"{amount} {base_currency_name} в {target_currency_name}: {converted_amount}")

    except APIException as e:
        bot.send_message(chat_id, f"Ошибка: {e.message}")

if __name__ == '__main__':
    bot.polling(none_stop=True)