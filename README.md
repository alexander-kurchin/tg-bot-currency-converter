# tg-bot-currency-converter
 > Простой Telegram бот-конвертер валют

Это итоговый проект по теме ООП из курса «Интенсив Python-разработчик» от SkillFactory.

# Как создать бота?

Для того чтобы создать бота, вам необходимо написать боту *[@BotFather](https://t.me/botfather)* и выполнить несколько простых шагов.

Используйте команду ***/newbot***, чтобы создать нового бота.

Затем необходимо:

1. **Установить имя (*name*) вашего бота.**  
    Имя вашего бота отображается в контактной информации и в других местах.
2. **Установить имя пользователя (*username*) вашего бота.**  
    Имя пользователя — это короткое имя, которое будет использоваться для идентификации вашего бота и обращения к нему. Имена пользователей состоят из 5–32 символов и нечувствительны к регистру, могут включать только латинские символы, числа и символы подчёркивания. Имя пользователя вашего бота должно заканчиваться на **«*bot*»**, например, «*tetris_bot*» или «_TetrisBot_».
3. **Получить токен (*token*).**  
    Токен представляет собой строку вида *110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw*. Он необходим для авторизации  вашей программы, в которой реализована логика бота.

# Добавляем токен в .env

Токен — это пароль от вашего бота, поэтому храните свой токен в безопасности. Чтобы моя программа корректно работала у вас, отредактируйте файл `.env`:

Поместите ваш токен внутри кавычек:

```
TOKEN="Токен, полученный при регистрации"
```

Должно получиться что-то вроде:

```
TOKEN="110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"
```

# API для курсов ЦБ РФ
Я использовал сервис [Курсы ЦБ РФ в XML и JSON, API](https://www.cbr-xml-daily.ru/), так как он бесплатный, не требует регистрации, а официальные API ЦБ работают ненадежно (да и json мне приятнее xml :smile:).

# Размещаем код на сервере

![Схема взаимодействия пользователей, сервера tg и бота](https://optima740.github.io/image/post-2020-09-18/how_it_works.png)

Бота можно запусть прямо на своём компьютере, это удобно для тестирования во время разработки. Но готовый код лучше запустить на сервере.

Я использовал бесплатный тариф в облачной платформе [*Python*Anywhere](https://www.pythonanywhere.com/).

Загружаете файлы `main.py extensions.py currencies.py .env requirements.txt` на сервер.

Запускает консоль, и сначала устанавливаете зависимости `pip install -r /home/<ваш_username>/requirements.txt`, а затем запускаете саму программу `python /home/<ваш_username>/main.py`.

Вуаля.
