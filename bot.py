import telebot
import os

from io import BytesIO

import requests
import keyboards


from ibm_translate import *


TOKEN = os.environ["TOKEN"]
bot = telebot.TeleBot(TOKEN)


class Language:
    def __init__(self):
        self.source = 'en'
        self.source_page = 0
        self.target = 'ru'
        self.target_page = 0
        self.audio = 'off'


language = Language()


@bot.message_handler(commands={'start'})
def start_window(message):
    bot.send_message(message.chat.id, 'Этот бот умеет переводить текст на многие языки, а также распознавать аудиосообщения и дублировать переведнный текст голосом\n'
                                      'Чтобы выбрать язык с которого вы хотите перевести текст введите команду "/from" \n'
                                      'Чтобы выбрать язык на который вы хотите перевести текст введите команду "/to" \n'
                                      'Чтобы включить или выключить дублирование переведенного текста аудиосообщением введите команду "/audio" \n'
                                      'Для перевода текста просто напишите или скопируйте его в поле "Сообщение..." и нажмите отправить! \n'
                                      'Языки, поддерживаемые для голосового ввода отмечены значком 🎤 \n'
                                      'Языки, поддерживающие дублирование текста аудиосообщением отмечены значком 🔊 \n')
    
@bot.message_handler(commands={'help'})
def start_window(message):
    bot.send_message(message.chat.id, 'Справка \n'
                                      'Чтобы выбрать язык с которого вы хотите перевести текст введите команду "/from" \n'
                                      'Чтобы выбрать язык на который вы хотите перевести текст введите команду "/to" \n'
                                      'Чтобы включить или выключить дублирование переведенного текста аудиосообщением введите команду "/audio" \n'
                                      'Для перевода текста просто напишите или скопируйте его в поле "Сообщение..." и нажмите отправить! \n'
                                      'Языки, поддерживаемые для голосового ввода отмечены значком 🎤 \n'
                                      'Языки, поддерживающие дублирование текста аудиосообщением отмечены значком 🔊 \n')    


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
    audio = file.content

    speech_models = speech_to_text.list_models().get_result()
    speech_models = speech_models['models']

    for i in range(0, len(speech_models)):
        if language.source == speech_models[i]['language'][:2]:
            text = speech_to_text.recognize(audio=BytesIO(audio), model=speech_models[i]['name'], content_type='audio/ogg;codecs=opus').get_result()
            if len(text['results']) == 0:
                bot.send_message(message.chat.id, 'Ошибка идентефикации')
                return
            else:
                text = text['results'][0]['alternatives'][0]['transcript']
                translation = language_translator.translate(text=[text],
                                                            source=language.source,
                                                            target=language.target).get_result()
                translation = translation['translations'][0]['translation']
                message1 = bot.send_message(message.chat.id, translation, reply_to_message_id=message.message_id)
                if language.audio == 'on':
                    try:
                        bot.send_voice(message.chat.id, select_voice(translation, language.target), reply_to_message_id=message1.message_id)
                    except Exception as e:
                        print(e)
                break
    else:
        bot.send_message(message.chat.id, 'Вы выбрали язык, не доступный для голосового ввода')


@bot.message_handler(commands={'audio', 'from', 'to'})
def commands(message):
    try:
        if message.text == '/audio':
            bot.send_message(message.chat.id, "Дублирование переведенного текста голосом", reply_markup=keyboards.audio_accompaniment(language.audio))
        elif message.text == '/from':
            language.source_page = keyboards.index_search(language.source)
            bot.send_message(message.chat.id, "Перевести текст с языка:",
                             reply_markup=keyboards.translate_keyboard(language.source, language.source_page, 'source'))
        elif message.text == '/to':
            language.target_page = keyboards.index_search(language.target)
            bot.send_message(message.chat.id, "Перевести текст на язык:",
                             reply_markup=keyboards.translate_keyboard(language.target, language.target_page, 'target'))
    except Exception as e:
        print(e)


@bot.callback_query_handler(func=lambda call: True)
def keyboards_calls(call):
    try:
        if call.message.text == 'Перевести текст с языка:':
            if call.data == 'next':
                language.source_page += 14
            elif call.data == 'previous':
                language.source_page -= 14
            else:
                language.source = call.data
                name = find_name(keyboards.languages, language.source)
                bot.send_message(call.message.chat.id, "Перевод текста с языка: " + name.lower())
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=keyboards.translate_keyboard(language.source, language.source_page, 'source'))

        elif call.message.text == 'Перевести текст на язык:':
            if call.data == 'next':
                language.target_page += 14
            elif call.data == 'previous':
                language.target_page -= 14
            elif call.data != 'avto':
                language.target = call.data
                name = find_name(keyboards.languages, language.target)
                bot.send_message(call.message.chat.id, text='Перевод текста на язык: ' + name.lower())
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=keyboards.translate_keyboard(language.target, language.target_page, 'target'))

        elif call.message.text == 'Дублирование переведенного текста голосом':
            language.audio = call.data
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=keyboards.audio_accompaniment(language.audio))

    except Exception as e:
        print(e)


@bot.message_handler(func=lambda message: True)
def translate(message):
    translate_text = message.text

    if language.source == 'avto':  # В качестве источника выбрано "Автоопределение"
        source_language = response_to_list(language_translator.identify(translate_text).get_result())  # Распознование введенного текста
        source_language = language_identification(keyboards.languages, source_language)
        if source_language == 0:
            bot.send_message(message.chat.id, "Идентефицированный язык не доступен для перевода")
            return
        elif source_language[0] == language.target:
            bot.send_message(message.chat.id, 'Идентефицированный язык совпадает с целевым языком')
            return

        bot.send_message(message.chat.id, 'Идентефицированный язык: ' + source_language[1].lower())
        translation = language_translator.translate(text=[translate_text], source=source_language[0], target=language.target).get_result()
    elif language.source == language.target:
        bot.send_message(message.chat.id, 'Исходный язык совпадает с целевым')
        return
    else:
        translation = language_translator.translate(text=[translate_text], source=language.source, target=language.target).get_result()

    translation = json.dumps(translation, indent=2, ensure_ascii=False)
    translation = json.loads(translation)
    translation = translation['translations'][0]['translation']

    print(translation)

    message1 = bot.send_message(message.chat.id, translation, reply_to_message_id=message.message_id)

    if language.audio == 'on':
        try:
            bot.send_voice(message.chat.id, select_voice(translation, language.target), reply_to_message_id=message1.message_id)
        except Exception as e:
            print(e)


bot.polling(none_stop=True, timeout=60)
