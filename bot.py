import telebot
from telebot import types

# Создаем бота
bot = telebot.TeleBot('7300893052:AAG5Ofg9hYEqq2B0oXof1o4MS2ldH0lrwt8')

# Словарь для хранения состояния пользователя
user_data = {}

# Список городов и их геолокаций
cities = {
    'Almaty': {'latitude': 43.238949, 'longitude': 76.889709},
    'Astana': {'latitude': 51.169392, 'longitude': 71.449074},
    'Shymkent': {'latitude': 42.341675, 'longitude': 69.590099},
    'Karaganda': {'latitude': 49.801868, 'longitude': 73.102134},
    'Aktobe': {'latitude': 50.283937, 'longitude': 57.167034},
}

@bot.message_handler(commands=['start'])
def mes_start(message):
    # Инициализация состояния для пользователя
    user_data[message.chat.id] = {'country': None, 'city': None}
    
    # Создаем клавиатуру с выбором страны
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Казахстан', callback_data='button_1')
    markup.add(button1)
    
    bot.reply_to(message, 'Привет! Это бот, который покажет тебе точки переработки!')
    bot.reply_to(message, 'Выбери свою страну!', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    
    # Если пользователь выбрал Казахстан
    if call.data == 'button_1':
        bot.answer_callback_query(call.id, 'Вы выбрали Казахстан')
        bot.send_message(chat_id, 'Отлично! Ваша страна: Казахстан')
        
        # Обновляем состояние пользователя
        user_data[chat_id]['country'] = 1
        
        # Предлагаем выбрать город
        markup1 = types.InlineKeyboardMarkup()
        for city in cities.keys():
            markup1.add(types.InlineKeyboardButton(city, callback_data=f'city_{city}'))
        bot.send_message(chat_id, 'Выберите ваш город:', reply_markup=markup1)
    
    # Если пользователь выбрал город
    elif call.data.startswith('city_'):
        selected_city = call.data.split('_')[1]  # Извлекаем название города
        bot.answer_callback_query(call.id, f'Вы выбрали {selected_city}')
        bot.send_message(chat_id, f'Отлично! Ваш город: {selected_city}')
        print(call)
        
        # Обновляем состояние пользователя
        user_data[chat_id]['city'] = selected_city
        
        # Проверяем условия и отправляем геолокацию
        if user_data[chat_id]['country'] == 1 and selected_city in cities:
            location = cities[selected_city]
            bot.send_message(chat_id, f'Точка переработки в городе {selected_city}:')
            bot.send_location(chat_id, location['latitude'], location['longitude'])

# Запуск бота
bot.infinity_polling()



