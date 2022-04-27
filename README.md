# Телеграмм бот переводчик
Переводчик в виде чат-бота. Имеет поддержку более 50 языков, голосовой ввод и вывод текста. Перевод и распознавание речи реализовано с помощью сервисов IBM, таких как Watson Language Translator и сопутствующих продуктов Watson Speech to Text и Watson Text to Speech.
### Что умеет этот бот:
+ Поддержка 50 языков для перевода текста
+ Перевод ауидосообщений (не для всех языков)
+ Дублирование пееведенного текста аудиосообщением (не для всех языков) 
### Команды чат-бота:
+ /start - запуск бота
+ /from - выбор языка с которого перевести текст
+ /to - выбор языка на который перевести текст
+ /audio - включение или выключение дублирования переведнного текста аудиосообщением 
+ /help - справка по работе с ботом
### Используемые технологии:
+ Api - pyTelegramBotAPI
+ Перевод текста - IBM Watson Language Translator
+ Распознование речи в аудиосообщениях - IBM Watson Speech to Text
+ Конвертация текста в голос - IBM Watson Text to Speech
+ Deploy - Heroku
### Пример работы чат-бота 
#### Запуск бота при помощи команды /start
![Alt text](https://github.com/bogdanov2812/Screenshots/blob/master/Telegram_Bots/Translate/start.png)
#### Выбор языка с которого осуществлять перевод при помощи команды /from
![Alt text](https://github.com/bogdanov2812/Screenshots/blob/master/Telegram_Bots/Translate/from.png)
#### Выбор языка на который осуществлять перевод при помощи команды /to
![Alt text](https://github.com/bogdanov2812/Screenshots/blob/master/Telegram_Bots/Translate/to.png)
#### Перевод простого текста
![Alt text](https://github.com/bogdanov2812/Screenshots/blob/master/Telegram_Bots/Translate/text.png)
#### Включение функции дублирования переведнного текста аудиосообщением
![Alt text](https://github.com/bogdanov2812/Screenshots/blob/master/Telegram_Bots/Translate/audio.png)
#### Перевод текста с дублированием в виде голосового сообщения
![Alt text](https://github.com/bogdanov2812/Screenshots/blob/master/Telegram_Bots/Translate/text_with_audio.png)
#### Перевод аудиосообщения
![Alt text](https://github.com/bogdanov2812/Screenshots/blob/master/Telegram_Bots/Translate/audio_to_text.png)
#### Автоопредение языка
![Alt text](https://github.com/bogdanov2812/Screenshots/blob/master/Telegram_Bots/Translate/avto.png)
#### Справка для работы с ботом /help
![Alt text](https://github.com/bogdanov2812/Screenshots/blob/master/Telegram_Bots/Translate/help.png)
