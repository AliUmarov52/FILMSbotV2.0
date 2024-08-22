# Импорт Библиотек
import telebot  
from telebot import types  
import sqlite3
import random

# Тут Токен
bot = telebot.TeleBot("YOUR_TOKEN")  

# Подключаем базу данных
def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY
    )
    ''')
    conn.commit()
    conn.close()  # Закрываем соединение


# Добавление пользователя в базу данных
def add_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()


@bot.message_handler(commands=['users_admin'])
def list_users(message):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users')
    users = cursor.fetchall()
    conn.close()  # Закрываем соединение
    user_ids = [str(user[0]) for user in users]
    bot.send_message(message.chat.id, "Список пользователей:\n" + "\n".join(user_ids))


def start_markup():  
    markup = types.InlineKeyboardMarkup(row_width=1)  
    link_keyboard = types.InlineKeyboardButton(text="1-й Канал", url="https://t.me/kinorap")    
    check = types.InlineKeyboardButton(text="Проверить подписку", callback_data="check")  
    markup.add(link_keyboard, check)  
    return markup  


@bot.message_handler(commands=['start'])  
def start(message):  
    chat_id = message.chat.id  
    first_name = message.chat.first_name  
    bot.send_message(chat_id, f"Привет, {first_name}!\nЧтобы пользоваться этим ботом, подпишись на канал/каналы.", reply_markup=start_markup())  
    user_id = message.from_user.id
    add_user(user_id)



def check_subscription(chat_id, channel_id):  
    try:  
        member = bot.get_chat_member(chat_id=channel_id, user_id=chat_id)  
        return member.status in ['creator', 'administrator', 'member']  
    except Exception:  
        return False  


@bot.callback_query_handler(func=lambda call: call.data == 'check')  
def callback_check(call):  
    chat_id = call.message.chat.id  
    channel1 = "-1002219725769" # ID первого канала  
      # ID второго канала  
    if check_subscription(chat_id, channel1):  
        bot.send_message(chat_id, "Вы подписаны на канал. Спасибо!") 
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id) # Исправлено
        welcome(call.message)  # Вызов функции для возврата в главное меню
    else:  
        bot.send_message(chat_id, "Подпишитесь на канал, чтобы использовать бота.", reply_markup=start_markup()) 


# Главное меню
@bot.message_handler(func=lambda message: message.text == 'Главное меню')  
def welcome(message):  
    markup = types.InlineKeyboardMarkup(row_width=2) 
    button1 = types.InlineKeyboardButton('Поиск по жанрам', callback_data='Поиск по жанрам') 
    button2 = types.InlineKeyboardButton('Поиск по коду', callback_data='Поиск по коду') 
    button3 = types.InlineKeyboardButton('ТГК с фильмами', callback_data='ТГК с фильмами') 
    button4 = types.InlineKeyboardButton('Поиск по названию', callback_data='Поиск по названию') 
    button5 = types.InlineKeyboardButton('Новинки 2024', callback_data='Новинки 2024') 
    button6 = types.InlineKeyboardButton('Настройки', callback_data='Настройки') 
    markup.add(button5) 
    markup.add(button1, button2, button4) 
    markup.add(button3, button6)  # Главные кнопки меню
    
    chat_id = call.message.chat.id  
    channel1 = "-1002219725769" # ID первого канала
    if check_subscription(chat_id, channel1):
        bot.send_message(message.chat.id, f'Привет, КИНОМАН!\nМеня зовут ФИЛЬМОБОТ и я твой проводник в мир кино и сериалов :)\nДля начала выбери способ поиска фильма в меню ниже: ', reply_markup=markup) 
    else:  
        bot.send_message(chat_id, "Подпишитесь на канал, чтобы использовать бота.", reply_markup=start_markup()) 


def welcome1(message):
    chat_id = call.message.chat.id  
    channel1 = "-1002219725769" # ID первого канала
    markup = types.InlineKeyboardMarkup(row_width=2) 
    button1 = types.InlineKeyboardButton('Поиск по жанрам', callback_data='Поиск по жанрам') 
    button2 = types.InlineKeyboardButton('Поиск по коду', callback_data='Поиск по коду') 
    button3 = types.InlineKeyboardButton('ТГК с фильмами', callback_data='ТГК с фильмами') 
    button4 = types.InlineKeyboardButton('Поиск по названию', callback_data='Поиск по названию') 
    button5 = types.InlineKeyboardButton('Новинки 2024', callback_data='Новинки 2024') 
    button6 = types.InlineKeyboardButton('Настройки', callback_data='Настройки') 
    markup.add(button5) 
    markup.add(button1, button2, button4) 
    markup.add(button3, button6)  # Главные кнопки меню 

    if check_subscription(chat_id, channel1):
        bot.send_message(message.chat.id, "Вы переместились в главное меню. Выберите опцию ниже: ", reply_markup=markup)
    else:  
        bot.send_message(chat_id, "Подпишитесь на канал, чтобы использовать бота.", reply_markup=start_markup()) 


@bot.callback_query_handler(func=lambda call: True)
def info(call):
    chat_id = call.message.chat.id  
    channel1 = "-1002219725769" # ID первого канала
    if check_subscription(chat_id, channel1):
        if call.data == 'Поиск по коду':
            bot.send_message(call.message.chat.id, "Введите номер фильма:")
            bot.register_next_step_handler(call.message, search)
        elif call.data == 'ТГК с фильмами':
            tgk(call.message)
        elif call.data == 'Настройки':
            settings(call.message)
        elif call.data == 'Поиск по жанрам':
            bot.send_message(call.message.chat.id, "Введите жанр фильма:\n\nДоступные жанры: Драма, Ужасы, Фантастика, Комедия, Романтика, Вестерн, Криминал, Боевик, Триллер, Биография\n\nP.s Вводите жанр правильно")
            bot.register_next_step_handler(call.message, searchGenre)  # Возвращаемся в главное меню
        elif call.data == 'Поиск по названию':
            bot.send_message(call.message.chat.id, "Введите название фильма:")
            bot.register_next_step_handler(call.message, searchName)
        elif call.data == 'Новинки 2024':
            newFilms(call.message)
        else:
            welcome1(call.message)
    else:  
        bot.send_message(chat_id, "Подпишитесь на канал, чтобы использовать бота.", reply_markup=start_markup()) 

my_dict = {
    1: {
        "Название": "Интерстеллар",
        "Описание": "Космическая одиссея о группе астронавтов, которые исследуют червоточину в поисках нового дома для человечества.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0816692/",
        "Жанр": "Фантастика",
        "Код": "1",
        "Ссылка": "https://t.me/c/2178525944/17",
        "Трейлер": "https://www.youtube.com/watch?v=6ybBuTETr3U",
        "Скачать": ""
        
    },
    2: {
        "Название": "Начало",
        "Описание": "Вор, специализирующийся на краже идей, получает задание внедриться в сознание человека и изменить его мысли.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt1375666/",
        "Жанр": "Фантастика",
        "Код": "2",
        "Ссылка": "https://t.me/c/2178525944/19",
        "Трейлер": "https://www.youtube.com/watch?v=85Zz1CCXyDI",
        "Скачать": ""
        
    },
    3: {
        "Название": "Матрица",
        "Описание": "Программист Нейо узнает о правде о своей реальности и о том, что он может изменить мир.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0133093/",
        "Жанр": "Фантастика",
        "Код": "3",
        "Ссылка": "https://t.me/c/2178525944/21",
        "Трейлер": "https://www.youtube.com/watch?v=YihPA42fdQ8",
        "Скачать": ""
        
    },
    4: {
        "Название": "Побег из Шоушенка",
        "Описание": "История о дружбе двух заключенных, которые пытаются сбежать из тюрьмы Шоушенк.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0111161/",
        "Жанр": "Драма",
        "Код": "4",
        "Ссылка": "https://t.me/c/2178525944/23",
        "Трейлер": "https://www.youtube.com/watch?v=kgAeKpAPOYk",
        "Скачать": ""
        
    },
    5: {
        "Название": "Сияние",
        "Описание": "Писатель с семьей становится смотрителем у отеля, где начинают происходить странные события.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0081505/",
        "Жанр": "Ужасы",
        "Код": "5",
        "Ссылка": "https://t.me/c/2178525944/25",
        "Трейлер": "https://www.youtube.com/watch?v=bDj1El1Sr5A",
        "Скачать": ""
        
    }, 
    6: {
        "Название": "Тупой и ещё тупее",
        "Описание": "После того, как женщина оставляет портфель в терминале аэропорта, тупой водитель лимузина и его еще более тупой друг отправляются в веселую поездку по пересеченной местности в Аспен, чтобы вернуть его.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0109686/",
        "Жанр" : "Комедия",
        "Код": "6",
        "Ссылка": "https://t.me/c/2178525944/27",
        "Трейлер": "https://www.youtube.com/watch?v=zd__P3giExg",
        "Скачать": ""
        
    },
    7: {
        "Название": "Красавица и чудовище",
        "Описание": "Принц, обреченный провести свои дни в образе отвратительного монстра, намеревается вернуть себе человечность, завоевав любовь молодой женщины.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt2771200/",
        "Жанр": "Романтика",
        "Код": "7",
        "Ссылка": "https://t.me/c/2178525944/29",
        "Трейлер": "https://www.youtube.com/watch?v=MgVBTUJgsUs",
        "Скачать": ""
    },
    8: {
        "Название": "Звонок",
        "Описание": "Журналист должен расследовать загадочную видеозапись, которая, по-видимому, может стать причиной смерти любого человека через неделю или день после ее просмотра.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0298130/",
        "Жанр": "Ужасы",
        "Код": "8",
        "Ссылка": "https://t.me/c/2178525944/31",
        "Трейлер": "https://www.youtube.com/watch?v=evQ3yB8JbHA",
        "Скачать": ""
        
    },
    9: {"Название": "Кошмар на улице Вязов",
        "Описание": "Подростку Нэнси Томпсон предстоит раскрыть темную правду, которую скрывают ее родители, после того, как она и ее друзья во сне становятся мишенью для духа серийного убийцы с перчаткой с лезвиями, в котором, если они умрут, он убьет их в реальной жизни.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0087800/",
        "Жанр": "Ужасы",
        "Код": "9",
        "Ссылка": "https://t.me/c/2178525944/33",
        "Трейлер": "https://www.youtube.com/watch?v=z6pIZ5Vg3Qw",
        "Скачать": ""
        
    },
    10: {"Название": "Крик",
        "Описание": "Через год после убийства своей матери девочка-подросток подвергается террору со стороны убийцы в маске, который нападает на нее и ее друзей, используя устрашающие действия как часть смертельной игры.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0117571/",
        "Жанр": "Ужасы",
        "Код": "10",
        "Ссылка": "https://t.me/c/2178525944/35",
        "Трейлер": "https://www.youtube.com/watch?v=vkJQxqJwNhs",
        "Скачать": ""
        
    },
    11: {"Название": "Шпион по соседству",
        "Описание": "Бывший агент ЦРУ, Боб Хо, берется за самое сложное на сегодняшний день задание: присматривать за тремя детьми своей девушки, но все меняется, когда русский террорист нацеливается на семью",
        "Больше информации о фильме": "https://www.imdb.com/title/tt1273678/",
        "Жанр": "Комедия",
        "Код": "11",
        "Ссылка": "https://t.me/c/2178525944/37",
        "Трейлер": "https://www.youtube.com/watch?v=s_rt7udDnOQ",
        "Скачать": ""
        
    },
    12: {"Название": "Полтора шпиона",
        "Описание": "После того, как он восстановил связь с неловким приятелем из старшей школы через Facebook, скромный бухгалтер оказывается втянутым в мир международного шпионажа.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt1489889/",
        "Жанр": "Комедия",
        "Код": "12",
        "Ссылка": "https://t.me/c/2178525944/39",
        "Трейлер": "https://www.youtube.com/watch?v=vE-43jSiHx8",
        "Скачать": ""
    },
    13: {"Название": "Не грози южному централу, попивая сок у себя в квартале",
        "Описание": " Парень по кличке Пепельница переезжает в Южный Централ к своему отцу, чтобы стать настоящим мужчиной. Правда, папа младше сына на два года. Вскоре к «Пепельнице» приходит его кузен-гангстер Лок Дог — он учит героя основам жизни на улице.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0116126/",
        "Жанр": "Комедия",
        "Код": "13",
        "Ссылка": "https://t.me/c/2178525944/41",
        "Трейлер": "https://www.youtube.com/watch?v=9hvlUW7Q68k",
        "Скачать": ""
    },
    14: {"Название": "Один дома",
        "Описание": "Многодетная семья МакКалистеров улетает на Рождество в Париж без восьмилетнего сына Кевина — забыли про него в суматохе. Мальчик остается один в пустом доме и начинает наслаждаться жизнью без контроля родителей. Однако в этот дом задумали проникнуть грабители.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0099785/",
        "Жанр": "Комедия",
        "Код": "14",
        "Ссылка": "https://t.me/c/2178525944/42",
        "Трейлер": "https://www.youtube.com/watch?v=NrCI4QXlpis",
        "Скачать": ""
    },
    15: {"Название": "Большой Лебовски",
        "Описание": "Однажды в дом Джеффа «Чувака» Лебовски вламываются гангстеры. Они принимают героя за миллионера-однофамильца, угрозами требуют вернуть долг и портят ковер. Настоящий миллионер Лебовски отказывается компенсировать потери Чувака, но просит об одолжении — передать выкуп похитителям его жены.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0118715/",
        "Жанр": "Комедия",
        "Код": "15",
        "Ссылка": "https://t.me/c/2178525944/43",
        "Трейлер": "https://www.youtube.com/watch?v=o6lZhTdzhK8",
        "Скачать": ""
    },
    16: {"Название": "1+1",
        "Описание": "После того, как он стал полностью парализованным из-за несчастного случая во время полета на параплане, аристократ нанимает человека из пригорода в качестве своего опекуна.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt1675434/",
        "Жанр": "Драма",
        "Код": "16",
        "Ссылка": "https://t.me/c/2178525944/47",
        "Трейлер": "https://www.youtube.com/watch?v=m95M-I7Ij0o",
        "Скачать": ""
    },
    17: {"Название": "Джанго освобожденный",
        "Описание": "С помощью немецкого охотника за головами освобожденный раб отправляется спасти свою жену от жестокого владельца плантации в Миссисипи.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt1853728/",
        "Жанр": "Вестерн",
        "Код": "17",
        "Ссылка": "hhttps://t.me/c/2178525944/48",
        "Трейлер": "https://www.youtube.com/watch?v=4McenUEna3E",
        "Скачать": ""
    },
    18: {"Название": "Хранители",
        "Описание": "В версии «1985 года», где существуют супергерои, убийство коллеги отправляет активного мстителя Роршаха на след заговора, который изменит ход истории.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0409459/",
        "Жанр": "Боевик",
        "Код": "18",
        "Ссылка": "https://t.me/c/2178525944/52",
        "Трейлер": "https://www.youtube.com/watch?v=12q2pDWPuyI",
        "Скачать": ""
    },
    19: {"Название": "Зелёная миля",
        "Описание": "История, происходящая в камере смертников, где добрый великан Джон Коффи обладает таинственной силой исцелять недуги людей. Когда главный охранник, Пол Эджкомб, распознает дар Джона, он пытается помочь предотвратить казнь приговоренного.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0120689/",
        "Жанр": "Драма",
        "Код": "19",
        "Ссылка": "https://t.me/c/2178525944/53",
        "Трейлер": "https://www.youtube.com/watch?v=TODt_q-_4C4",
        "Скачать": ""
    },
    20: {"Название": "Достучаться до небес",
        "Описание": "Двое неизлечимо больных пациентов сбегают из больницы, угоняют машину и устремляются к морю.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0119472/",
        "Жанр": "Драма",
        "Код": "20",
        "Ссылка": "https://t.me/c/2178525944/54",
        "Трейлер": "https://www.youtube.com/watch?v=Slm8s89WTOo",
        "Скачать": ""
    },
    21: {"Название": "Леон",
        "Описание": "12-летнюю Матильду неохотно берет к себе Леон, профессиональный убийца, после того, как ее семью убили. Возникают необычные отношения, когда она становится его протеже и изучает ремесло убийцы.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0110413/",
        "Жанр": "Драма",
        "Код": "21",
        "Ссылка": "https://t.me/c/2178525944/55",
        "Трейлер": "https://www.youtube.com/watch?v=hvya_q8KM80",
        "Скачать": ""
    },
    22: {"Название": "Гладиатор",
        "Описание": "Бывший римский полководец намеревается отомстить продажному императору, который убил его семью и отправил его в рабство.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0172495/",
        "Жанр": "Драма",
        "Код": "22",
        "Ссылка": "https://t.me/c/2178525944/56",
        "Трейлер": "https://www.youtube.com/watch?v=F2Dr7Qb2Zf8",
        "Скачать": ""
        
    },
    23: {"Название": "Крёстный отец",
        "Описание": "Дон Вито Корлеоне, глава мафиозной семьи, решает передать свою империю младшему сыну Майклу. Однако его решение непреднамеренно ставит жизни его близких под серьезную опасность.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0068646/",
        "Жанр": "Криминал",
        "Код": "23",
        "Ссылка": "https://t.me/c/2178525944/57",
        "Трейлер": "https://www.youtube.com/watch?v=E3b9jVCUh7Q",
        "Скачать": ""
        
    },
    24: {"Название": "Назад в будущее",
        "Описание": "Марти Макфлай, 17-летний старшеклассник, случайно отправляется на 30 лет в прошлое на путешествующем во времени автомобиле DeLorean, изобретенном его близким другом, ученым-индивидуалистом Доком Брауном.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0088763/",
        "Жанр": "Фантастика",
        "Код": "24",
        "Ссылка": "https://t.me/c/2178525944/58",
        "Трейлер": "https://www.youtube.com/watch?v=ou8w0gQHlRE",
        "Скачать": ""
        
    },
    25: {"Название": "Бойцовский клуб",
        "Описание": "Офисный работник, страдающий бессонницей, и безрассудный мыловар создают подпольный бойцовский клуб, который перерастает в нечто большее.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0137523/",
        "Жанр": "Драма",
        "Код": "25",
        "Ссылка": "https://t.me/c/2178525944/59",
        "Трейлер": "https://www.youtube.com/watch?v=C7-7qQ61QHU",
        "Скачать": ""
        
    },
    26: {"Название": "Остров проклятых",
        "Описание": "Тедди Дэниелс и Чак Оул, два маршала США, отправляются в психиатрическую лечебницу на отдаленном острове, чтобы расследовать исчезновение пациента, где Тедди узнает шокирующую правду об этом месте.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt1130884/",
        "Жанр": "Триллер",
        "Код": "26",
        "Ссылка": "https://t.me/c/2178525944/60",
        "Трейлер": "https://www.youtube.com/watch?v=_l7R9Rz5URw",
        "Скачать": ""
        
    },
    27: {"Название": "Поймай мне, если сможешь",
        "Описание": "Фрэнку едва исполнилось 17, и он уже умелый фальшивомонетчик, успевший выдать себя за врача, юриста и пилота. Агент ФБР, Карл, становится одержим идеей выследить мошенника, который только наслаждается погоней.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0264464/",
        "Жанр": "Криминал",
        "Код": "27",
        "Ссылка": "https://t.me/c/2178525944/62",
        "Трейлер": "https://www.youtube.com/watch?v=nH3wJYOlXYw",
        "Скачать": ""
        
    },
    28: {"Название": "Молчание ягнят",
        "Описание": "Молодой курсант ФБР должен получить помощь от заключенного и манипулятивного убийцы-каннибала, чтобы помочь поймать другого серийного убийцу — безумца, который сдирает кожу со своих жертв.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0102926/",
        "Жанр": "Триллер",
        "Код": "28",
        "Ссылка": "https://t.me/c/2178525944/63",
        "Трейлер": "https://www.youtube.com/watch?v=m8Da_mQKd_8",
        "Скачать": ""
        
    },      
    29: {
        "Название": "Лицо со шрамом",
        "Описание": "Весной 1980 года был открыт порт Мэйриэл Харбор, и тысячи кубинских беженцев ринулись в Соединенные Штаты на поиски Американской Мечты. Один из них нашел ее на залитых солнцем улицах Майами. Богатство, власть и страсть превзошли даже самые невероятные его мечты. Его звали Тони Монтана. Мир запомнил его под другим именем — Лицо со шрамом.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0086250/",
        "Жанр": "Боевик",
        "Код": "29",
        "Ссылка": "https://t.me/c/2178525944/64",
        "Трейлер": "https://www.youtube.com/watch?v=mU0DdjbF8IQ",
        "Скачать": ""
    },
    30: {
        "Название": "Гадкий я 4",
        "Описание": "Грю, всемирно любимый суперзлодей, ставший агентом Антизлодейской лиги, отправляется в новую захватывающую историю о хаосе Миньонов вместе со своей женой и коллегой Люси, тремя приёмными девочками — Марго, Эдит и Агнес — и новым членом семьи Грю, Грю-младшим, вознамерившимся помучить своего отца. Семья вынуждена пуститься в бега, став мишенью для беглого преступника Максима Ле Маля и его возлюбленной Валентины.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt7510222/",
        "Жанр": "Комедия",
        "Код": "30",
        "Ссылка": "https://t.me/c/2178525944/65",
        "Новинки": "Новинки",
        "Трейлер": "https://www.youtube.com/watch?v=7G9nzhszvGs",
        "Скачать": ""
    },
    31: {
        "Название": "Головоломка 2",
        "Описание": "Продолжение, в котором Райли вступает в половую зрелость и в результате испытывает совершенно новые, более сложные эмоции. Пока Райли пытается приспособиться к своим подростковым годам, ее старые эмоции пытаются приспособиться к возможности быть замененными.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt22022452/",
        "Жанр": "Комедия",
        "Код": "31",
        "Ссылка": "https://t.me/c/2178525944/66",
        "Новинки": "Новинки",
        "Трейлер": "https://www.youtube.com/watch?v=xbSLz5lR520",
        "Скачать": ""
    }, 
    
   32:  {
       "Название": "Бегущий по лезвию 2049",
        "Описание": "Офицер полиции К находит давно похищенного бывшего Репликанта, что ставит под угрозу все живое.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt1856101/",
        "Жанр": "Фантастика",
        "Код": "32",
        "Ссылка": "https://t.me/c/2178525944/67",
        "Трейлер": "https://www.youtube.com/watch?v=taQW31SVPCk",
        "Скачать": ""
    },
    33: {
        "Название": "Марсианин",
        "Описание": "Астронавт оказывается застрявшим на Марсе и пытается выжить, используя свои знания о ботанике.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt3659388/",
        "Жанр": "Фантастика",
        "Код": "33",
        "Ссылка": "https://t.me/c/2178525944/68",
        "Трейлер": "https://www.youtube.com/watch?v=tvkoZF1BMec",
        "Скачать": ""
    },
    34: {
        "Название": "Гравитация",
        "Описание": "Астронавты пытаются выжить в космосе после разрушения их шаттла.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt1454468/",
        "Жанр": "Фантастика",
        "Код": "34",
        "Ссылка": "https://t.me/c/2178525944/69",
        "Трейлер": "https://www.youtube.com/watch?v=OZ-64FmA8WY",
        "Скачать": ""
    },
    35: {
        "Название": "Прометей",
        "Описание": "Экспедиция к дальним планетам открывает опасную тайну о происхождении человечества.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt1446714/",
        "Жанр": "Фантастика",
        "Код": "35",
        "Ссылка": "https://t.me/c/2178525944/70",
        "Трейлер": "https://www.youtube.com/watch?v=BzllHdG9C8g",
        "Скачать": ""
    },
    36: {
        "Название": "Вспомнить всё",
        "Описание": "Рабочий в будущем решает изменить свою жизнь с помощью воспоминаний, но сталкивается с непростой реальностью.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt0100802/",
        "Жанр": "Фантастика",
        "Код": "36",
        "Ссылка": "https://t.me/c/2178525944/72",
        "Трейлер": "https://www.youtube.com/watch?v=6acW6-dmxKs",
        "Скачать": ""
    },
    37: {
        "Название": "Элизиум",
        "Описание": "Будущее, где богатые живут на искусственной планете, а бедные остаются на Земле. Один человек решает изменить это.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt2178470/",
        "Жанр": "Фантастика",
        "Код": "37",
        "Ссылка": "https://t.me/c/2178525944/73",
        "Трейлер": "https://www.youtube.com/watch?v=kJOoglkhJJ4",
        "Скачать": ""
    },
    38: {
        "Название": "Дэдпул и Россомаха",
        "Описание": "Управление по изменению времени предлагает Дэдпулу место в Кинематографической вселенной Marvel, но вместо этого нанимает вариант Росомахи, чтобы спасти свою вселенную от вымирания.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt6263850/",
        "Жанр": "Фантастика",
        "Код": "38",
        "Ссылка": "https://t.me/c/2178525944/74",
        "Новинки": "Новинки",
        "Трейлер": "https://www.youtube.com/watch?v=uTfkgia3BxQ",
        "Скачать": ""
    },
    39: {
        "Название": "Винни-Пух: Кровь и мёд",
        "Описание": "После того, как Кристофер Робин бросает их ради колледжа, Пух и Пятачок пускаются в кровавые разборки в поисках нового источника пищи.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt19623240/",
        "Жанр": "Ужасы",
        "Код": "39",
        "Ссылка": "https://ify.ac/1Lom",
        "Новинки": "Новинки",
        "Трейлер": "https://www.youtube.com/watch?v=9BqNyhVvsnk",
        "Скачать": ""
    },
    40: {
        "Название": "Оппенгеймер",
        "Описание": "История американского ученого Дж. Роберта Оппенгеймера и его роли в разработке атомной бомбы.",
        "Больше информации о фильме": "https://www.imdb.com/title/tt15398776/",
        "Жанр": "Биография",
        "Код": "40",
        "Ссылка": "https://t.me/c/2178525944/81",
        "Трейлер": "https://ify.ac/1LqL",
        "Скачать": "https://t.me/c/2178525944/81"
    }
}

showed_movies = {} 

def search(message):
    chat_id = call.message.chat.id  
    channel1 = "-1002219725769" # ID первого канала
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('↩️ Назад в меню', callback_data='return_to_menu')
    if check_subscription(chat_id, channel1):
        try:
            n = int(message.text)  # Получаем число из сообщения

            if n in my_dict:
                movie = my_dict[n]
                button2 = types.InlineKeyboardButton('Смотреть бесплатно', url=movie["Ссылка"])
                button3 = types.InlineKeyboardButton('Трейлер', url=movie["Трейлер"])
                button4 = types.InlineKeyboardButton('Скачать',url=movie["Скачать"])  # Ссылка из словаря

                markup.add(button2, button3, button1)
                markup.add(button4)  # Добавляем кнопки в нужном порядке
            
                response = (f"Название: {movie['Название']}\n\n"
                            f"Описание: {movie['Описание']}\n\n"
                            f"Больше информации о фильме: {movie['Больше информации о фильме']}\n\n"
                            f"Код фильма: {movie['Код']}")
                bot.send_message(message.chat.id, response, reply_markup=markup)
            else:
                markup.add(button1)  # Добавляем кнопку "Назад в меню", если фильм не найден
                bot.send_message(message.chat.id, "Фильм не найден. Пожалуйста, попробуйте другой номер.", reply_markup=markup)

        except ValueError:
            markup.add(button1)  # Добавляем кнопку "Назад в меню", если введено некорректное значение
            bot.send_message(message.chat.id, "Пожалуйста, введите корректное числовое значение.", reply_markup=markup)
    else:  
        bot.send_message(chat_id, "Подпишитесь на канал, чтобы использовать бота.", reply_markup=start_markup()) 
        


def searchGenre(message): 
    global showed_movies
    user_id = message.chat.id
    chat_id = call.message.chat.id  
    channel1 = "-1002219725769" # ID первого канала
    
    if user_id not in showed_movies:
        showed_movies[user_id] = []

    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('↩️ Назад в меню', callback_data='menu')
    markup.add(button1)

    genre_map = {
        'Фантастика': "Фантастика",
        'Драма': "Драма",
        'Ужасы': "Ужасы",
        'Комедия': "Комедия",
        'Романтика': "Романтика",
        'Вестерн': "Вестерн",
        'Триллер': "Триллер",
        'Боевик': "Боевик",
        'Криминал': "Криминал",
        'Биография': "Биография"
    }

    genre_key = message.text.capitalize()  # Приводим текст сообщения к корректному формату
    response = ""

    if genre_key in genre_map:
        genre_name = genre_map[genre_key]
        response += f"Фильм в жанре '{genre_name}':\n"
        movies_in_genre = [movie for movie in my_dict.values() if movie["Жанр"] == genre_name]

        # Исключаем уже показанные фильмы
        movies_in_genre = [movie for movie in movies_in_genre if movie['Название'] not in showed_movies[user_id]]

        if movies_in_genre:
            # Выбираем случайный фильм из списка
            selected_movie = random.choice(movies_in_genre)
            response += f"\nНазвание: {selected_movie['Название']}\n\nОписание: {selected_movie['Описание']}\nБольше информации о фильме: {selected_movie['Больше информации о фильме']}\n\nКод фильма: {selected_movie['Код']}"
            # Добавляем показанный фильм в список
            button2 = types.InlineKeyboardButton('Смотреть бесплатно', url=selected_movie['Ссылка'])
            button3 = types.InlineKeyboardButton('Трейлер', url=selected_movie["Трейлер"])
            button4 = types.InlineKeyboardButton('Скачать фильм', url=selected_movie["Скачать"])  # Ссылка из словаря
            markup.add(button2)
            markup.add(button3, button4)

            showed_movies[user_id].append(selected_movie['Название'])
        else:
            response = f"Все фильмы в жанре '{genre_name}' уже показаны."

    else:
        response = "Пожалуйста, выберите другой жанр."
    if check_subscription(chat_id, channel1):
        bot.send_message(message.chat.id, response, reply_markup=markup)
    else:  
        bot.send_message(chat_id, "Подпишитесь на канал, чтобы использовать бота.", reply_markup=start_markup())

def searchName(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton('↩️ Назад в меню', callback_data='to_menu')
    markup.add(button1)
    movie_name = message.text.lower()
    movie_found = False
    chat_id = call.message.chat.id  
    channel1 = "-1002219725769" # ID первого канала

    if check_subscription(chat_id, channel1):
        for movie in my_dict.values():
            if movie["Название"].lower() == movie_name:
                response = f"Название: {movie['Название']}\n\nОписание: {movie['Описание']}\n\nБольше информации о фильме: {movie['Больше информации о фильме']}\nЖанр: {movie['Жанр']}\n\nКод фильма: {movie['Код']}"
            
                button2 = types.InlineKeyboardButton('Смотреть бесплатно', url=movie['Ссылка'])
                button3 = types.InlineKeyboardButton('Трейлер', url=movie["Трейлер"])
                button4 = types.InlineKeyboardButton('Скачать фильм', url=movie["Скачать"])  # Ссылка из словаря
                markup.add(button2, button3)
                markup.add(button4)
            
                bot.send_message(message.chat.id, response, reply_markup=markup)
                movie_found = True
                break  # Выходим из цикла, как только находим фильм
    
        if not movie_found:
            bot.send_message(message.chat.id, "Фильм не был найден", reply_markup=markup)
    else:  
        bot.send_message(chat_id, "Подпишитесь на канал, чтобы использовать бота.", reply_markup=start_markup())

def newFilms(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('↩️ Назад в меню', callback_data='return_menu')
    markup.add(button1)
    chat_id = call.message.chat.id  
    channel1 = "-1002219725769" # ID первого канала
    
    # Создаем список новинок
    new_movies = [movie for movie in my_dict.values() if movie.get('Новинки') == 'Новинки']
    
    # Проверяем, есть ли новинки
    if check_subscription(chat_id, channel1):
        if new_movies:
            # Выбираем случайный фильм
            movie = random.choice(new_movies)
            response = (f"Название: {movie['Название']}\n\n"
                        f"Описание: {movie['Описание']}\n\n"
                        f"Больше информации о фильме: {movie['Больше информации о фильме']}\n"
                        f"Жанр: {movie['Жанр']}\n\n"
                        f"Код фильма: {movie['Код']}\n\n")
            button2 = types.InlineKeyboardButton('Смотреть бесплатно', url=movie['Ссылка'])
            button3 = types.InlineKeyboardButton('Трейлер', url=movie["Трейлер"])
            button4 = types.InlineKeyboardButton('Скачать фильм', url=movie["Скачать"])  # Ссылка из словаря
            markup.add(button1, button2)
            markup.add(button3, button4)

            bot.send_message(message.chat.id, response, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Фильм не был найден", reply_markup=markup)
    else:  
        bot.send_message(chat_id, "Подпишитесь на канал, чтобы использовать бота.", reply_markup=start_markup())
        
def tgk(message):
    # Тут оставим ссылку на наш приватный тг канал
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('↩️ Назад в меню', callback_data='to_')
    markup.add(button1)

    bot.send_message(message.chat.id, 'Подпишись -> https://t.me/+DJTaOu_I6q9jMGVi', reply_markup=markup)


def settings(message):
    # Если хочешь, то дополни настройки
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('↩️ Назад в меню', callback_data='return_to_enu')
    markup.add(button1)
    bot.send_message(message.chat.id, 'О проблемах писать -> @alexpltz', reply_markup=markup)

    
# Создаем базу данных при запуске бота
create_database()


bot.polling(none_stop=True)
