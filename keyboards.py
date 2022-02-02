from telebot import types
from ibm_translate import voices

languages = {
    'avto': 'Автоопределение',
    'hu': 'Венгерский',
    'en': 'Английский',
    'vi': 'Вьетнамский',
    'ar': 'Арабский',
    'nl': 'Голландский',
    'bn': 'Бенгальский',
    'el': 'Греческий',
    'bg': 'Болгарский',
    'gu': 'Гуджарати',
    'bs': 'Боснийский',
    'da': 'Датский',
    'cy': 'Валлийский',
    'he': 'Иврит',

    'id': 'Индонезийский',
    'lv': 'Латышский',
    'ga': 'Ирландсикй',
    'lt': 'Литовский',
    'es': 'Испанискй',
    'ms': 'Малайский',
    'it': 'Итальянский',
    'ml': 'Малаялам',
    'zh-TW': 'Китайский (традиционный)',
    'mt': 'Мальтийский',
    'zh': "Китайсикй (упрощенный)",
    'de': 'Немецкий',
    'ko': 'Корейский',
    'ne': 'Непальский',

    'nb': 'Норвежский букмол',
    'sl': 'Словенский',
    'pl': 'Польский',
    'th': 'Тайский',
    'pt': 'Португальский',
    'ta': 'Тамильский',
    'ro': 'Румынский',
    'te': 'Телугу',
    'ru': 'Русский',
    'tr': 'Турецкий',
    'si': 'Сингальский',
    'uk': 'Украинский',
    'sk': 'Словацкий',
    'ur': 'Урду',

    'fi': 'Финский',
    'cs': 'Чешский',
    'fr': 'Французский',
    'sv': 'Шведский',
    'hi': 'Хинди',
    'et': 'Эстонский',
    'hr': 'Хорватский',
    'ja': 'Японский',
}

lang_audio = ('en', 'ar', 'nl', 'es', 'it', 'de', 'ko', 'pt', 'fr', 'ja')


def index_search(language):
    dictionary = languages.copy()

    index = 0
    page = 0

    for i, j in dictionary.items():
        if i == language:
            index = list(dictionary).index(i)

    while index not in range(page, page + 14):
        page = page + 14

    return page


def emoji(language, flag):
    if flag == 'target':
        for i in range(0, len(voices)):
            if language == list(voices.keys())[i][:2]:
                return ' 🔊'
    else:
        for i in range(0, len(lang_audio)):
            if language == lang_audio[i]:
                return ' 🎤'
    return ''


def accept(language, button):
    if language == button:
        return '✅ '
    else:
        return ''


def translate_keyboard(language, page, flag):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    for i in range(page, page + 14, 2):

        if i == 50:
            break

        button1 = types.InlineKeyboardButton(text=accept(language, list(languages.keys())[i]) + list(languages.values())[i] + emoji(list(languages.keys())[i], flag), callback_data=list(languages.keys())[i])

        button2 = types.InlineKeyboardButton(text=accept(language, list(languages.keys())[i+1]) + list(languages.values())[i + 1] + emoji(list(languages.keys())[i], flag), callback_data=list(languages.keys())[i + 1])

        keyboard.add(button1, button2)

    if page == 0:
        button_next = types.InlineKeyboardButton(text='➡', callback_data='next')
        keyboard.add(button_next)
    elif page == 42:
        button_previous = types.InlineKeyboardButton(text='⬅', callback_data='previous')
        keyboard.add(button_previous)
    else:
        button_next = types.InlineKeyboardButton(text='➡', callback_data='next')
        button_previous = types.InlineKeyboardButton(text='⬅', callback_data='previous')
        keyboard.add(button_previous, button_next)

    return keyboard


def audio_accompaniment(switch):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    if switch == 'off':
        button1 = types.InlineKeyboardButton(text='Вкл', callback_data='on')
        button2 = types.InlineKeyboardButton(text='✅ Откл', callback_data='off')
    else:
        button1 = types.InlineKeyboardButton(text='✅ Вкл', callback_data='on')
        button2 = types.InlineKeyboardButton(text='Откл', callback_data='off')
    keyboard.add(button1, button2)
    return keyboard
